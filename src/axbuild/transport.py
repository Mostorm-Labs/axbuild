"""Verified transport for release indexes and artifact archives."""
from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import shutil
import tempfile
import urllib.error
import urllib.parse
import urllib.request

from .archive import verify_sha256
from .errors import AxBuildError, OfflineError, TransportError
from .model import ArtifactRef, ReleaseIndexRef

ReleaseRef = ArtifactRef | ReleaseIndexRef
MAX_DOWNLOAD_BYTES = 2 * 1024**3


@dataclass(frozen=True)
class ReleaseFile:
    path: Path
    source: str
    network_used: bool


def redirect_is_safe(old_url: str, new_url: str) -> bool:
    old = urllib.parse.urlsplit(old_url)
    new = urllib.parse.urlsplit(new_url)
    if new.scheme not in {"http", "https"}:
        return False
    if old.scheme == "https" and new.scheme != "https":
        return False
    return True


class SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not redirect_is_safe(req.full_url, newurl):
            raise TransportError(f"unsafe redirect refused: {req.full_url} -> {newurl}")
        old = urllib.parse.urlsplit(req.full_url)
        new = urllib.parse.urlsplit(newurl)
        redirected = super().redirect_request(req, fp, code, msg, headers, newurl)
        if redirected is not None and (old.scheme, old.netloc) != (new.scheme, new.netloc):
            redirected.remove_header("Authorization")
            redirected.remove_header("Cookie")
        return redirected


def _open(request: urllib.request.Request):
    return urllib.request.build_opener(SafeRedirectHandler()).open(request, timeout=30)


def release_url(ref: ReleaseRef) -> str:
    tag = urllib.parse.quote(ref.release_tag, safe="")
    asset = urllib.parse.quote(ref.asset, safe="")
    return f"https://github.com/{ref.repository}/releases/download/{tag}/{asset}"


def _download(request: urllib.request.Request, destination: Path) -> None:
    total = 0
    with _open(request) as source, destination.open("wb") as target:
        while chunk := source.read(1024 * 1024):
            total += len(chunk)
            if total > MAX_DOWNLOAD_BYTES:
                raise TransportError("release file exceeds 2 GiB download limit")
            target.write(chunk)
        target.flush()
        os.fsync(target.fileno())


def _github_download(ref: ReleaseRef, destination: Path) -> None:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        _download(urllib.request.Request(release_url(ref)), destination)
        return

    api_root = f"https://api.github.com/repos/{ref.repository}/releases"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "AxBuild/0.1",
    }
    tag_url = api_root + "/tags/" + urllib.parse.quote(ref.release_tag, safe="")
    with _open(urllib.request.Request(tag_url, headers=headers)) as source:
        raw = source.read(5 * 1024 * 1024 + 1)
    if len(raw) > 5 * 1024 * 1024:
        raise TransportError("GitHub release metadata exceeds 5 MiB limit")
    try:
        metadata = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise TransportError("GitHub release metadata is not valid JSON") from exc
    matches = [asset for asset in metadata.get("assets", []) if asset.get("name") == ref.asset]
    if len(matches) != 1 or type(matches[0].get("id")) is not int or matches[0]["id"] <= 0:
        raise TransportError(f"locked GitHub release asset is missing or ambiguous: {ref.asset}")
    asset_headers = dict(headers)
    asset_headers["Accept"] = "application/octet-stream"
    _download(
        urllib.request.Request(f"{api_root}/assets/{matches[0]['id']}", headers=asset_headers),
        destination,
    )


def _mirror_download(ref: ReleaseRef, mirror: str, destination: Path) -> bool:
    parsed = urllib.parse.urlsplit(mirror)
    if parsed.scheme in {"http", "https"}:
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise TransportError("mirror URL must be a credential-free base URL")
        suffix = "/" + urllib.parse.quote(ref.release_tag, safe="") + "/" + urllib.parse.quote(ref.asset, safe="")
        try:
            _download(urllib.request.Request(mirror.rstrip("/") + suffix), destination)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                raise FileNotFoundError(ref.asset) from exc
            raise
        return True

    if parsed.scheme == "file":
        if parsed.netloc not in {"", "localhost"}:
            raise TransportError("file mirror must be local or localhost")
        root = Path(urllib.request.url2pathname(parsed.path))
    elif parsed.scheme and not (len(parsed.scheme) == 1 and len(mirror) > 2 and mirror[1] == ":"):
        raise TransportError(f"unsupported mirror scheme: {parsed.scheme}")
    else:
        root = Path(mirror).expanduser()
    source = root.joinpath(*ref.release_tag.split("/"), ref.asset)
    if not source.is_file():
        raise FileNotFoundError(source)
    shutil.copyfile(source, destination)
    return False


def ensure_release_file(
    ref: ReleaseRef,
    destination: Path,
    *,
    mirror: str | None = None,
    offline: bool = False,
) -> ReleaseFile:
    """Return exact verified bytes for a trusted release reference."""
    try:
        if destination.exists() or destination.is_symlink():
            verify_sha256(destination, ref.sha256)
            return ReleaseFile(destination, "store", False)
        if offline:
            raise OfflineError(f"offline resolution requires materialized release file: {ref.asset}")

        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            dir=destination.parent, prefix=".axbuild-transfer-", delete=False
        ) as temp:
            staging = Path(temp.name)
        try:
            source = "github"
            network_used = True
            if mirror is not None:
                try:
                    network_used = _mirror_download(ref, mirror, staging)
                    source = "mirror"
                except FileNotFoundError:
                    _github_download(ref, staging)
            else:
                _github_download(ref, staging)
            verify_sha256(staging, ref.sha256)
            staging.replace(destination)
            return ReleaseFile(destination, source, network_used)
        finally:
            staging.unlink(missing_ok=True)
    except (AxBuildError, FileNotFoundError):
        raise
    except (OSError, ValueError, urllib.error.URLError) as exc:
        raise TransportError(f"release transport failed for {ref.asset}: {exc}") from exc
