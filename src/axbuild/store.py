"""Persistent content-addressed Store for verified AxBuild artifacts."""
from __future__ import annotations

from contextlib import contextmanager
import errno
import hashlib
import os
from pathlib import Path
import shutil
import tempfile
import time
from typing import Callable, Iterator

from .archive import verify_sha256
from .errors import AxBuildError
from .model import ArtifactRef, ReleaseIndexRef


class SdkStore:
    def __init__(self, root: Path):
        self.root = root.expanduser().absolute()

    def _path(self, *parts: str) -> Path:
        path = self.root
        for part in parts:
            path = path / part
            if path.is_symlink():
                raise AxBuildError(f"store namespace contains symlink: {path}")
        return path

    def archive_path(self, ref: ArtifactRef | ReleaseIndexRef) -> Path:
        return self._path("archives", "sha256", ref.sha256, ref.asset)

    def package_path(self, ref: ArtifactRef) -> Path:
        return self._path("packages", ref.family, ref.kind, ref.identity)

    def release_index_path(self, ref: ReleaseIndexRef) -> Path:
        return self._path("release-sets", ref.family, ref.identity, ref.asset)

    @contextmanager
    def lock(self, key: str, *, timeout: float = 30.0) -> Iterator[None]:
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        path = self._path("locks", f"{digest}.lock")
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor = os.open(path, os.O_CREAT | os.O_RDWR, 0o600)
        acquired = False
        deadline = time.monotonic() + timeout
        try:
            while True:
                try:
                    os.lseek(descriptor, 0, os.SEEK_SET)
                    if os.name == "nt":
                        import msvcrt

                        msvcrt.locking(descriptor, msvcrt.LK_NBLCK, 1)
                    else:
                        import fcntl

                        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    acquired = True
                    break
                except OSError as exc:
                    if exc.errno not in {errno.EACCES, errno.EAGAIN, errno.EDEADLK}:
                        raise
                    if time.monotonic() >= deadline:
                        raise AxBuildError(f"store lock timed out: {key}") from exc
                    time.sleep(0.05)
            yield
        finally:
            if acquired:
                os.lseek(descriptor, 0, os.SEEK_SET)
                if os.name == "nt":
                    import msvcrt

                    msvcrt.locking(descriptor, msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(descriptor, fcntl.LOCK_UN)
            os.close(descriptor)

    def materialize_package(
        self,
        ref: ArtifactRef,
        archive: Path,
        installer: Callable[[Path, Path], None],
        validator: Callable[[Path], None],
    ) -> Path:
        with self.lock(f"package:{ref.family}:{ref.kind}:{ref.identity}"):
            destination = self.package_path(ref)
            if destination.exists():
                validator(destination)
                return destination

            verify_sha256(archive, ref.sha256)
            destination.parent.mkdir(parents=True, exist_ok=True)
            staging = Path(
                tempfile.mkdtemp(prefix=".axbuild-staging-", dir=destination.parent)
            )
            try:
                installer(archive, staging)
                validator(staging)
                if destination.exists():
                    validator(destination)
                    return destination
                staging.rename(destination)
                return destination
            finally:
                if staging.exists():
                    shutil.rmtree(staging)
