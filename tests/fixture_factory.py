from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import zipfile

from axbuild.archive import file_sha256


@dataclass(frozen=True)
class FixtureLayout:
    repo_root: Path
    mirror_root: Path
    store_root: Path
    lock_path: Path


def _write_zip(path: Path, files: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as zf:
        for name, content in sorted(files.items()):
            zf.writestr(name, content)


def _write_release(
    tmp_path: Path,
    *,
    family: str,
    tag: str,
    release_set_id: str,
    artifacts: list[dict],
) -> FixtureLayout:
    repo_root = tmp_path / "repo"
    mirror_root = tmp_path / "mirror"
    store_root = tmp_path / "store"
    repo_root.mkdir(parents=True, exist_ok=True)
    index = {
        "format": "axbuild-release-index-v1",
        "family": family,
        "releaseSetId": release_set_id,
        "artifacts": artifacts,
    }
    index_asset = f"{family}-index.json"
    index_path = mirror_root / tag / index_asset
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lock = {
        "format": "axbuild-sdk-lock-v1",
        "family": family,
        "repository": "Mostorm-Labs/fixture-dependencies",
        "releaseTag": tag,
        "releaseSetId": release_set_id,
        "indexAsset": index_asset,
        "indexSha256": file_sha256(index_path),
    }
    lock_path = repo_root / f"{family}-sdk.lock.json"
    lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return FixtureLayout(repo_root, mirror_root, store_root, lock_path)


def create_axiom_like_fixture(tmp_path: Path) -> FixtureLayout:
    family = "axiom-like"
    tag = "axiom-like-sdk-v1"
    mirror = tmp_path / "mirror" / tag
    host = mirror / "axiom-host-linux-x86_64.zip"
    runtime = mirror / "axiom-runtime-windows-x64.zip"
    _write_zip(host, {"bin/protoc": "synthetic-host-tool"})
    _write_zip(runtime, {"lib/cmake/semantic/semantic-config.cmake": "# synthetic runtime"})
    artifacts = [
        {
            "kind": "host-tools",
            "key": "linux-x86_64",
            "identity": "host-linux-1",
            "asset": host.name,
            "sha256": file_sha256(host),
            "size": host.stat().st_size,
            "metadata": {"executable": "bin/protoc"},
        },
        {
            "kind": "runtime",
            "key": "windows-x64-msvc-static",
            "identity": "runtime-win-1",
            "asset": runtime.name,
            "sha256": file_sha256(runtime),
            "size": runtime.stat().st_size,
            "metadata": {"abi": {"arch": "x64", "linkage": "static", "crt": "static-release"}},
        },
    ]
    return _write_release(
        tmp_path,
        family=family,
        tag=tag,
        release_set_id="axiom-set-1",
        artifacts=artifacts,
    )


def create_nearcast_like_fixture(tmp_path: Path, *, complete: bool) -> FixtureLayout:
    family = "nearcast-like"
    tag = "nearcast-airplay-sdk-v1"
    mirror = tmp_path / "mirror" / tag
    runtime = mirror / "nearcast-airplay-windows-x64.zip"
    files = {
        "gstreamer/lib/pkgconfig/gstreamer-1.0.pc": "prefix=/synthetic",
        "gstreamer/bin/gst-inspect-1.0.exe": "synthetic-executable",
        "bonjour/Bonjour64.msi": "synthetic-msi",
        "webview2/build/native/include/WebView2.h": "// synthetic header",
        "vcpkg/installed/x64-windows/.axbuild-present": "present",
    }
    if complete:
        files["dnssd/Include/dns_sd.h"] = "// synthetic dns-sd header"
    _write_zip(runtime, files)
    artifacts = [
        {
            "kind": "runtime",
            "key": "windows-x64",
            "identity": "airplay-runtime-win-1",
            "asset": runtime.name,
            "sha256": file_sha256(runtime),
            "size": runtime.stat().st_size,
            "metadata": {"closure": ["gstreamer", "vcpkg", "dnssd", "bonjour", "webview2"]},
        }
    ]
    return _write_release(
        tmp_path,
        family=family,
        tag=tag,
        release_set_id="nearcast-set-1",
        artifacts=artifacts,
    )
