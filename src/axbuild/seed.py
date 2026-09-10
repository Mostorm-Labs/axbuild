"""Deterministic tooling for the NearCast AirPlay seed package.

The producer is intentionally separate from the family-neutral resolver.  It
turns an already materialized dependency closure into reviewable metadata and
release bytes; it does not publish those bytes or alter a consumer lock.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import tempfile
from typing import Any, Mapping
import zipfile

from .archive import file_sha256
from .contracts import (
    validate_asset_name,
    validate_namespace,
    validate_repository,
    validate_sha256,
)
from .errors import ContractError, IntegrityError

NEARCAST_AIRPLAY_FAMILY = "nearcast-airplay"
SEED_PACKAGE_FORMAT = "axbuild-nearcast-airplay-seed-v1"
PROVENANCE_FORMAT = "axbuild-nearcast-airplay-provenance-v1"
PACKAGE_CONTRACT = "nearcast-airplay-seed-v1"
DEFAULT_REPOSITORY = "Mostorm-Labs/axbuild"
DEFAULT_TARGET = "windows-x64"
DEFAULT_VARIANT = "release"
ARCHIVE_ASSET = "nearcast-airplay-runtime-windows-x64-release.zip"
INDEX_ASSET = "nearcast-airplay-sdk-index.json"
PROVENANCE_ASSET = "nearcast-airplay-provenance.json"
LOCK_ASSET = "nearcast-airplay-sdk.lock.json"

REQUIRED_CLOSURE_PATHS = (
    "gstreamer/lib/pkgconfig/gstreamer-1.0.pc",
    "gstreamer/bin/gst-inspect-1.0.exe",
    "dnssd/Include/dns_sd.h",
    "bonjour/Bonjour64.msi",
    "webview2/build/native/include/WebView2.h",
    "vcpkg/installed/x64-windows/.axbuild-present",
)


@dataclass(frozen=True)
class SeedOutputs:
    output_dir: Path
    mirror_root: Path
    family: str
    release_set_id: str
    release_tag: str
    artifact_identity: str
    artifact_sha256: str
    index_sha256: str
    archive_path: Path
    index_path: Path
    provenance_path: Path
    lock_path: Path


def _canonical_json(value: Any) -> bytes:
    try:
        return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ContractError(f"seed inputs must be JSON-serializable: {exc}") from exc


def _inventory(source_root: Path) -> list[dict[str, Any]]:
    source_root = source_root.expanduser().absolute()
    if not source_root.is_dir() or source_root.is_symlink():
        raise IntegrityError(f"seed source must be a real directory: {source_root}")
    entries: list[dict[str, Any]] = []
    for path in sorted(source_root.rglob("*"), key=lambda item: item.as_posix()):
        if path.is_symlink():
            raise IntegrityError(f"seed source contains symlink: {path}")
        if not path.is_file():
            continue
        relative = path.relative_to(source_root).as_posix()
        if not relative or PurePosixPath(relative).is_absolute():
            raise IntegrityError(f"unsafe seed source path: {relative!r}")
        entries.append({"path": relative, "size": path.stat().st_size, "sha256": file_sha256(path)})
    return entries


def _validate_closure(inventory: list[dict[str, Any]]) -> None:
    names = {entry["path"] for entry in inventory}
    missing = [path for path in REQUIRED_CLOSURE_PATHS if path not in names]
    if missing:
        raise IntegrityError("NearCast AirPlay closure missing required path(s): " + ", ".join(missing))


def _normalized_inputs(build_inputs: Mapping[str, Any] | None) -> dict[str, Any]:
    if build_inputs is None:
        build_inputs = {}
    if not isinstance(build_inputs, Mapping):
        raise ContractError("seed build inputs must be an object")
    normalized = json.loads(_canonical_json(dict(build_inputs)))
    if not isinstance(normalized, dict):
        raise ContractError("seed build inputs must be an object")
    normalized.setdefault("target", DEFAULT_TARGET)
    normalized.setdefault("variant", DEFAULT_VARIANT)
    normalized.setdefault("abi", {"arch": "x64", "platform": "windows"})
    normalized.setdefault("toolchain", {"compiler": "msvc"})
    return normalized


def seed_artifact_identity(
    source_root: Path,
    build_inputs: Mapping[str, Any] | None = None,
    *,
    package_contract: str = PACKAGE_CONTRACT,
) -> str:
    """Return an identity derived from source bytes and build-contract inputs."""
    inventory = _inventory(source_root)
    payload = {
        "packageContract": package_contract,
        "family": NEARCAST_AIRPLAY_FAMILY,
        "kind": "runtime",
        "key": DEFAULT_TARGET,
        "variant": DEFAULT_VARIANT,
        "buildInputs": _normalized_inputs(build_inputs),
        "files": inventory,
    }
    digest = hashlib.sha256(_canonical_json(payload)).hexdigest()
    return f"nearcast-airplay-runtime-windows-x64-release-{digest[:16]}"


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_deterministic_zip(source_root: Path, destination: Path, inventory: list[dict[str, Any]]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for entry in inventory:
            source = source_root / Path(entry["path"])
            info = zipfile.ZipInfo(entry["path"])
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            with source.open("rb") as handle:
                archive.writestr(info, handle.read())


def build_nearcast_airplay_seed(
    source_root: Path,
    output_dir: Path,
    *,
    repository: str = DEFAULT_REPOSITORY,
    release_tag: str | None = None,
    release_set_id: str | None = None,
    build_inputs: Mapping[str, Any] | None = None,
    components: list[Mapping[str, Any]] | None = None,
    notices: str | None = None,
) -> SeedOutputs:
    """Materialize a candidate seed release locally.

    The output directory is also a local mirror root: ``<tag>/<asset>`` is
    populated so the ordinary AxBuild resolver can qualify the candidate.
    """
    repository = validate_repository(repository)
    source_root = Path(source_root).expanduser().absolute()
    output_dir = Path(output_dir).expanduser().absolute()
    inputs = _normalized_inputs(build_inputs)
    inventory = _inventory(source_root)
    _validate_closure(inventory)
    identity = seed_artifact_identity(source_root, inputs)
    suffix = identity.rsplit("-", 1)[-1]
    release_set_id = validate_namespace(release_set_id or f"nearcast-airplay-v1-{suffix}")
    release_tag = validate_namespace(release_tag or f"nearcast-airplay-sdk-v1-{suffix}")
    components_value = components if components is not None else [
        {"name": name, "source": "closure-input", "version": "unspecified"}
        for name in sorted({path.split("/", 1)[0] for path in (entry["path"] for entry in inventory)})
    ]
    if not isinstance(components_value, list) or any(not isinstance(item, Mapping) for item in components_value):
        raise ContractError("seed components must be an array of objects")
    notices_value = notices if notices is not None else "Redistribution review required before external publication."
    if not isinstance(notices_value, str):
        raise ContractError("seed notices must be a string")

    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / ARCHIVE_ASSET
    index_path = output_dir / INDEX_ASSET
    provenance_path = output_dir / PROVENANCE_ASSET
    lock_path = output_dir / LOCK_ASSET
    release_dir = output_dir / release_tag
    release_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(dir=output_dir, prefix=".axbuild-seed-", suffix=".zip", delete=False) as temp:
        temporary_archive = Path(temp.name)
    try:
        _write_deterministic_zip(source_root, temporary_archive, inventory)
        temporary_archive.replace(archive_path)
    finally:
        temporary_archive.unlink(missing_ok=True)

    artifact_sha = file_sha256(archive_path)
    artifact_size = archive_path.stat().st_size
    artifact_metadata = {
        "packageContract": PACKAGE_CONTRACT,
        "target": DEFAULT_TARGET,
        "variant": DEFAULT_VARIANT,
        "abi": inputs["abi"],
        "toolchain": inputs["toolchain"],
        "provenanceAsset": PROVENANCE_ASSET,
    }
    index = {
        "format": "axbuild-release-index-v1",
        "family": NEARCAST_AIRPLAY_FAMILY,
        "releaseSetId": release_set_id,
        "artifacts": [{
            "kind": "runtime",
            "key": DEFAULT_TARGET,
            "identity": identity,
            "asset": ARCHIVE_ASSET,
            "sha256": artifact_sha,
            "size": artifact_size,
            "metadata": artifact_metadata,
        }],
    }
    _write_json(index_path, index)
    index_sha = file_sha256(index_path)
    lock = {
        "format": "axbuild-sdk-lock-v1",
        "family": NEARCAST_AIRPLAY_FAMILY,
        "repository": repository,
        "releaseTag": release_tag,
        "releaseSetId": release_set_id,
        "indexAsset": INDEX_ASSET,
        "indexSha256": index_sha,
    }
    _write_json(lock_path, lock)
    provenance = {
        "format": PROVENANCE_FORMAT,
        "family": NEARCAST_AIRPLAY_FAMILY,
        "packageContract": PACKAGE_CONTRACT,
        "target": DEFAULT_TARGET,
        "variant": DEFAULT_VARIANT,
        "artifact": {
            "kind": "runtime",
            "key": DEFAULT_TARGET,
            "identity": identity,
            "asset": ARCHIVE_ASSET,
            "sha256": artifact_sha,
            "size": artifact_size,
        },
        "release": {
            "repository": repository,
            "releaseTag": release_tag,
            "releaseSetId": release_set_id,
            "indexAsset": INDEX_ASSET,
            "indexSha256": index_sha,
        },
        "source": {"files": inventory},
        "buildInputs": inputs,
        "components": components_value,
        "redistribution": {"status": "review-required", "notes": notices_value},
    }
    _write_json(provenance_path, provenance)

    for asset in (archive_path, index_path):
        shutil.copyfile(asset, release_dir / asset.name)
    return SeedOutputs(
        output_dir,
        output_dir,
        NEARCAST_AIRPLAY_FAMILY,
        release_set_id,
        release_tag,
        identity,
        artifact_sha,
        index_sha,
        archive_path,
        index_path,
        provenance_path,
        lock_path,
    )


def load_provenance(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"invalid provenance JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError("provenance root must be an object")
    required = {
        "format", "family", "packageContract", "target", "variant", "artifact",
        "release", "source", "buildInputs", "components", "redistribution",
    }
    unknown = sorted(value.keys() - required)
    missing = sorted(required - value.keys())
    if unknown:
        raise ContractError("provenance contains unknown field(s): " + ", ".join(unknown))
    if missing:
        raise ContractError("provenance missing required field(s): " + ", ".join(missing))
    if value["format"] != PROVENANCE_FORMAT:
        raise ContractError(f"provenance format must be {PROVENANCE_FORMAT}")
    if value["family"] != NEARCAST_AIRPLAY_FAMILY:
        raise ContractError("provenance family must be nearcast-airplay")
    for field in ("packageContract", "target", "variant"):
        if not isinstance(value[field], str) or not value[field]:
            raise ContractError(f"provenance.{field} must be a non-empty string")
    artifact = value["artifact"]
    release = value["release"]
    if not isinstance(artifact, dict) or not isinstance(release, dict):
        raise ContractError("provenance artifact and release must be objects")
    for field in ("identity", "asset", "sha256"):
        if not isinstance(artifact.get(field), str) or not artifact[field]:
            raise ContractError(f"provenance.artifact.{field} must be a non-empty string")
    validate_namespace(artifact["identity"])
    validate_asset_name(artifact["asset"])
    validate_sha256(artifact["sha256"])
    validate_repository(release.get("repository"))
    validate_namespace(release.get("releaseSetId"))
    validate_sha256(release.get("indexSha256"))
    if not isinstance(value["source"], dict) or not isinstance(value["source"].get("files"), list):
        raise ContractError("provenance.source.files must be an array")
    if not isinstance(value["components"], list) or any(not isinstance(item, dict) for item in value["components"]):
        raise ContractError("provenance.components must be an array of objects")
    redistribution = value["redistribution"]
    if not isinstance(redistribution, dict) or not isinstance(redistribution.get("status"), str):
        raise ContractError("provenance.redistribution.status must be a string")
    return value
