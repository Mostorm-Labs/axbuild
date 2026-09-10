"""Family-neutral resolution orchestration."""
from __future__ import annotations

from typing import Any

from .contracts import load_release_index, validate_namespace
from .errors import ContractError
from .model import ArtifactRef, MaterializedArtifact, ResolutionResult, ResolveRequest
from .provider import Provider
from .store import SdkStore
from .transport import ensure_release_file


def _assert_ref_matches_verified_index(ref: ArtifactRef, index, index_ref) -> None:
    if ref.family != index.family or ref.family != index_ref.family:
        raise ContractError("provider artifact family differs from verified index")
    if ref.repository != index_ref.repository or ref.release_tag != index_ref.release_tag:
        raise ContractError("provider artifact repository/tag differs from verified index authority")
    try:
        record = index.artifact(ref.kind, ref.key)
    except KeyError as exc:
        raise ContractError(
            f"provider artifact is absent from verified index: {ref.kind}/{ref.key}"
        ) from exc
    if (
        ref.identity != record.identity
        or ref.asset != record.asset
        or ref.sha256.lower() != record.sha256.lower()
        or ref.size != record.size
        or dict(ref.metadata) != dict(record.metadata)
    ):
        raise ContractError(
            f"provider artifact differs from verified index: {ref.kind}/{ref.key}"
        )


def resolve_provider(provider: Provider, request: ResolveRequest) -> ResolutionResult:
    family = validate_namespace(provider.family)
    store = SdkStore(request.store_root)
    index_ref = provider.index_ref(request)
    if index_ref.family != family:
        raise ContractError("provider index family differs from registered provider family")

    index_path = store.release_index_path(index_ref)
    with store.lock(f"index:{family}:{index_ref.identity}:{index_ref.asset}"):
        index_file = ensure_release_file(
            index_ref,
            index_path,
            mirror=request.mirror,
            offline=request.offline,
        )
    index = load_release_index(index_path)
    if index.family != family:
        raise ContractError("release index family differs from provider family")
    if index.release_set_id != index_ref.identity:
        raise ContractError("release index releaseSetId differs from SDK lock authority")

    plan = provider.plan(request, index)
    if plan.family != family:
        raise ContractError("provider plan family differs from provider family")
    keys = [(ref.kind, ref.key) for ref in plan.artifacts]
    if len(set(keys)) != len(keys):
        raise ContractError("provider plan contains duplicate artifact kind/key")
    for ref in plan.artifacts:
        _assert_ref_matches_verified_index(ref, index, index_ref)

    materialized: list[MaterializedArtifact] = []
    artifact_facts: list[dict[str, Any]] = []
    network_used = index_file.network_used

    for ref in plan.artifacts:
        root = store.package_path(ref)
        source = "store"
        artifact_network = False
        if root.exists():
            provider.validate(ref, root)
        else:
            archive = store.archive_path(ref)
            with store.lock(f"archive:{ref.sha256}:{ref.asset}"):
                transfer = ensure_release_file(
                    ref,
                    archive,
                    mirror=request.mirror,
                    offline=request.offline,
                )
            source = transfer.source
            artifact_network = transfer.network_used
            root = store.materialize_package(
                ref,
                archive,
                lambda source, staging, ref=ref: provider.install(ref, source, staging),
                lambda materialized_root, ref=ref: provider.validate(ref, materialized_root),
            )
        item = MaterializedArtifact(ref, root, source, artifact_network)
        materialized.append(item)
        artifact_facts.append(
            {
                "family": ref.family,
                "kind": ref.kind,
                "key": ref.key,
                "identity": ref.identity,
                "sha256": ref.sha256,
                "root": str(root),
                "source": source,
                "networkUsed": artifact_network,
            }
        )
        network_used = network_used or artifact_network

    environment = provider.environment(plan, tuple(materialized))
    if not isinstance(environment, dict) or any(
        not isinstance(key, str) or not isinstance(value, str)
        for key, value in environment.items()
    ):
        raise ContractError("provider environment must map strings to strings")

    facts = {
        "format": "axbuild-resolution-v1",
        "family": family,
        "target": request.target,
        "releaseSetId": index_ref.identity,
        "index": {
            "identity": index_ref.identity,
            "sha256": index_ref.sha256,
            "root": str(index_path),
            "source": index_file.source,
            "networkUsed": index_file.network_used,
        },
        "artifacts": artifact_facts,
        "networkUsed": network_used,
        "metadata": dict(plan.metadata),
    }
    return ResolutionResult(environment, facts)
