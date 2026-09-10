"""Immutable data model shared by AxBuild components."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class ReleaseIndexRef:
    family: str
    identity: str
    repository: str
    release_tag: str
    asset: str
    sha256: str


@dataclass(frozen=True)
class ArtifactRef:
    family: str
    kind: str
    key: str
    identity: str
    repository: str
    release_tag: str
    asset: str
    sha256: str
    size: int | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict, compare=False, hash=False)


@dataclass(frozen=True)
class ResolveRequest:
    repo_root: Path
    target: str
    store_root: Path
    mirror: str | None = None
    offline: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "repo_root", self.repo_root.expanduser().absolute())
        object.__setattr__(self, "store_root", self.store_root.expanduser().absolute())


@dataclass(frozen=True)
class ProviderPlan:
    family: str
    artifacts: tuple[ArtifactRef, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MaterializedArtifact:
    ref: ArtifactRef
    root: Path
    source: str
    network_used: bool

@dataclass(frozen=True)
class IndexedArtifact:
    kind: str
    key: str
    identity: str
    asset: str
    sha256: str
    size: int | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict, compare=False, hash=False)


@dataclass(frozen=True)
class ReleaseIndex:
    family: str
    release_set_id: str
    artifacts: tuple[IndexedArtifact, ...]

    def artifact(self, kind: str, key: str) -> IndexedArtifact:
        matches = [item for item in self.artifacts if item.kind == kind and item.key == key]
        if len(matches) != 1:
            raise KeyError((kind, key))
        return matches[0]

@dataclass(frozen=True)
class ResolutionResult:
    environment: Mapping[str, str]
    facts: Mapping[str, Any]
