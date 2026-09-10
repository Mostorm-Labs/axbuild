from pathlib import Path

import pytest

from axbuild.model import ArtifactRef, ResolveRequest


def test_artifact_ref_is_hashable_and_immutable() -> None:
    ref = ArtifactRef(
        family="demo",
        kind="runtime",
        key="windows-x64",
        identity="id-1",
        repository="org/repo",
        release_tag="sdk-v1",
        asset="demo.zip",
        sha256="a" * 64,
    )
    assert {ref: "ok"}[ref] == "ok"
    with pytest.raises((AttributeError, TypeError)):
        ref.asset = "other.zip"  # type: ignore[misc]


def test_resolve_request_normalizes_paths(tmp_path: Path) -> None:
    request = ResolveRequest(
        repo_root=tmp_path / "project",
        target="windows-x64",
        store_root=tmp_path / "store",
    )
    assert request.repo_root.is_absolute()
    assert request.store_root.is_absolute()
    assert request.target == "windows-x64"
    assert request.mirror is None
    assert request.offline is False
