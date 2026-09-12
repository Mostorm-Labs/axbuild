from __future__ import annotations

import json
from pathlib import Path
import zipfile

import pytest

from axbuild.archive import file_sha256
from axbuild.contracts import load_release_index, load_sdk_lock
from axbuild.errors import ContractError, IntegrityError
from axbuild.model import ResolveRequest
from axbuild.nearcast_airplay import NearCastAirPlayProvider
from axbuild.provider import ProviderRegistry
from axbuild.publication import (
    prepare_nearcast_airplay_release,
    verify_published_release,
    verify_superseded_release,
)
from axbuild.qualification import qualify_nearcast_airplay_artifact


REPOSITORY = "Mostorm-Labs/axdeps"
RELEASE_TAG = "nearcast-airplay-runtime-windows-x64-release-testidentity"
RELEASE_SET_ID = "nearcast-airplay-set-testidentity"
ASSET_NAMES = {
    "nearcast-airplay-runtime-windows-x64-release.zip",
    "nearcast-airplay-sdk-index.json",
    "nearcast-airplay-provenance.json",
    "nearcast-airplay-sdk.lock.json",
}


def _qualified_candidate(tmp_path: Path) -> Path:
    source = tmp_path / "source.zip"
    files = {
        "gstreamer/1.0/msvc_x86_64/lib/pkgconfig/gstreamer-1.0.pc": "gstreamer",
        "gstreamer/1.0/msvc_x86_64/bin/gst-inspect-1.0.exe": "inspect",
        "dnssd/Include/dns_sd.h": "dns",
        "bonjour/Bonjour64.msi": "bonjour",
        "webview2/build/native/include/WebView2.h": "webview",
        "vcpkg/installed/x64-windows/bin/libcrypto-3-x64.dll": "vcpkg",
    }
    with zipfile.ZipFile(source, "w") as archive:
        for name, content in files.items():
            archive.writestr(name, content)
    candidate = tmp_path / "candidate"
    qualify_nearcast_airplay_artifact(source, candidate)
    return candidate


def test_prepare_release_validates_qualification_and_writes_frozen_contracts(tmp_path):
    candidate = _qualified_candidate(tmp_path)
    original_provenance = (candidate / "nearcast-airplay-provenance.json").read_bytes()

    bundle = prepare_nearcast_airplay_release(
        candidate,
        tmp_path / "publication",
        repository=REPOSITORY,
        release_tag=RELEASE_TAG,
        release_set_id=RELEASE_SET_ID,
    )

    assert {path.name for path in bundle.assets} == ASSET_NAMES
    assert bundle.provenance_path.read_bytes() == original_provenance
    assert bundle.artifact_identity.startswith(
        "nearcast-airplay-runtime-windows-x64-release-"
    )
    index = load_release_index(bundle.index_path)
    record = index.artifact("runtime", "windows-x64")
    assert index.family == "nearcast-airplay"
    assert index.release_set_id == RELEASE_SET_ID
    assert record.identity == bundle.artifact_identity
    assert record.asset == bundle.runtime_path.name
    assert record.sha256 == file_sha256(bundle.runtime_path)
    assert record.size == bundle.runtime_path.stat().st_size
    assert record.metadata["target"] == "windows-x64"
    assert record.metadata["variant"] == "release"

    lock = load_sdk_lock(bundle.lock_path)
    assert lock.repository == REPOSITORY
    assert lock.release_tag == RELEASE_TAG
    assert lock.identity == RELEASE_SET_ID
    assert lock.asset == bundle.index_path.name
    assert lock.sha256 == file_sha256(bundle.index_path)


def test_prepare_release_rejects_qualification_digest_mismatch(tmp_path):
    candidate = _qualified_candidate(tmp_path)
    report_path = candidate / "qualification-report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["artifactSha256"] = "0" * 64
    report_path.write_text(json.dumps(report), encoding="utf-8")

    with pytest.raises(IntegrityError, match="SHA256 mismatch"):
        prepare_nearcast_airplay_release(
            candidate,
            tmp_path / "publication",
            repository=REPOSITORY,
            release_tag=RELEASE_TAG,
            release_set_id=RELEASE_SET_ID,
        )


def test_prepare_release_rejects_relaxed_redistribution(tmp_path):
    candidate = _qualified_candidate(tmp_path)
    provenance_path = candidate / "nearcast-airplay-provenance.json"
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    provenance["redistribution"]["status"] = "approved"
    provenance_path.write_text(json.dumps(provenance), encoding="utf-8")

    with pytest.raises(ContractError, match="review-required"):
        prepare_nearcast_airplay_release(
            candidate,
            tmp_path / "publication",
            repository=REPOSITORY,
            release_tag=RELEASE_TAG,
            release_set_id=RELEASE_SET_ID,
        )


