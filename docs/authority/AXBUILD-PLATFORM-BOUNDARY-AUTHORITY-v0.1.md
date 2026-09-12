# AxBuild Platform Boundary Authority v0.1

## Status

- Classification: `Current Authority`
- Established by: `P23 Authority Supersession`
- Repository: `Mostorm-Labs/axbuild`
- Canonical implementation baseline reviewed: `f686192bf1f080b1bb2b26f8c5b23136f56e086e`
- Governance predecessors:
  - `docs/governance/AXBUILD-POST-C2-P21-AUTHORITY-REVIEW-v0.1.md`
  - `docs/governance/AXBUILD-POST-C2-P22-FIVE-AXIS-DRIFT-REVIEW-v0.1.md`

## Purpose

Define the current post-C2 AxBuild platform boundary without rewriting Phase 1.5 history and without pre-designing Phase 3 implementation.

This authority governs:

1. the role of public `Mostorm-Labs/axbuild` versus private release repositories;
2. the currently accepted scope of `Mostorm-Labs/axdeps`;
3. release-authority selection rules after C2;
4. canonical lifecycle phase naming;
5. the boundary between release publication and consumer migration;
6. preserved Phase 1.5 decisions that remain current;
7. successor capability gaps that must receive their own authority before implementation.

## 1. Platform roles

### `Mostorm-Labs/axbuild`

`axbuild` is the public dependency-supply tooling and contract repository.

Its platform role includes:

- family-neutral resolver behavior;
- Store and verified transport behavior;
- lock/index schemas and executable contract validation;
- provider contracts;
- qualification/publication tooling where explicitly authorized;
- reusable platform workflows when later established by authority.

`axbuild` is not, merely by being the tooling repository, the publication location for third-party binary payloads whose redistribution posture does not permit public publication.

### Binary release authority

Binary release authority is selected explicitly per dependency family/lifecycle. Repository location is part of dependency authority through the checked lock/index chain and must not be inferred from tool placement, cache location, or implementation convenience.

`Mostorm-Labs/axdeps` is an approved private immutable binary release authority and is the Current Authority for the `nearcast-airplay` C2 publication family.

Current policy:

```yaml
axdeps:
  role: approved private immutable dependency release authority
  current_authoritative_family:
    - nearcast-airplay
  universal_default: false
  mandatory_for_all_private_families: false
  mandatory_for_project_specific_families: false
```

No future family becomes `axdeps`-owned merely because `nearcast-airplay` uses it. Future ownership must be chosen by that family's authority lifecycle.

## 2. NearCast AirPlay current publication authority

For the current qualified NearCast AirPlay Windows x64 runtime closure:

```yaml
family: nearcast-airplay
release_authority_repository: Mostorm-Labs/axdeps
authoritative_release_tag: nearcast-airplay-runtime-windows-x64-release-26bdd0c07de1c6db-r2
authoritative_release_id: 387564756
artifact_identity: nearcast-airplay-runtime-windows-x64-release-26bdd0c07de1c6db
runtime_sha256: 0a085cdb439e4d3dbe517d83e40898d6a124ea689ec24cd987b49d7ccf74c44e
redistribution_status: review-required
```

The earlier non-immutable publication remains historical, preserved, and non-authoritative. It must not be selected by a current consumer lock.

This authority does not authorize NearCast consumer migration.

## 3. Core dependency-authority semantics remain unchanged

The current semantic authority remains the v1 lock/index model:

```text
SDK lock
  repository
  releaseTag
  releaseSetId
  indexAsset
  indexSha256
        |
        v
verified release index
  family
  releaseSetId
  exact artifact identity / asset / sha256
```

The selected repository is explicit authority data. Store, mirrors, GitHub transport, CI caches, and local package directories can provide bytes but do not choose a different dependency identity.

C2 did not supersede `axbuild-sdk-lock-v1` or `axbuild-release-index-v1`.

No `sdk-lock-v2` or release-index semantic change is established by this P23 authority.

## 4. Existing project-owned releases

Existing qualified Axiom release sets remain project-owned unless a later authority explicitly changes that ownership.

Current preserved decisions:

- Axiom Skia SDK: `ADOPT EXISTING RELEASE`;
- Axiom Semantic SDK: `ADOPT EXISTING RELEASE`;
- existing qualified bytes must not be rebuilt or mutated merely to satisfy AxBuild migration metadata;
- their current project-owned release authority remains valid until a separate adoption lifecycle proves and authorizes a new arrangement.

This authority does not move Axiom releases to `axdeps` and does not authorize Axiom consumer migration.

