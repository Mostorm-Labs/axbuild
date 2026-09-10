"""Synthetic provider shaped like Axiom's host-tool + target-runtime SDK."""
from __future__ import annotations

from pathlib import Path

from axbuild.archive import extract_zip_safe
from axbuild.contracts import load_sdk_lock
from axbuild.errors import ContractError, IntegrityError
from axbuild.model import ArtifactRef, MaterializedArtifact, ProviderPlan, ReleaseIndex, ReleaseIndexRef, ResolveRequest


class AxiomLikeProvider:
    family = "axiom-like"

    def __init__(self, lock_path: Path, *, host_key: str):
        self.lock_path = Path(lock_path)
        self.host_key = host_key

    def _authority(self) -> ReleaseIndexRef:
        ref = load_sdk_lock(self.lock_path)
        if ref.family != self.family:
            raise ContractError(f"Axiom-like lock family must be {self.family}")
        return ref

    def index_ref(self, request: ResolveRequest) -> ReleaseIndexRef:
        return self._authority()

    def _ref(self, record, authority: ReleaseIndexRef) -> ArtifactRef:
        return ArtifactRef(
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

    def plan(self, request: ResolveRequest, index: ReleaseIndex) -> ProviderPlan:
        authority = self._authority()
        try:
            host = index.artifact("host-tools", self.host_key)
            runtime = index.artifact("runtime", request.target)
        except KeyError as exc:
            raise ContractError(f"Axiom-like target selection failed: {exc.args[0]}") from exc
        return ProviderPlan(
            self.family,
            (self._ref(host, authority), self._ref(runtime, authority)),
            {"dependencyShape": "host-tools+target-runtime", "host": self.host_key, "target": request.target},
        )

    def install(self, ref: ArtifactRef, archive: Path, staging_root: Path) -> None:
        extract_zip_safe(archive, staging_root)

    def validate(self, ref: ArtifactRef, materialized_root: Path) -> None:
        required = (
            materialized_root / "bin/protoc"
            if ref.kind == "host-tools"
            else materialized_root / "lib/cmake/semantic/semantic-config.cmake"
        )
        if not required.is_file():
            raise IntegrityError(f"Axiom-like {ref.kind} package missing required file: {required.name}")

    def environment(
        self,
        plan: ProviderPlan,
        materialized: tuple[MaterializedArtifact, ...],
    ) -> dict[str, str]:
        by_kind = {item.ref.kind: item.root for item in materialized}
        return {
            "AXIOM_LIKE_HOST_ROOT": str(by_kind["host-tools"]),
            "AXIOM_LIKE_RUNTIME_ROOT": str(by_kind["runtime"]),
        }
