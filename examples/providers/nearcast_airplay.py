"""Project-owned provider used to qualify the NearCast AirPlay seed candidate."""
from __future__ import annotations

from pathlib import Path

from axbuild.archive import extract_zip_safe
from axbuild.contracts import load_sdk_lock
from axbuild.errors import ContractError, IntegrityError
from axbuild.model import ArtifactRef, MaterializedArtifact, ProviderPlan, ReleaseIndex, ReleaseIndexRef, ResolveRequest
from axbuild.seed import load_provenance


class NearCastAirPlayProvider:
    family = "nearcast-airplay"

    def __init__(self, lock_path: Path, provenance_path: Path | None = None):
        self.lock_path = Path(lock_path)
        self.provenance_path = Path(provenance_path) if provenance_path is not None else None

    def _authority(self) -> ReleaseIndexRef:
        ref = load_sdk_lock(self.lock_path)
        if ref.family != self.family:
            raise ContractError(f"NearCast AirPlay lock family must be {self.family}")
        return ref

    def index_ref(self, request: ResolveRequest) -> ReleaseIndexRef:
        return self._authority()

    def plan(self, request: ResolveRequest, index: ReleaseIndex) -> ProviderPlan:
        authority = self._authority()
        try:
            record = index.artifact("runtime", request.target)
        except KeyError as exc:
            raise ContractError(f"NearCast AirPlay target is unavailable: {request.target}") from exc
        if self.provenance_path is not None:
            provenance = load_provenance(self.provenance_path)
            artifact = provenance["artifact"]
            release = provenance["release"]
            if (
                release["repository"] != authority.repository
                or release["releaseTag"] != authority.release_tag
                or release["releaseSetId"] != authority.identity
                or artifact["identity"] != record.identity
                or artifact["asset"] != record.asset
                or artifact["sha256"].lower() != record.sha256.lower()
            ):
                raise ContractError("NearCast AirPlay provenance differs from lock/index authority")
        return ProviderPlan(
            self.family,
            (ArtifactRef(
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
            ),),
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
                raise IntegrityError(f"NearCast AirPlay closure missing {label}: {path}")

    def environment(
        self,
        plan: ProviderPlan,
        materialized: tuple[MaterializedArtifact, ...],
    ) -> dict[str, str]:
        return {"NEARCAST_AIRPLAY_ROOT": str(materialized[0].root)}
