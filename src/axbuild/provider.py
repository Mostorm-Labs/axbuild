"""Project-owned provider contract and explicit registry."""
from __future__ import annotations

from pathlib import Path
from typing import Protocol

from .contracts import validate_namespace
from .errors import AxBuildError
from .model import (
    ArtifactRef,
    MaterializedArtifact,
    ProviderPlan,
    ReleaseIndex,
    ReleaseIndexRef,
    ResolutionResult,
    ResolveRequest,
)


class Provider(Protocol):
    family: str

    def index_ref(self, request: ResolveRequest) -> ReleaseIndexRef: ...

    def plan(self, request: ResolveRequest, index: ReleaseIndex) -> ProviderPlan: ...

    def install(self, ref: ArtifactRef, archive: Path, staging_root: Path) -> None: ...

    def validate(self, ref: ArtifactRef, materialized_root: Path) -> None: ...

    def environment(
        self,
        plan: ProviderPlan,
        materialized: tuple[MaterializedArtifact, ...],
    ) -> dict[str, str]: ...


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, Provider] = {}

    def register(self, provider: Provider) -> None:
        family = validate_namespace(provider.family)
        if family in self._providers:
            raise AxBuildError(f"provider already registered: {family}")
        self._providers[family] = provider

    def resolve(self, family: str, request: ResolveRequest) -> ResolutionResult:
        if family not in self._providers:
            raise AxBuildError(f"unknown provider family: {family}")
        from .resolver import resolve_provider

        return resolve_provider(self._providers[family], request)
