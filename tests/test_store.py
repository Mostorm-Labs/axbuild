from pathlib import Path
import zipfile

import pytest

from axbuild.archive import file_sha256, extract_zip_safe
from axbuild.errors import IntegrityError
from axbuild.model import ArtifactRef, ReleaseIndexRef
from axbuild.store import SdkStore


def make_archive(tmp_path: Path, name: str = "demo.zip") -> Path:
    archive = tmp_path / name
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr("sdk/include/demo.h", "header")
    return archive


def make_ref(archive: Path) -> ArtifactRef:
    return ArtifactRef(
        family="demo",
        kind="runtime",
        key="windows-x64",
        identity="runtime-1",
        repository="org/repo",
        release_tag="sdk-v1",
        asset=archive.name,
        sha256=file_sha256(archive),
    )


def test_store_paths_are_content_and_family_namespaced(tmp_path):
    archive = make_archive(tmp_path)
    ref = make_ref(archive)
    store = SdkStore(tmp_path / "store")
    assert store.archive_path(ref) == store.root / "archives" / "sha256" / ref.sha256 / ref.asset
    assert store.package_path(ref) == store.root / "packages" / "demo" / "runtime" / "runtime-1"

    index_ref = ReleaseIndexRef("demo", "set-1", "org/repo", "sdk-v1", "index.json", "a" * 64)
    assert store.release_index_path(index_ref) == store.root / "release-sets" / "demo" / "set-1" / "index.json"


def test_materialize_installs_and_reuses_valid_package(tmp_path):
    archive = make_archive(tmp_path)
    ref = make_ref(archive)
    store = SdkStore(tmp_path / "store")
    calls = {"install": 0, "validate": 0}

    def install(source: Path, staging: Path) -> None:
        calls["install"] += 1
        extract_zip_safe(source, staging)

    def validate(root: Path) -> None:
        calls["validate"] += 1
        if not (root / "sdk/include/demo.h").is_file():
            raise IntegrityError("missing header")

    first = store.materialize_package(ref, archive, install, validate)
    second = store.materialize_package(ref, archive, install, validate)
    assert first == second == store.package_path(ref)
    assert calls["install"] == 1
    assert calls["validate"] == 2


def test_invalid_existing_package_is_integrity_failure_not_auto_repair(tmp_path):
    archive = make_archive(tmp_path)
    ref = make_ref(archive)
    store = SdkStore(tmp_path / "store")
    destination = store.package_path(ref)
    destination.mkdir(parents=True)
    (destination / "corrupt.txt").write_text("bad", encoding="utf-8")
    install_calls = 0

    def install(source: Path, staging: Path) -> None:
        nonlocal install_calls
        install_calls += 1
        extract_zip_safe(source, staging)

    def validate(root: Path) -> None:
        if not (root / "sdk/include/demo.h").is_file():
            raise IntegrityError("materialized package is invalid")

    with pytest.raises(IntegrityError, match="invalid"):
        store.materialize_package(ref, archive, install, validate)
    assert install_calls == 0
    assert (destination / "corrupt.txt").is_file()


def test_failed_staging_never_publishes_destination(tmp_path):
    archive = make_archive(tmp_path)
    ref = make_ref(archive)
    store = SdkStore(tmp_path / "store")

    def install(source: Path, staging: Path) -> None:
        extract_zip_safe(source, staging)

    def validate(root: Path) -> None:
        raise IntegrityError("fixture rejection")

    with pytest.raises(IntegrityError, match="fixture rejection"):
        store.materialize_package(ref, archive, install, validate)
    assert not store.package_path(ref).exists()
    assert not any(store.package_path(ref).parent.glob(".axbuild-staging-*"))


def test_materialize_verifies_archive_before_installer(tmp_path):
    archive = make_archive(tmp_path)
    ref = make_ref(archive)
    archive.write_bytes(b"tampered")
    store = SdkStore(tmp_path / "store")
    installed = False

    def install(source: Path, staging: Path) -> None:
        nonlocal installed
        installed = True

    with pytest.raises(IntegrityError, match="SHA256"):
        store.materialize_package(ref, archive, install, lambda root: None)
    assert installed is False
