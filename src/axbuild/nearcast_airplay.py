"""AxBuild provider for the qualified NearCast AirPlay dependency closure."""
from __future__ import annotations

from pathlib import Path

from .archive import extract_zip_safe
from .contracts import load_sdk_lock
from .errors import ContractError, IntegrityError
from .model import (
    ArtifactRef,
    MaterializedArtifact,
    ProviderPlan,
    ReleaseIndex,
    ReleaseIndexRef,
    ResolveRequest,
)


class NearCastAirPlayProvider:
    family = "nearcast-airplay"

    def __init__(self, lock_path: Path):
        self.lock_path = Path(lock_path)

    def _authority(self) -> ReleaseIndexRef:
        ref = load_sdk_lock(self.lock_path)
        if ref.family != self.family:
            raise ContractError(f"NearCast AirPlay lock family must be {self.family}")
        return ref

    def index_ref(self, request: ResolveRequest) -> ReleaseIndexRef:
        return self._authority()

    def plan(self, request: ResolveRequest, index: ReleaseIndex) -> ProviderPlan:
        if request.target != "windows-x64":
            raise ContractError(f"NearCast AirPlay target is unavailable: {request.target}")
        authority = self._authority()
        try:
            record = index.artifact("runtime", request.target)
        except KeyError as exc:
            raise ContractError(f"NearCast AirPlay target is unavailable: {request.target}") from exc
        if record.metadata.get("target") != request.target or record.metadata.get("variant") != "release":
            raise ContractError("NearCast AirPlay artifact metadata differs from requested target/variant")
        artifact = ArtifactRef(
            family=self.family,
            kind=record.kind,
            key=record.key,
            identity=record.identity,
            repository=authority.repository,
            release_tag=authority.release_tag,
            asset=record.asset,
            sha256=record.sha256,
            size=record.size,
            metadata=record.metadata,
        )
        return ProviderPlan(
            self.family,
            (artifact,),
            {"dependencyShape": "prebuilt-closure", "target": request.target},
        )

    def install(self, ref: ArtifactRef, archive: Path, staging_root: Path) -> None:
        extract_zip_safe(archive, staging_root)

    def validate(self, ref: ArtifactRef, materialized_root: Path) -> None:
        required = (
            materialized_root / "dnssd/Include/dns_sd.h",
            materialized_root / "bonjour/Bonjour64.msi",
            materialized_root / "webview2/build/native/include/WebView2.h",
        )
        for path in required:
            if not path.is_file():
                raise IntegrityError(f"NearCast AirPlay closure missing required path: {path}")
        gstreamer_layouts = (
            (
                materialized_root / "gstreamer/lib/pkgconfig/gstreamer-1.0.pc",
                materialized_root / "gstreamer/bin/gst-inspect-1.0.exe",
            ),
            (
                materialized_root / "gstreamer/1.0/msvc_x86_64/lib/pkgconfig/gstreamer-1.0.pc",
                materialized_root / "gstreamer/1.0/msvc_x86_64/bin/gst-inspect-1.0.exe",
            ),
        )
        if not any(all(path.is_file() for path in layout) for layout in gstreamer_layouts):
            raise IntegrityError("NearCast AirPlay closure is missing a supported GStreamer layout")
        vcpkg = materialized_root / "vcpkg/installed/x64-windows"
        if not vcpkg.is_dir() or not any(path.is_file() for path in vcpkg.rglob("*")):
            raise IntegrityError("NearCast AirPlay closure is missing the vcpkg x64-windows payload")

    def environment(
        self,
        plan: ProviderPlan,
        materialized: tuple[MaterializedArtifact, ...],
    ) -> dict[str, str]:
        return {"NEARCAST_AIRPLAY_ROOT": str(materialized[0].root)}
