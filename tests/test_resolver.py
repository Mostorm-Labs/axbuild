import json
from pathlib import Path
import zipfile

import pytest

from axbuild.archive import extract_zip_safe, file_sha256
from axbuild.errors import AxBuildError, ContractError, IntegrityError, OfflineError
from axbuild.model import ArtifactRef, ProviderPlan, ReleaseIndexRef, ResolveRequest
from axbuild.provider import ProviderRegistry


def write_zip(path: Path, marker: str = "sdk/marker.txt") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr(marker, "ok")


class DemoProvider:
    family = "demo"

    def __init__(self, index_ref: ReleaseIndexRef, *, tamper_plan: bool = False, tamper_metadata: bool = False):
        self._index_ref = index_ref
        self._tamper_plan = tamper_plan
        self._tamper_metadata = tamper_metadata

    def index_ref(self, request):
        return self._index_ref

    def plan(self, request, index):
        record = index.artifact("runtime", request.target)
        asset = "evil.zip" if self._tamper_plan else record.asset
        ref = ArtifactRef(
            family=self.family,
            kind=record.kind,
            key=record.key,
            identity=record.identity,
            repository=self._index_ref.repository,
            release_tag=self._index_ref.release_tag,
            asset=asset,
            sha256=record.sha256,
            size=record.size,
            metadata={"abi": {"arch": "arm64"}} if self._tamper_metadata else record.metadata,
        )
        return ProviderPlan(self.family, (ref,), {"target": request.target})

    def install(self, ref, archive, staging_root):
        extract_zip_safe(archive, staging_root)

    def validate(self, ref, materialized_root):
        if not (materialized_root / "sdk/marker.txt").is_file():
            raise IntegrityError("missing demo marker")

    def environment(self, plan, materialized):
        return {"DEMO_SDK_ROOT": str(materialized[0].root)}


def make_fixture(tmp_path: Path):
    mirror = tmp_path / "mirror"
    tag = "demo-sdk-v1"
    artifact_path = mirror / tag / "demo-runtime.zip"
    write_zip(artifact_path)
    artifact_sha = file_sha256(artifact_path)
    index = {
        "format": "axbuild-release-index-v1",
        "family": "demo",
        "releaseSetId": "demo-set-1",
        "artifacts": [
            {
                "kind": "runtime",
                "key": "windows-x64",
                "identity": "runtime-id-1",
                "asset": artifact_path.name,
                "sha256": artifact_sha,
                "size": artifact_path.stat().st_size,
                "metadata": {"abi": {"arch": "x64"}},
            }
        ],
    }
    index_path = mirror / tag / "demo-index.json"
    index_path.write_text(json.dumps(index, sort_keys=True), encoding="utf-8")
    index_ref = ReleaseIndexRef(
        "demo",
        "demo-set-1",
        "Mostorm-Labs/demo",
        tag,
        index_path.name,
        file_sha256(index_path),
    )
    request = ResolveRequest(
        repo_root=tmp_path / "repo",
        target="windows-x64",
        store_root=tmp_path / "store",
        mirror=str(mirror),
    )
    return index_ref, request


def test_registry_rejects_duplicate_family(tmp_path):
    index_ref, _ = make_fixture(tmp_path)
    provider = DemoProvider(index_ref)
    registry = ProviderRegistry()
    registry.register(provider)
    with pytest.raises(AxBuildError, match="already registered"):
        registry.register(provider)


def test_resolver_materializes_verified_artifact_and_emits_facts(tmp_path):
    index_ref, request = make_fixture(tmp_path)
    registry = ProviderRegistry()
    registry.register(DemoProvider(index_ref))

    result = registry.resolve("demo", request)

    assert Path(result.environment["DEMO_SDK_ROOT"]).is_dir()
    assert result.facts["family"] == "demo"
    assert result.facts["releaseSetId"] == "demo-set-1"
    assert result.facts["index"]["source"] == "mirror"
    assert result.facts["artifacts"][0]["source"] == "mirror"
    assert result.facts["networkUsed"] is False
    assert "token" not in json.dumps(result.facts).lower()


def test_second_resolution_can_be_fully_offline_from_store(tmp_path):
    index_ref, request = make_fixture(tmp_path)
    registry = ProviderRegistry()
    registry.register(DemoProvider(index_ref))
    registry.resolve("demo", request)

    offline_request = ResolveRequest(
        repo_root=request.repo_root,
        target=request.target,
        store_root=request.store_root,
        offline=True,
    )
    result = registry.resolve("demo", offline_request)

    assert result.facts["index"]["source"] == "store"
    assert result.facts["artifacts"][0]["source"] == "store"
    assert result.facts["networkUsed"] is False


def test_offline_missing_store_fails_closed(tmp_path):
    index_ref, request = make_fixture(tmp_path)
    registry = ProviderRegistry()
    registry.register(DemoProvider(index_ref))
    offline_request = ResolveRequest(
        repo_root=request.repo_root,
        target=request.target,
        store_root=tmp_path / "empty-store",
        offline=True,
    )
    with pytest.raises(OfflineError):
        registry.resolve("demo", offline_request)


def test_provider_cannot_select_asset_not_present_in_verified_index(tmp_path):
    index_ref, request = make_fixture(tmp_path)
    registry = ProviderRegistry()
    registry.register(DemoProvider(index_ref, tamper_plan=True))
    with pytest.raises(ContractError, match="verified index"):
        registry.resolve("demo", request)


def test_unknown_provider_family_fails(tmp_path):
    registry = ProviderRegistry()
    with pytest.raises(AxBuildError, match="unknown provider"):
        registry.resolve(
            "missing",
            ResolveRequest(tmp_path, "windows-x64", tmp_path / "store"),
        )


def test_provider_cannot_tamper_verified_artifact_metadata(tmp_path):
    index_ref, request = make_fixture(tmp_path)
    registry = ProviderRegistry()
    registry.register(DemoProvider(index_ref, tamper_metadata=True))
    with pytest.raises(ContractError, match="verified index"):
        registry.resolve("demo", request)
