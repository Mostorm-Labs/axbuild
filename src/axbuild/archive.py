"""Integrity helpers and safe archive extraction."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile

from .errors import IntegrityError

_WINDOWS_DRIVE = re.compile(r"^[A-Za-z]:")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_sha256(path: Path, expected: str) -> None:
    actual = file_sha256(path)
    normalized = expected.lower()
    if actual != normalized:
        raise IntegrityError(
            f"SHA256 mismatch for {path}: expected={normalized} actual={actual}"
        )


def _zip_entry_is_symlink(info: zipfile.ZipInfo) -> bool:
    if info.create_system != 3:
        return False
    mode = (info.external_attr >> 16) & 0xFFFF
    return stat.S_ISLNK(mode)


def _safe_member_path(name: str, destination: Path) -> Path:
    if not name or "\x00" in name:
        raise IntegrityError(f"unsafe archive path: {name!r}")
    normalized = name.replace("\\", "/")
    if normalized.startswith("/") or _WINDOWS_DRIVE.match(normalized):
        raise IntegrityError(f"unsafe archive path: {name!r}")
    pure = PurePosixPath(normalized)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        raise IntegrityError(f"unsafe archive path: {name!r}")
    target = destination.joinpath(*pure.parts)
    root = destination.resolve()
    resolved_parent = target.parent.resolve()
    try:
        resolved_parent.relative_to(root)
    except ValueError as exc:
        raise IntegrityError(f"unsafe archive path: {name!r}") from exc
    return target


def extract_zip_safe(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "r") as zf:
        planned: list[tuple[zipfile.ZipInfo, Path]] = []
        for info in zf.infolist():
            if _zip_entry_is_symlink(info):
                raise IntegrityError(f"archive contains symlink entry: {info.filename}")
            target = _safe_member_path(info.filename.rstrip("/"), destination)
            planned.append((info, target))

        for info, target in planned:
            if info.is_dir() or info.filename.endswith("/"):
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info, "r") as source, target.open("wb") as output:
                while chunk := source.read(1024 * 1024):
                    output.write(chunk)
            if os.name != "nt":
                mode = (info.external_attr >> 16) & 0o777
                if mode:
                    target.chmod(mode)
