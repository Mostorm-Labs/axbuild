"""Qualification tooling for a local NearCast AirPlay artifact candidate."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import tempfile
from typing import Any, Mapping
import zipfile

from . import __version__
from .archive import extract_zip_safe, file_sha256, verify_sha256
from .contracts import validate_asset_name, validate_namespace, validate_sha256
from .errors import ContractError, IntegrityError

FAMILY = "nearcast-airplay"
TARGET = "windows-x64"
VARIANT = "release"
PACKAGE_CONTRACT = "nearcast-airplay-artifact-qualification-v1"
MANIFEST_FORMAT = "axbuild-nearcast-airplay-artifact-manifest-v1"
PROVENANCE_FORMAT = "axbuild-nearcast-airplay-provenance-v1"
REPORT_FORMAT = "axbuild-nearcast-airplay-qualification-report-v1"
ARCHIVE_NAME = "nearcast-airplay-runtime-windows-x64-release.zip"
MANIFEST_NAME = "nearcast-airplay-artifact-manifest.json"
PROVENANCE_NAME = "nearcast-airplay-provenance.json"
REPORT_NAME = "qualification-report.json"

REQUIRED_CLOSURE_PATHS = (
    "dnssd/Include/dns_sd.h",
    "bonjour/Bonjour64.msi",
    "webview2/build/native/include/WebView2.h",
)
GSTREAMER_LAYOUTS = (
    (
        "gstreamer/lib/pkgconfig/gstreamer-1.0.pc",
        "gstreamer/bin/gst-inspect-1.0.exe",
    ),
    (
        "gstreamer/1.0/msvc_x86_64/lib/pkgconfig/gstreamer-1.0.pc",
        "gstreamer/1.0/msvc_x86_64/bin/gst-inspect-1.0.exe",
    ),
)
VCPKG_ROOT_PREFIX = "vcpkg/installed/x64-windows/"
VCPKG_SENTINEL = VCPKG_ROOT_PREFIX + ".axbuild-present"


@dataclass(frozen=True)
class QualificationOutputs:
    output_dir: Path
    archive_path: Path
    manifest_path: Path
    provenance_path: Path
    report_path: Path
    artifact_identity: str
    archive_sha256: str


def _canonical(value: Any) -> bytes:
    try:
        return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ContractError(f"qualification inputs must be JSON-serializable: {exc}") from exc


def _inventory(root: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        if path.is_symlink():
            raise IntegrityError(f"candidate contains symlink: {path}")
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if not relative or PurePosixPath(relative).is_absolute() or "\\" in relative:
            raise IntegrityError(f"unsafe candidate path: {relative!r}")
        entries.append({"path": relative, "size": path.stat().st_size, "sha256": file_sha256(path)})
    return entries


def _validate_required_layout(entries: list[dict[str, Any]]) -> None:
    present = {item["path"] for item in entries}
    missing = [path for path in REQUIRED_CLOSURE_PATHS if path not in present]
    if not any(set(layout).issubset(present) for layout in GSTREAMER_LAYOUTS):
        missing.extend(GSTREAMER_LAYOUTS[0])
    if VCPKG_SENTINEL not in present and not any(path.startswith(VCPKG_ROOT_PREFIX) for path in present):
        missing.append(VCPKG_SENTINEL)
    if missing:
        raise IntegrityError("NearCast AirPlay closure missing required path(s): " + ", ".join(missing))


def _inputs(value: Mapping[str, Any] | None) -> dict[str, Any]:
    if value is None:
        value = {}
    if not isinstance(value, Mapping):
        raise ContractError("build inputs must be an object")
    result = json.loads(_canonical(dict(value)))
    result.setdefault("abi", {"arch": "x64", "platform": "windows"})
    result.setdefault("toolchain", {"compiler": "msvc"})
    return result


def artifact_identity(
    entries: list[Mapping[str, Any]],
    build_inputs: Mapping[str, Any] | None = None,
    *,
    package_contract: str = PACKAGE_CONTRACT,
) -> str:
    """Create an identity from canonical archive inventory and build inputs."""
    canonical_entries = sorted((dict(item) for item in entries), key=lambda item: item["path"])
    payload = {
        "packageContract": package_contract,
        "family": FAMILY,
        "target": TARGET,
        "variant": VARIANT,
        "buildInputs": _inputs(build_inputs),
        "files": canonical_entries,
    }
    digest = hashlib.sha256(_canonical(payload)).hexdigest()
    return f"nearcast-airplay-runtime-windows-x64-release-{digest[:16]}"


def _write_zip(root: Path, destination: Path, entries: list[dict[str, Any]]) -> None:
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for item in entries:
            info = zipfile.ZipInfo(item["path"])
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, (root / Path(item["path"])).read_bytes())


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def qualify_nearcast_airplay_artifact(
    source_archive: Path,
    output_dir: Path,
    *,
    build_inputs: Mapping[str, Any] | None = None,
    components: list[Mapping[str, Any]] | None = None,
    notices: str | None = None,
) -> QualificationOutputs:
    """Qualify an explicit local closure archive without publishing it."""
    source_archive = Path(source_archive).expanduser().absolute()
    output_dir = Path(output_dir).expanduser().absolute()
    if not source_archive.is_file() or source_archive.is_symlink():
        raise IntegrityError(f"source archive must be a real file: {source_archive}")
    inputs = _inputs(build_inputs)
    source_sha = file_sha256(source_archive)
    source_size = source_archive.stat().st_size
    with tempfile.TemporaryDirectory(prefix="axbuild-qualify-") as temporary:
        extracted = Path(temporary) / "closure"
        with zipfile.ZipFile(source_archive, "r") as archive:
            names = [info.filename for info in archive.infolist() if not info.is_dir()]
        if len(names) != len(set(names)):
            raise IntegrityError("source archive contains duplicate file entries")
        extract_zip_safe(source_archive, extracted)
        entries = _inventory(extracted)
        _validate_required_layout(entries)
        identity = artifact_identity(entries, inputs)
        output_dir.mkdir(parents=True, exist_ok=True)
        archive_path = output_dir / ARCHIVE_NAME
        manifest_path = output_dir / MANIFEST_NAME
        provenance_path = output_dir / PROVENANCE_NAME
        report_path = output_dir / REPORT_NAME
        with tempfile.NamedTemporaryFile(dir=output_dir, prefix=".axbuild-qualify-", suffix=".zip", delete=False) as handle:
            temporary_archive = Path(handle.name)
        try:
            _write_zip(extracted, temporary_archive, entries)
            temporary_archive.replace(archive_path)
        finally:
            temporary_archive.unlink(missing_ok=True)

    archive_sha = file_sha256(archive_path)
    artifact = {
        "family": FAMILY,
        "target": TARGET,
        "variant": VARIANT,
        "artifactIdentity": identity,
        "asset": ARCHIVE_NAME,
        "size": archive_path.stat().st_size,
        "sha256": archive_sha,
    }
    manifest = {
        "format": MANIFEST_FORMAT,
        "family": FAMILY,
        "target": TARGET,
        "variant": VARIANT,
        "artifactIdentity": identity,
        "files": entries,
    }
    components_value = components
    if components_value is None:
        components_value = [
            {"name": name, "source": "closure-input", "version": "unspecified"}
            for name in sorted({item["path"].split("/", 1)[0] for item in entries})
        ]
    if not isinstance(components_value, list) or any(not isinstance(item, Mapping) for item in components_value):
        raise ContractError("components must be an array of objects")
    if notices is None:
        notices = "Redistribution review required before external publication."
    if not isinstance(notices, str):
        raise ContractError("notices must be a string")
    provenance = {
        "format": PROVENANCE_FORMAT,
        "family": FAMILY,
        "packageContract": PACKAGE_CONTRACT,
        "artifactIdentity": identity,
        "sourceArchive": {"fileName": source_archive.name, "size": source_size, "sha256": source_sha},
        "components": components_value,
        "buildInputs": inputs,
        "redistribution": {"status": "review-required", "notes": notices},
    }
    _write_json(manifest_path, manifest)
    _write_json(provenance_path, provenance)
    loaded_manifest = load_artifact_manifest(manifest_path)
    loaded_provenance = load_provenance(provenance_path)
    if loaded_provenance["artifactIdentity"] != loaded_manifest["artifactIdentity"]:
        raise ContractError("provenance artifact identity differs from manifest")
    with zipfile.ZipFile(archive_path, "r") as archive:
        archive_names = [info.filename for info in archive.infolist()]
        if archive_names != [item["path"] for item in loaded_manifest["files"]]:
            raise IntegrityError("artifact manifest does not match archive entries")
    verify_sha256(archive_path, archive_sha)
    validation_results = {
        "manifest": {"status": "pass", "detail": "manifest matches deterministic archive inventory"},
        "provenance": {"status": "pass", "detail": "provenance identity matches manifest"},
        "archive": {"status": "pass", "detail": "archive SHA256 verified"},
    }
    report = {
        "format": REPORT_FORMAT,
        "artifactIdentity": identity,
        "artifactSha256": archive_sha,
        "validationResults": validation_results,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "toolVersion": f"axbuild/{__version__}",
    }
    _write_json(report_path, report)
    return QualificationOutputs(output_dir, archive_path, manifest_path, provenance_path, report_path, identity, archive_sha)


def load_artifact_manifest(path: Path) -> dict[str, Any]:
    value = _load_object(path, "artifact manifest")
    required = {"format", "family", "target", "variant", "artifactIdentity", "files"}
    _strict_keys(value, required, "artifact manifest")
    if value["format"] != MANIFEST_FORMAT:
        raise ContractError(f"artifact manifest format must be {MANIFEST_FORMAT}")
    if value["family"] != FAMILY or value["target"] != TARGET or value["variant"] != VARIANT:
        raise ContractError("artifact manifest family/target/variant mismatch")
    validate_namespace(value["artifactIdentity"])
    files = value["files"]
    if not isinstance(files, list) or not files:
        raise ContractError("artifact manifest.files must be a non-empty array")
    seen: set[str] = set()
    for item in files:
        if not isinstance(item, dict):
            raise ContractError("artifact manifest file entry must be an object")
        _strict_keys(item, {"path", "size", "sha256"}, "artifact manifest file")
        path_value = item["path"]
        if not isinstance(path_value, str) or not path_value or "\\" in path_value or "\x00" in path_value or PurePosixPath(path_value).is_absolute():
            raise ContractError(f"unsafe artifact manifest path: {path_value!r}")
        if path_value in seen:
            raise ContractError(f"duplicate artifact manifest path: {path_value}")
        seen.add(path_value)
        if type(item["size"]) is not int or item["size"] < 0:
            raise ContractError("artifact manifest file size must be non-negative")
        validate_sha256(item["sha256"])
    return value


def load_provenance(path: Path) -> dict[str, Any]:
    value = _load_object(path, "provenance")
    required = {"format", "family", "packageContract", "artifactIdentity", "sourceArchive", "components", "buildInputs", "redistribution"}
    _strict_keys(value, required, "provenance")
    if value["format"] != PROVENANCE_FORMAT or value["family"] != FAMILY:
        raise ContractError("provenance format/family mismatch")
    validate_namespace(value["artifactIdentity"])
    source = value["sourceArchive"]
    if not isinstance(source, dict):
        raise ContractError("provenance.sourceArchive must be an object")
    _strict_keys(source, {"fileName", "size", "sha256"}, "provenance sourceArchive")
    validate_asset_name(source["fileName"])
    if type(source["size"]) is not int or source["size"] < 0:
        raise ContractError("provenance sourceArchive size must be non-negative")
    validate_sha256(source["sha256"])
    if not isinstance(value["components"], list) or any(not isinstance(item, dict) for item in value["components"]):
        raise ContractError("provenance.components must be an array of objects")
    redistribution = value["redistribution"]
    if not isinstance(redistribution, dict) or redistribution.get("status") != "review-required" or not isinstance(redistribution.get("notes"), str):
        raise ContractError("provenance redistribution must remain review-required")
    return value


def load_qualification_report(path: Path) -> dict[str, Any]:
    value = _load_object(path, "qualification report")
    required = {"format", "artifactIdentity", "artifactSha256", "validationResults", "timestamp", "toolVersion"}
    _strict_keys(value, required, "qualification report")
    if value["format"] != REPORT_FORMAT:
        raise ContractError(f"qualification report format must be {REPORT_FORMAT}")
    validate_namespace(value["artifactIdentity"])
    validate_sha256(value["artifactSha256"])
    if not isinstance(value["validationResults"], dict) or not value["validationResults"]:
        raise ContractError("qualification report.validationResults must be an object")
    for name, item in value["validationResults"].items():
        if not isinstance(name, str) or not isinstance(item, dict) or item.get("status") != "pass":
            raise ContractError(f"qualification result is not passing: {name}")
    for field in ("timestamp", "toolVersion"):
        if not isinstance(value[field], str) or not value[field]:
            raise ContractError(f"qualification report.{field} must be a non-empty string")
    return value


def _load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"invalid {label} JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError(f"{label} root must be an object")
    return value


def _strict_keys(value: dict[str, Any], required: set[str], label: str) -> None:
    missing = sorted(required - value.keys())
    unknown = sorted(value.keys() - required)
    if missing:
        raise ContractError(f"{label} missing required field(s): {', '.join(missing)}")
    if unknown:
        raise ContractError(f"{label} contains unknown field(s): {', '.join(unknown)}")