def test_published_release_verification_accepts_only_exact_downloaded_assets(tmp_path):
    candidate = _qualified_candidate(tmp_path)
    bundle = prepare_nearcast_airplay_release(
        candidate,
        tmp_path / "publication",
        repository=REPOSITORY,
        release_tag=RELEASE_TAG,
        release_set_id=RELEASE_SET_ID,
    )
    downloaded = tmp_path / "downloaded"
    downloaded.mkdir()
    for asset in bundle.assets:
        (downloaded / asset.name).write_bytes(asset.read_bytes())
    metadata = {
        "tagName": RELEASE_TAG,
        "isDraft": False,
        "isImmutable": True,
        "assets": [
            {
                "name": asset.name,
                "size": asset.stat().st_size,
                "digest": f"sha256:{file_sha256(asset)}",
            }
            for asset in bundle.assets
        ],
    }

    verified = verify_published_release(metadata, bundle, downloaded)

    assert verified == {asset.name: file_sha256(asset) for asset in bundle.assets}


@pytest.mark.parametrize(
    "mutation", ["wrong-tag", "mutable-release", "extra-asset", "changed-bytes"]
)
def test_published_release_verification_refuses_immutable_mismatch(tmp_path, mutation):
    candidate = _qualified_candidate(tmp_path)
    bundle = prepare_nearcast_airplay_release(
        candidate,
        tmp_path / "publication",
        repository=REPOSITORY,
        release_tag=RELEASE_TAG,
        release_set_id=RELEASE_SET_ID,
    )
    downloaded = tmp_path / "downloaded"
    downloaded.mkdir()
    for asset in bundle.assets:
        (downloaded / asset.name).write_bytes(asset.read_bytes())
    metadata = {
        "tagName": RELEASE_TAG,
        "isDraft": False,
        "isImmutable": True,
        "assets": [
            {"name": asset.name, "size": asset.stat().st_size}
            for asset in bundle.assets
        ],
    }
    if mutation == "wrong-tag":
        metadata["tagName"] = "latest"
    elif mutation == "mutable-release":
        metadata["isImmutable"] = False
    elif mutation == "extra-asset":
        metadata["assets"].append({"name": "unexpected.txt", "size": 1})
    else:
        (downloaded / bundle.runtime_path.name).write_bytes(b"changed")

    with pytest.raises((ContractError, IntegrityError)):
        verify_published_release(metadata, bundle, downloaded)


def test_published_release_resolves_online_then_replays_offline(tmp_path):
    candidate = _qualified_candidate(tmp_path)
    bundle = prepare_nearcast_airplay_release(
        candidate,
        tmp_path / "publication",
        repository=REPOSITORY,
        release_tag=RELEASE_TAG,
        release_set_id=RELEASE_SET_ID,
    )
    mirror = tmp_path / "mirror" / RELEASE_TAG
    mirror.mkdir(parents=True)
    for asset in (bundle.runtime_path, bundle.index_path):
        (mirror / asset.name).write_bytes(asset.read_bytes())

    registry = ProviderRegistry()
    registry.register(NearCastAirPlayProvider(bundle.lock_path))
    store = tmp_path / "store"
    online = registry.resolve(
        "nearcast-airplay",
        ResolveRequest(tmp_path, "windows-x64", store, str(tmp_path / "mirror")),
    )
    offline = registry.resolve(
        "nearcast-airplay",
        ResolveRequest(tmp_path, "windows-x64", store, offline=True),
    )

    assert online.facts["networkUsed"] is False
    assert online.facts["artifacts"][0]["sha256"] == file_sha256(bundle.runtime_path)
    assert offline.facts["networkUsed"] is False
    assert offline.facts["index"]["source"] == "store"
    assert offline.facts["artifacts"][0]["source"] == "store"


def test_superseded_release_verification_requires_exact_nonimmutable_assets():
    expected = {
        "runtime.zip": {
            "id": 11,
            "size": 7,
            "sha256": "a" * 64,
        },
        "index.json": {
            "id": 12,
            "size": 9,
            "sha256": "b" * 64,
        },
    }
    metadata = {
        "id": 42,
        "tag_name": "superseded-v1",
        "immutable": False,
        "assets": [
            {
                "id": values["id"],
                "name": name,
                "size": values["size"],
                "digest": f"sha256:{values['sha256']}",
                "state": "uploaded",
            }
            for name, values in expected.items()
        ],
    }

    assert verify_superseded_release(
        metadata,
        release_id=42,
        release_tag="superseded-v1",
        expected_assets=expected,
    ) == {name: values["sha256"] for name, values in expected.items()}


@pytest.mark.parametrize("mutation", ["wrong-id", "immutable", "changed-digest"])
def test_superseded_release_verification_rejects_changed_history(mutation):
    expected = {
        "runtime.zip": {
            "id": 11,
            "size": 7,
            "sha256": "a" * 64,
        }
    }
    metadata = {
        "id": 42,
        "tag_name": "superseded-v1",
        "immutable": False,
        "assets": [
            {
                "id": 11,
                "name": "runtime.zip",
                "size": 7,
                "digest": f"sha256:{'a' * 64}",
                "state": "uploaded",
            }
        ],
    }
    if mutation == "wrong-id":
        metadata["id"] = 43
    elif mutation == "immutable":
        metadata["immutable"] = True
    else:
        metadata["assets"][0]["digest"] = f"sha256:{'b' * 64}"

    with pytest.raises((ContractError, IntegrityError)):
        verify_superseded_release(
            metadata,
            release_id=42,
            release_tag="superseded-v1",
            expected_assets=expected,
        )
