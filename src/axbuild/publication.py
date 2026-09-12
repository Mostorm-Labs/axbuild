"""Prepare and verify an immutable NearCast AirPlay release bundle."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import shutil
from typing import Any, Mapping
import zipfile

from .archive import file_sha256, verify_sha256
from .contracts import (
    load_release_index,
    load_sdk_lock,
    validate_namespace,
    validate_release_tag,
    validate_repository,
)
from .errors import ContractError, IntegrityError
from .qualification import (
    ARCHIVE_NAME,
    FAMILY,
    MANIFEST_NAME,
    PROVENANCE_NAME,
    REPORT_NAME,
    TARGET,
    VARIANT,
    load_artifact_manifest,
    load_provenance,
    load_qualification_report,
)

INDEX_NAME = "nearcast-airplay-sdk-index.json"
LOCK_NAME = "nearcast-airplay-sdk.lock.json"


@dataclass(frozen=True)
class PublicationBundle:
    output_dir: Path
    repository: str
    release_tag: str
    release_set_id: str
    artifact_identity: str
    runtime_path: Path
    index_path: Path
    provenance_path: Path
    lock_path: Path

    @property
    def assets(self) -> tuple[Path, ...]:
        return (
            self.runtime_path,
            self.index_path,
            self.provenance_path,
            self.lock_path,
        )


def _json_bytes(value: Mapping[str, Any]) -> bytes:
    return (json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _write_once(path: Path, content: bytes) -> None:
    if path.exists() or path.is_symlink():
        if not path.is_file() or path.is_symlink() or path.read_bytes() != content:
            raise IntegrityError(f"immutable publication output differs: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as output:
        output.write(content)


def _copy_once(source: Path, destination: Path) -> None:
    if destination.exists() or destination.is_symlink():
        if (
            not destination.is_file()
            or destination.is_symlink()
            or file_sha256(destination) != file_sha256(source)
        ):
            raise IntegrityError(f"immutable publication output differs: {destination}")
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    with source.open("rb") as input_file, destination.open("xb") as output_file:
        shutil.copyfileobj(input_file, output_file, length=1024 * 1024)


def _verify_archive_inventory(archive_path: Path, manifest: Mapping[str, Any]) -> None:
    expected = list(manifest["files"])
    with zipfile.ZipFile(archive_path, "r") as archive:
        infos = archive.infolist()
        if [info.filename for info in infos] != [item["path"] for item in expected]:
            raise IntegrityError("qualified runtime inventory differs from artifact manifest")
        for info, item in zip(infos, expected, strict=True):
            if info.is_dir() or info.file_size != item["size"]:
                raise IntegrityError(f"qualified runtime entry size differs: {info.filename}")
            digest = hashlib.sha256()
            with archive.open(info, "r") as source:
                for chunk in iter(lambda: source.read(1024 * 1024), b""):
                    digest.update(chunk)
            if digest.hexdigest() != item["sha256"].lower():
                raise IntegrityError(f"qualified runtime entry digest differs: {info.filename}")


def prepare_nearcast_airplay_release(
    qualification_dir: Path,
    output_dir: Path,
    *,
    repository: str,
    release_tag: str,
    release_set_id: str,
) -> PublicationBundle:
    """Validate one qualified instance and materialize its four release assets."""
    qualification_dir = Path(qualification_dir).expanduser().absolute()
    output_dir = Path(output_dir).expanduser().absolute()
    repository = validate_repository(repository)
    release_tag = validate_release_tag(release_tag)
    release_set_id = validate_namespace(release_set_id)

    runtime_input = qualification_dir / ARCHIVE_NAME
    manifest_path = qualification_dir / MANIFEST_NAME
    provenance_input = qualification_dir / PROVENANCE_NAME
    report_path = qualification_dir / REPORT_NAME
    for path in (runtime_input, manifest_path, provenance_input, report_path):
        if not path.is_file() or path.is_symlink():
            raise IntegrityError(f"qualification input is missing or unsafe: {path}")

    manifest = load_artifact_manifest(manifest_path)
    provenance = load_provenance(provenance_input)
    report = load_qualification_report(report_path)
    identity = manifest["artifactIdentity"]
    if provenance["artifactIdentity"] != identity or report["artifactIdentity"] != identity:
        raise ContractError("qualification artifact identities differ")
    verify_sha256(runtime_input, report["artifactSha256"])
    _verify_archive_inventory(runtime_input, manifest)

    runtime_path = output_dir / ARCHIVE_NAME
    provenance_path = output_dir / PROVENANCE_NAME
    index_path = output_dir / INDEX_NAME
    lock_path = output_dir / LOCK_NAME
    _copy_once(runtime_input, runtime_path)
    _copy_once(provenance_input, provenance_path)

    index = {
        "format": "axbuild-release-index-v1",
        "family": FAMILY,
        "releaseSetId": release_set_id,
        "artifacts": [
            {
                "kind": "runtime",
                "key": TARGET,
                "identity": identity,
                "asset": ARCHIVE_NAME,
                "sha256": report["artifactSha256"].lower(),
                "size": runtime_input.stat().st_size,
                "metadata": {
                    "target": TARGET,
                    "variant": VARIANT,
                    "fileCount": len(manifest["files"]),
                    "artifactManifestSha256": file_sha256(manifest_path),
                    "provenanceSha256": file_sha256(provenance_input),
                    "qualificationReportSha256": file_sha256(report_path),
                },
            }
        ],
    }
    _write_once(index_path, _json_bytes(index))
    parsed_index = load_release_index(index_path)
    if parsed_index.family != FAMILY or parsed_index.release_set_id != release_set_id:
        raise ContractError("generated release index differs from frozen authority")

    lock = {
        "format": "axbuild-sdk-lock-v1",
        "family": FAMILY,
        "repository": repository,
        "releaseTag": release_tag,
        "releaseSetId": release_set_id,
        "indexAsset": INDEX_NAME,
        "indexSha256": file_sha256(index_path),
    }
    _write_once(lock_path, _json_bytes(lock))
    parsed_lock = load_sdk_lock(lock_path)
    if (
        parsed_lock.repository != repository
        or parsed_lock.release_tag != release_tag
        or parsed_lock.identity != release_set_id
        or parsed_lock.sha256 != file_sha256(index_path)
    ):
        raise ContractError("generated SDK lock differs from frozen authority")

    return PublicationBundle(
        output_dir,
        repository,
        release_tag,
        release_set_id,
        identity,
        runtime_path,
        index_path,
        provenance_path,
        lock_path,
    )


def verify_published_release(
    metadata: Mapping[str, Any],
    bundle: PublicationBundle,
    downloaded_dir: Path,
) -> dict[str, str]:
    """Verify exact metadata and downloaded bytes without permitting mutation."""
    if not isinstance(metadata, Mapping):
        raise ContractError("GitHub release metadata must be an object")
    if metadata.get("tagName") != bundle.release_tag:
        raise ContractError("published release tag differs from frozen tag")
    if metadata.get("isDraft") is not False:
        raise ContractError("published release must not be a draft")
    if metadata.get("isPrerelease") not in {None, False}:
        raise ContractError("published release must not be a prerelease")
    records = metadata.get("assets")
    if not isinstance(records, list) or any(not isinstance(item, Mapping) for item in records):
        raise ContractError("GitHub release assets must be an array of objects")
    by_name: dict[str, Mapping[str, Any]] = {}
    for item in records:
        name = item.get("name")
        if not isinstance(name, str) or name in by_name:
            raise ContractError("GitHub release assets contain an invalid or duplicate name")
        by_name[name] = item

    expected = {path.name: path for path in bundle.assets}
    if set(by_name) != set(expected):
        raise ContractError("published release asset set differs from frozen asset set")
    downloaded_dir = Path(downloaded_dir).expanduser().absolute()
    verified: dict[str, str] = {}
    for name, source in expected.items():
        expected_digest = file_sha256(source)
        expected_size = source.stat().st_size
        record = by_name[name]
        if record.get("size") != expected_size:
            raise IntegrityError(f"published release asset size differs: {name}")
        metadata_digest = record.get("digest")
        if metadata_digest is not None and metadata_digest != f"sha256:{expected_digest}":
            raise IntegrityError(f"published release metadata digest differs: {name}")
        downloaded = downloaded_dir / name
        if not downloaded.is_file() or downloaded.is_symlink():
            raise IntegrityError(f"downloaded release asset is missing or unsafe: {name}")
        verify_sha256(downloaded, expected_digest)
        verified[name] = expected_digest
    return verified
