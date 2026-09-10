"""Synthetic provider shaped like NearCast's prebuilt AirPlay dependency closure."""
from __future__ import annotations

from pathlib import Path

from axbuild.archive import extract_zip_safe
from axbuild.contracts import load_sdk_lock
from axbuild.errors import ContractError, IntegrityError
from axbuild.model import ArtifactRef, MaterializedArtifact, ProviderPlan, ReleaseIndex, ReleaseIndexRef, ResolveRequest


class NearCastLikeProvider:
    family = "nearcast-like"

    def __init__(self, lock_path: Path):
        self.lock_path = Path(lock_path)

    def _authority(self) -> ReleaseIndexRef:
        ref = load_sdk_lock(self.lock_path)
        if ref.family != self.family:
            raise ContractError(f"NearCast-like lock family must be {self.family}")
        return ref

    def index_ref(self, request: ResolveRequest) -> ReleaseIndexRef:
        return self._authority()

    def plan(self, request: ResolveRequest, index: ReleaseIndex) -> ProviderPlan:
        authority = self._authority()
        try:
            record = index.artifact("runtime", request.target)
        except KeyError as exc:
            raise ContractError(f"NearCast-like target is unavailable: {request.target}") from exc
        ref = ArtifactRef(
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
            (ref,),
            {"dependencyShape": "prebuilt-closure", "target": request.target},
        )

    def install(self, ref: ArtifactRef, archive: Path, staging_root: Path) -> None:
        extract_zip_safe(archive, staging_root)

    def validate(self, ref: ArtifactRef, materialized_root: Path) -> None:
        required = {
            "gstreamer-pkgconfig": materialized_root / "gstreamer/lib/pkgconfig/gstreamer-1.0.pc",
            "gstreamer-inspect": materialized_root / "gstreamer/bin/gst-inspect-1.0.exe",
            "dnssd-header": materialized_root / "dnssd/Include/dns_sd.h",
            "bonjour-installer": materialized_root / "bonjour/Bonjour64.msi",
            "webview2-header": materialized_root / "webview2/build/native/include/WebView2.h",
            "vcpkg-root": materialized_root / "vcpkg/installed/x64-windows/.axbuild-present",
        }
        for label, path in required.items():
            if not path.is_file():
                raise IntegrityError(f"NearCast-like closure missing {label}: {path}")

    def environment(
        self,
        plan: ProviderPlan,
        materialized: tuple[MaterializedArtifact, ...],
    ) -> dict[str, str]:
        return {"NEARCAST_LIKE_AIRPLAY_ROOT": str(materialized[0].root)}
