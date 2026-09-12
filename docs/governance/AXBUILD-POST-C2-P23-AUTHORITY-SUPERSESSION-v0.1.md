# AxBuild Post-C2 P23 Authority Supersession v0.1

## Stage

- Owner: `aegis-governance`
- Stage: `P23 Authority Supersession`
- Repository: `Mostorm-Labs/axbuild`
- Canonical baseline under governance review: `f686192bf1f080b1bb2b26f8c5b23136f56e086e`
- Governance branch: `governance/axbuild-post-c2-authority-review`
- Predecessors:
  - `docs/governance/AXBUILD-POST-C2-P21-AUTHORITY-REVIEW-v0.1.md`
  - `docs/governance/AXBUILD-POST-C2-P22-FIVE-AXIS-DRIFT-REVIEW-v0.1.md`
- Replacement Current Authority:
  - `docs/authority/AXBUILD-PLATFORM-BOUNDARY-AUTHORITY-v0.1.md`
- Status: `ESTABLISHED`

## Objective

Perform explicit partial supersession of the stale Phase 1.5 claims identified by P21/P22 while preserving all unaffected inventory decisions and historical evidence.

P23 does not rewrite Phase 1.5 v0.1 in place. The old documents remain available as historical/current mixed authority, with precedence narrowed by the replacement authority for the exact claims listed below.

## Non-goals

P23 does **not**:

- design Phase 3 Existing-Release Adoption;
- design Generic Producer Model, Change Classification, or Reusable Producer Workflows;
- authorize Phase 3 implementation;
- authorize NearCast or Axiom consumer migration;
- modify `NEARCAST_AIRPLAY_DEPS_URL`;
- move Axiom releases into `axdeps`;
- make `axdeps` the universal/default repository for all future dependency families;
- change `axbuild-sdk-lock-v1` or `axbuild-release-index-v1`;
- change `redistribution.status=review-required`;
- reopen C1.5/C2 Gate results.

## Source Authority Map After Supersession

### Current Authority — platform boundary

`docs/authority/AXBUILD-PLATFORM-BOUNDARY-AUTHORITY-v0.1.md`

This is Current Authority for:

- public `axbuild` versus binary release-authority boundary;
- current family-specific `axdeps` authority policy;
- NearCast AirPlay C2 publication authority;
- canonical phase nomenclature;
- publication versus consumer-migration separation;
- preserved Phase 1.5 decisions versus explicitly superseded claims;
- the fact that Phase 3 generic capability authority is still missing.

### Current Authority — preserved Phase 1.5 scope

The following remain Current Authority from:

- `docs/dependencies/2026-09-10-dependency-inventory-seed-releases-v0.1.md`
- `docs/dependencies/dependency-inventory-v0.1.json`

Preserved decisions include:

- decision taxonomy;
- Axiom Skia = `ADOPT EXISTING RELEASE`;
- Axiom Semantic SDK = `ADOPT EXISTING RELEASE`;
- no rebuild/mutation of existing qualified Axiom bytes merely for migration metadata;
- recorded `DO NOT REHOST` boundaries;
- recorded `KEEP AS-IS` source/tooling boundaries;
- initial NearCast AirPlay monolithic-family decision;
- consumer migration remains separate from publication;
- exact repository/tag/index/digest authority and no floating `latest`.

### Historical / fulfilled authority and evidence

The following remain preserved as history/evidence and are not replacement platform architecture:

- C1/C1.5/C2 P30/P31 packages;
- C1.5/C2 P34 Gate records;
- PR #5 and merge `f686192bf1f080b1bb2b26f8c5b23136f56e086e`;
- immutable `nearcast-airplay` r2 release in `Mostorm-Labs/axdeps`;
- preserved earlier non-immutable release.

## Supersession Ledger

### S1 — Shared `axdeps` registry wholly deferred

**Old claim:** a shared binary registry such as `Mostorm-Labs/axdeps` is deferred until at least two projects require the same independently versioned family.

**Classification:** `Superseded for current platform policy`.

**Replacement:** `axdeps` is already an approved private immutable release authority and is Current Authority for `nearcast-airplay` C2. It is not automatically universal/default for other families.

**Reason:** later explicit C2 authority plus successful immutable publication and integration established a real approved use before the old deferral condition was met.

### S2 — NearCast AirPlay publication owned by `Mostorm-Labs/NearCast`

**Old claim:** initial NearCast AirPlay seed release should be published under `Mostorm-Labs/NearCast`.

**Classification:** `Superseded for the current nearcast-airplay publication family`.

**Replacement:** current release authority is `Mostorm-Labs/axdeps` with authoritative immutable r2 release.

