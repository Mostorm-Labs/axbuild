import json
from pathlib import Path
import subprocess
import sys

import pytest

from axbuild.archive import file_sha256
from axbuild.errors import ContractError, IntegrityError
from axbuild.provider import ProviderRegistry
from axbuild.model import ResolveRequest
from axbuild.seed import (
    NEARCAST_AIRPLAY_FAMILY,
    build_nearcast_airplay_seed,
    load_provenance,
    seed_artifact_identity,
)
from examples.providers.nearcast_airplay import NearCastAirPlayProvider


REQUIRED_FILES = {
    "gstreamer/lib/pkgconfig/gstreamer-1.0.pc": "gstreamer",
    "gstreamer/bin/gst-inspect-1.0.exe": "inspect",
    "dnssd/Include/dns_sd.h": "dns",
    "bonjour/Bonjour64.msi": "bonjour",
    "webview2/build/native/include/WebView2.h": "webview",
    "vcpkg/installed/x64-windows/.axbuild-present": "vcpkg",
}


def write_closure(root: Path) -> None:
    for name, content in REQUIRED_FILES.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def test_seed_identity_is_deterministic_and_input_sensitive(tmp_path):
    root = tmp_path / "closure"
    write_closure(root)
    inputs = {
        "components": [
            {"name": "gstreamer", "version": "1.26.0", "source": "official-sdk"},
            {"name": "bonjour", "version": "3.0.0", "source": "official-sdk"},
        ],
        "toolchain": {"compiler": "msvc", "runtime": "vcruntime"},
    }
    first = seed_artifact_identity(root, inputs)
    second = seed_artifact_identity(root, json.loads(json.dumps(inputs)))
    assert first == second

    (root / "gstreamer/bin/gst-inspect-1.0.exe").write_text("changed", encoding="utf-8")
    assert seed_artifact_identity(root, inputs) != first


def test_build_seed_writes_four_outputs_and_valid_contracts(tmp_path):
    source = tmp_path / "closure"
    output = tmp_path / "out"
    write_closure(source)
    result = build_nearcast_airplay_seed(source, output)

    assert result.family == NEARCAST_AIRPLAY_FAMILY
    for path in (result.archive_path, result.index_path, result.provenance_path, result.lock_path):
        assert path.is_file()
    assert result.archive_path.name == "nearcast-airplay-runtime-windows-x64-release.zip"
    assert file_sha256(result.archive_path) == result.artifact_sha256
    assert result.index_sha256 == file_sha256(result.index_path)
    provenance = load_provenance(result.provenance_path)
    assert provenance["format"] == "axbuild-nearcast-airplay-provenance-v1"
    assert provenance["artifact"]["identity"] == result.artifact_identity
    assert provenance["redistribution"]["status"] == "review-required"


def test_seed_rejects_incomplete_closure(tmp_path):
    source = tmp_path / "closure"
    write_closure(source)
    (source / "dnssd/Include/dns_sd.h").unlink()
    with pytest.raises(IntegrityError, match="dnssd"):
        build_nearcast_airplay_seed(source, tmp_path / "out")


def test_provenance_rejects_unknown_top_level_fields(tmp_path):
    path = tmp_path / "provenance.json"
    path.write_text(json.dumps({"format": "axbuild-nearcast-airplay-provenance-v1", "unexpected": True}), encoding="utf-8")
    with pytest.raises(ContractError, match="unknown"):
        load_provenance(path)


def test_seed_resolves_from_empty_store_and_replays_offline(tmp_path):
    source = tmp_path / "closure"
    output = tmp_path / "out"
    write_closure(source)
    result = build_nearcast_airplay_seed(source, output)
    registry = ProviderRegistry()
    registry.register(NearCastAirPlayProvider(result.lock_path, result.provenance_path))

    online = registry.resolve(
        "nearcast-airplay",
        ResolveRequest(tmp_path / "repo", "windows-x64", tmp_path / "store", str(result.mirror_root)),
    )
    assert online.facts["index"]["source"] == "mirror"
    assert online.facts["artifacts"][0]["source"] == "mirror"
    assert online.facts["networkUsed"] is False

    offline = registry.resolve(
        "nearcast-airplay",
        ResolveRequest(tmp_path / "repo", "windows-x64", tmp_path / "store", offline=True),
    )
    assert offline.facts["index"]["source"] == "store"
    assert offline.facts["artifacts"][0]["source"] == "store"
    assert offline.facts["networkUsed"] is False


def test_seed_cli_emits_candidate_facts(tmp_path):
    source = tmp_path / "closure"
    output = tmp_path / "out"
    write_closure(source)
    result = subprocess.run(
        [sys.executable, "-m", "axbuild", "build-nearcast-airplay-seed", str(source), str(output)],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["family"] == NEARCAST_AIRPLAY_FAMILY
    assert Path(payload["lock"]).is_file()
    assert result.stderr == ""