## 5. Preserved Phase 1.5 decisions

The following Phase 1.5 decisions remain current unless separately superseded in a future lifecycle:

- decision taxonomy: `ADOPT EXISTING RELEASE`, `CREATE SEED RELEASE`, `KEEP AS-IS`, `DO NOT REHOST`, `DEFER`;
- toolchain/vendor distribution boundaries classified as `DO NOT REHOST` remain in force;
- small/source-managed dependencies classified as `KEEP AS-IS` remain in force;
- NearCast AirPlay remains one monolithic initial family for the Windows x64 closure unless independent upgrade cadence/reuse evidence justifies a split;
- exact repository/tag/index/digest authority is required;
- floating `latest` is not dependency authority;
- consumer migration is a separate lifecycle from artifact qualification/publication;
- no hidden source-build fallback is implied by AxBuild resolution.

## 6. Explicitly superseded Phase 1.5 claims

The following prior claims are no longer Current Authority:

1. `Mostorm-Labs/axdeps` / a shared binary registry is wholly deferred until multiple projects independently require it.
2. NearCast AirPlay seed publication should be owned by `Mostorm-Labs/NearCast`.
3. NearCast AirPlay lock/release examples that require the release repository to be `Mostorm-Labs/NearCast` for the now-published C2 family.
4. NearCast AirPlay `currentRelease: null` and `newSeedReleaseRequired: true` after the immutable C2 r2 publication completed.
5. Forward roadmap language that names the next platform-generalization lifecycle `Phase 2`.

These claims remain preserved in Phase 1.5 v0.1 as historical context; this document supersedes them only for current decision-making.

## 7. Canonical phase nomenclature

The canonical lifecycle naming is now:

```text
Phase 1    Framework Foundation
Phase 1.5  Dependency Inventory / Seed-Release Decisions
Phase 2    First Real Family Qualification + Private Publication
           NearCast AirPlay C1 / C1.5 / C2 — complete
Phase 3    Platform Generalization
Phase 4    Consumer Adoption / Migration
```

Older references that call platform generalization `Phase 2` are historical planning nomenclature after this authority is established. Their underlying capability ideas are not discarded solely because the phase number changed.

## 8. Publication and consumer migration are separate authorities

A qualified/published dependency family does not automatically become the active consumer dependency authority inside a product repository.

Therefore C2 publication success does not authorize:

- modifying `Mostorm-Labs/NearCast`;
- replacing `NEARCAST_AIRPLAY_DEPS_URL` or current restore behavior;
- checking a new AxBuild consumer lock into NearCast;
- changing NearCast CI to use AxBuild;
- Axiom migration;
- public redistribution.

Each consumer migration requires its own requirements/design/verification/implementation lifecycle and explicit Gate.

## 9. Redistribution boundary

`redistribution.status=review-required` remains current for the qualified `nearcast-airplay` artifact.

Private immutable publication to `Mostorm-Labs/axdeps` is not a general approval for public or external redistribution. Future publication scopes must preserve or explicitly supersede their own redistribution authority.

## 10. Phase 3 authority gap intentionally remains open

This document does not design Phase 3. The following capabilities remain unresolved successor work:

- generic immutable Existing-Release Adoption;
- Generic Producer Model;
- Change Classification;
- Reusable Producer Workflows;
- any broader policy for deciding project-owned versus `axdeps`-owned future families.

At minimum, Existing-Release Adoption must receive explicit capability authority before Axiom migration can safely proceed.

Future work must not treat the current NearCast-specific qualification/publication implementation as generic architecture authority merely because that code exists in `axbuild`.

## 11. Successor routing boundary

After this P23 authority is integrated, the next substantive lifecycle may establish Phase 3 capability authority. It must not jump directly to P30.

Expected sequence:

```text
Phase 3 capability authority / requirements / design
        -> P20 Verification Design
        -> P30 Implementation Planning
        -> P31 Task Packaging
        -> P32 Implementation
        -> P34 Gate
```

The first Phase 3 capability to evaluate is Generic Existing-Release Adoption because Axiom Skia and Semantic SDK already have qualified project-owned releases that should not be rebuilt merely for migration.

## 12. Authority precedence

For the scopes explicitly covered here, precedence is:

```text
AXBUILD-PLATFORM-BOUNDARY-AUTHORITY-v0.1
        > affected stale Phase 1.5 claims
```

The Phase 1.5 inventory remains Current Authority for preserved decisions not explicitly superseded here.

C2 P31 execution packages remain historical/fulfilled execution authority and evidence; they do not override this platform boundary for future work.