**Reason:** C2 explicitly separated public AxBuild tooling from private binary publication and selected `axdeps`.

### S3 — NearCast-owned lock/release examples for the now-published family

**Old claim:** examples that require the current NearCast AirPlay lock to point at a NearCast-owned release repository.

**Classification:** `Superseded for the current published C2 release`.

**Replacement:** current lock/index authority may point at `Mostorm-Labs/axdeps`; repository identity remains explicit in the existing v1 lock semantic.

**Reason:** C2 did not change lock semantics; it exercised the existing repository selector against the approved private authority.

### S4 — NearCast AirPlay `currentRelease: null` / `newSeedReleaseRequired: true`

**Old claim:** NearCast AirPlay has no current canonical release and still requires creation of its first seed release.

**Classification:** `Superseded by completed lifecycle state`.

**Replacement:** the qualified artifact has an authoritative immutable r2 private release in `Mostorm-Labs/axdeps`.

**Reason:** C1.5/C2 completed qualification, publication, Gate, and repository integration.

### S5 — Platform generalization named `Phase 2`

**Old claim:** producer/adoption generalization is future `Phase 2` work.

**Classification:** `Superseded planning nomenclature`.

**Replacement:** canonical lifecycle naming is:

```text
Phase 1    Framework Foundation
Phase 1.5  Dependency Inventory / Seed-Release Decisions
Phase 2    First Real Family Qualification + Private Publication
Phase 3    Platform Generalization
Phase 4    Consumer Adoption / Migration
```

**Reason:** a distinct real-family qualification/publication lifecycle has now occupied the Phase 2 slot and is complete. Capability intent from old wording remains valid where not otherwise superseded.

## Claims Explicitly Not Superseded

P23 explicitly preserves the following boundaries:

1. Axiom Skia and Semantic SDK remain `ADOPT EXISTING RELEASE` candidates.
2. Existing qualified Axiom bytes must not be rebuilt solely to satisfy AxBuild metadata/migration.
3. Existing Axiom release ownership is unchanged by C2/P23.
4. Toolchain/vendor `DO NOT REHOST` decisions remain current.
5. NearCast AirPlay remains a monolithic family for the current initial closure unless a later lifecycle justifies splitting.
6. Publication does not imply consumer migration.
7. `redistribution.status=review-required` remains unchanged.
8. Core v1 lock/index semantics remain current.
9. `axdeps` is not made universal/default by this supersession.
10. No Phase 3 implementation authority exists yet.

## Downstream Dependency Expectations

After P23 is integrated, downstream documents and planning must obey:

```text
Current platform boundary authority
  docs/authority/AXBUILD-PLATFORM-BOUNDARY-AUTHORITY-v0.1.md
        |
        +--> Phase 1.5 inventory only for preserved decisions
        |
        +--> C2 history/evidence for nearcast-airplay publication occurrence
        |
        +--> future Phase 3 capability authority (not yet established)
```

README/status documentation should be synchronized only after this P23 authority is accepted/integrated. README text must not become authority merely because it is newer prose.

## Gate / Evidence Impact

P23 does not invalidate C1.5 or C2 evidence. No Gate reopening is required.

No implementation repair is required.

No semantic schema/version repair is required.

The unresolved Phase 3 verification gap is forward-looking: once a Phase 3 capability/design authority exists, it must receive P20 Verification Design before P30 implementation planning.

## P23 Decision

```yaml
stage: P23
owner: aegis-governance
status: ESTABLISHED
replacement_authority:
  docs/authority/AXBUILD-PLATFORM-BOUNDARY-AUTHORITY-v0.1.md

supersession:
  mode: partial
  old_authority_preserved: true
  stale_claims_superseded: 5

core_semantics_changed: false
c2_gate_reopened: false
implementation_repair_required: false
consumer_migration_authorized: false
phase3_implementation_authorized: false

current_phase_boundary:
  phase2: complete
  phase3: authority_not_yet_established
  phase4: not_started
```

## Successor Boundary

P23 closes the post-C2 authority reconciliation itself. It does not own the next substantive capability lifecycle.

The next substantive owner should be selected by central `aegis` routing or, if the successor is accepted as unambiguous, begin a new Phase 3 capability-authority lifecycle starting from requirements/capability definition rather than P30 implementation.

Expected first successor problem:

> Define a generic immutable Existing-Release Adoption capability that can consume already-qualified project-owned release sets such as Axiom Skia/Semantic without rebuilding, mutating, or silently relocating their bytes.

Before implementation, that successor lifecycle must establish capability/design authority and P20 Verification Design.
