"""Strict JSON contracts for AxBuild locks and release indexes."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .errors import ContractError
from .model import IndexedArtifact, ReleaseIndex, ReleaseIndexRef

_LOCK_FORMAT = "axbuild-sdk-lock-v1"
_INDEX_FORMAT = "axbuild-release-index-v1"
_SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")
_NAMESPACE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def _read_object(path: Path) -> dict[str, Any]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"invalid JSON contract: {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ContractError(f"contract root must be an object: {path}")
    return raw


def _require_exact_keys(obj: dict[str, Any], required: set[str], optional: set[str], label: str) -> None:
    missing = sorted(required - obj.keys())
    unknown = sorted(obj.keys() - required - optional)
    if missing:
        raise ContractError(f"{label} missing required field(s): {', '.join(missing)}")
    if unknown:
        raise ContractError(f"{label} contains unknown field(s): {', '.join(unknown)}")


def _require_string(obj: dict[str, Any], key: str, label: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value:
        raise ContractError(f"{label}.{key} must be a non-empty string")
    return value


def validate_namespace(value: str) -> str:
    if not isinstance(value, str) or not _NAMESPACE.fullmatch(value):
        raise ContractError(f"unsafe namespace component: {value!r}")
    return value


def validate_asset_name(value: str) -> str:
    value = validate_namespace_like_filename(value)
    if value in {".", ".."}:
        raise ContractError(f"unsafe asset name: {value!r}")
    return value


def validate_namespace_like_filename(value: str) -> str:
    if not isinstance(value, str) or not value or "/" in value or "\\" in value or "\x00" in value:
        raise ContractError(f"unsafe file name: {value!r}")
    return value


def validate_sha256(value: str) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        raise ContractError("SHA256 must contain exactly 64 hexadecimal characters")
    return value.lower()


def validate_repository(value: str) -> str:
    if not isinstance(value, str) or not _REPOSITORY.fullmatch(value):
        raise ContractError(f"repository must be owner/repo: {value!r}")
    return value


def validate_release_tag(value: str) -> str:
    if (
        not isinstance(value, str)
        or not value
        or value.startswith("/")
        or value.endswith("/")
        or "\\" in value
        or "\x00" in value
        or ":" in value
    ):
        raise ContractError(f"SDK lock.releaseTag is unsafe: {value!r}")
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ContractError(f"SDK lock.releaseTag is unsafe: {value!r}")
    return value


def load_sdk_lock(path: Path) -> ReleaseIndexRef:
    obj = _read_object(path)
    required = {"format", "family", "repository", "releaseTag", "releaseSetId", "indexAsset", "indexSha256"}
    _require_exact_keys(obj, required, set(), "SDK lock")
    if obj["format"] != _LOCK_FORMAT:
        raise ContractError(f"SDK lock format must be {_LOCK_FORMAT}")
    family = validate_namespace(_require_string(obj, "family", "SDK lock"))
    repository = validate_repository(_require_string(obj, "repository", "SDK lock"))
    release_tag = validate_release_tag(_require_string(obj, "releaseTag", "SDK lock"))
    release_set_id = validate_namespace(_require_string(obj, "releaseSetId", "SDK lock"))
    index_asset = validate_asset_name(_require_string(obj, "indexAsset", "SDK lock"))
    digest = validate_sha256(_require_string(obj, "indexSha256", "SDK lock"))
    return ReleaseIndexRef(family, release_set_id, repository, release_tag, index_asset, digest)


def load_release_index(path: Path) -> ReleaseIndex:
    obj = _read_object(path)
    required = {"format", "family", "releaseSetId", "artifacts"}
    _require_exact_keys(obj, required, set(), "release index")
    if obj["format"] != _INDEX_FORMAT:
        raise ContractError(f"release index format must be {_INDEX_FORMAT}")
    family = validate_namespace(_require_string(obj, "family", "release index"))
    release_set_id = validate_namespace(_require_string(obj, "releaseSetId", "release index"))
    records = obj["artifacts"]
    if not isinstance(records, list) or not records:
        raise ContractError("release index.artifacts must be a non-empty array")
    artifacts: list[IndexedArtifact] = []
    seen: set[tuple[str, str]] = set()
    required_artifact = {"kind", "key", "identity", "asset", "sha256"}
    optional_artifact = {"size", "metadata"}
    for position, record in enumerate(records):
        label = f"release index.artifacts[{position}]"
        if not isinstance(record, dict):
            raise ContractError(f"{label} must be an object")
        _require_exact_keys(record, required_artifact, optional_artifact, label)
        kind = validate_namespace(_require_string(record, "kind", label))
        key = validate_namespace(_require_string(record, "key", label))
        identity = validate_namespace(_require_string(record, "identity", label))
        asset = validate_asset_name(_require_string(record, "asset", label))
        digest = validate_sha256(_require_string(record, "sha256", label))
        size = record.get("size")
        if size is not None and (type(size) is not int or size < 0):
            raise ContractError(f"{label}.size must be a non-negative integer")
        metadata = record.get("metadata", {})
        if not isinstance(metadata, dict):
            raise ContractError(f"{label}.metadata must be an object")
        pair = (kind, key)
        if pair in seen:
            raise ContractError(f"duplicate artifact kind/key: {kind}/{key}")
        seen.add(pair)
        artifacts.append(IndexedArtifact(kind, key, identity, asset, digest, size, metadata))
    return ReleaseIndex(family, release_set_id, tuple(artifacts))
