# AxBuild Post-C2 P22 Five-Axis Drift Review v0.1

## Stage

- Owner: `aegis-governance`
- Stage: `P22 Five-Axis Drift Review`
- Repository: `Mostorm-Labs/axbuild`
- Canonical baseline under review: `f686192bf1f080b1bb2b26f8c5b23136f56e086e`
- Governance branch: `governance/axbuild-post-c2-authority-review`
- Predecessor: `docs/governance/AXBUILD-POST-C2-P21-AUTHORITY-REVIEW-v0.1.md`
- Profile: `Standard`
- Status: `READY_WITH_FINDINGS`
- Successor: `P23 Authority Supersession`

## Objective

Classify the bounded post-C2 drift identified by P21 across Product, Semantic, Architecture, Implementation, and Verification axes; determine the earliest owning layer for each finding; and define the minimum supersession boundary required before new platform-generalization capability work begins.

This review does not create the missing generic existing-release adoption mechanism and does not authorize consumer migration.

## Non-goals

P22 does **not**:

- start Phase 3 implementation;
- define the Generic Existing-Release Adoption design;
- authorize NearCast or Axiom consumer migration;
- change `NEARCAST_AIRPLAY_DEPS_URL`;
- change `redistribution.status=review-required`;
- generalize `Mostorm-Labs/axdeps` into a universal release authority without explicit authority;
- rewrite Phase 1.5 history in place;
- reopen C1.5 or C2 Gate results;
- classify a future missing P20 as a current C2 verification defect.

## Reviewed Sources

### Current / mixed authority

- `docs/dependencies/2026-09-10-dependency-inventory-seed-releases-v0.1.md`
- `docs/dependencies/dependency-inventory-v0.1.json`
- `docs/successors/AXBUILD-NEARCAST-AIRPLAY-RELEASE-AUTHORITY-RESOLUTION-P31-v0.1.md`

### Historical fulfilled execution authority

- `docs/packages/AXBUILD-NEARCAST-AIRPLAY-RELEASE-PUBLICATION-P31-v0.4.md`

### Core semantic contracts

- `schemas/sdk-lock-v1.schema.json`
- `schemas/release-index-v1.schema.json`
- `src/axbuild/contracts.py`
- `src/axbuild/model.py`

### Implementation reality / evidence

- canonical merge `f686192bf1f080b1bb2b26f8c5b23136f56e086e`
- PR #5 and durable P34 Gate evidence
- immutable `Mostorm-Labs/axdeps` release `387564756`
- `src/axbuild/qualification.py`
- `src/axbuild/nearcast_airplay.py`
- `src/axbuild/publication.py`
- hosted C1.5/C2 verification runs

### Descriptive downstream documentation

- `README.md`

## Baseline Delta Relevant to Drift

The repository delta from pre-C2 baseline `863238a718045f320ceb5715d235ccc895fa6e57` to canonical `f686192bf1f080b1bb2b26f8c5b23136f56e086e` adds NearCast AirPlay qualification/publication functionality and governance/task artifacts.

It does **not** modify:

- `schemas/sdk-lock-v1.schema.json`;
- `schemas/release-index-v1.schema.json`;
- `src/axbuild/contracts.py` core lock/index semantics;
- `src/axbuild/model.py` core release/index reference model.

Therefore C2 publication did not itself supersede the core AxBuild lock/index semantic contract.

## Five-Axis Summary

| Axis | Drift verdict | Severity | Owning layer | Required action |
| --- | --- | --- | --- | --- |
| Product | bounded planning/nomenclature drift; product objective remains trusted | moderate | Governance / roadmap authority | P23 canonicalize phase naming; preserve dependency-supply objective |
| Semantic | no material core semantic drift | none/materially clear | none | preserve v1 lock/index semantics; no P12/P13 reopening |
| Architecture | material authority drift around release ownership/location and future platform policy | material | Architecture authority / Governance | P23 partially supersede stale inventory claims and freeze current platform boundary |
| Implementation | C2 implementation aligns with accepted scope-specific authority; family-specific implementation must not be misread as generic platform architecture | non-blocking bounded specialization | future capability design, not repair | preserve implementation; do not route to P35/P36 |
| Verification | C2 verification remains valid; future generic adoption/producer capabilities have no Verification Design yet because their authority is not yet defined | forward authority gap, not C2 defect | future P20 after capability/design authority | do not reopen C2; require new P20 before future P30 |

## Axis 1 — Product Drift

### Verdict

`NO_PRODUCT_OBJECTIVE_DRIFT` with bounded roadmap/nomenclature drift.

The product problem remains trusted:

> reduce repeated expensive dependency builds by resolving exact qualified reusable dependency artifacts under explicit authority, integrity, and offline/fail-closed behavior.

C1.5/C2 strengthens evidence for that objective rather than contradicting it.

### Drift found

Older repository planning language places producer/adoption generalization in `Phase 2`, while the lifecycle actually executed a distinct first-real-family qualification/publication program after Phase 1/1.5 and now treats the next platform-generalization lifecycle as the next phase.

This is planning authority drift, not a changed product requirement.

### Canonical phase nomenclature for P23

P22 selects the following nomenclature to be frozen by P23:

```text
Phase 1    Framework Foundation
Phase 1.5  Dependency Inventory / Seed-Release Decisions
Phase 2    First Real Family Qualification + Private Publication
           (NearCast AirPlay C1 / C1.5 / C2 lifecycle, complete)
Phase 3    Platform Generalization
Phase 4    Consumer Adoption / Migration
```

Old forward-looking references that call platform generalization `Phase 2` become superseded planning nomenclature after P23. Their capability intent is not discarded merely because the number changes.

### Product routing

No P00/P01/P02 repair is required for the existing AxBuild problem statement.

A **new** Phase 3 capability may later enter P02/P03 because its exact capability authority is not yet frozen; that is successor work, not repair of the existing product objective.

## Axis 2 — Semantic Drift

### Verdict

`NO_MATERIAL_SEMANTIC_DRIFT`.

The core dependency-authority semantics remain:

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

The lock already permits the authoritative repository to be selected explicitly. C2 used that existing semantic capability to bind `Mostorm-Labs/axdeps`; it did not require a new lock field or change what Store/mirror/transport may decide.

The Store, mirror, GitHub Release, or cache still do not become dependency identity authority merely because they provide bytes.

### NearCast-specific contracts

C2 added NearCast-specific artifact-manifest / qualification-report contracts and qualification/publication logic. Those define one family workflow. They do not supersede `axbuild-sdk-lock-v1` or `axbuild-release-index-v1`.

### Semantic routing

- Do not reopen P12/P13 for C2.
- Do not create `sdk-lock-v2` merely to reconcile `axdeps` ownership.
- If Phase 3 Existing-Release Adoption later requires a new locator/adapter semantic, that future lifecycle must explicitly determine whether it can remain within v1 semantics or requires a new contract. P22 does not pre-decide that design.

## Axis 3 — Architecture Drift

### Verdict

`MATERIAL_ARCHITECTURE_AUTHORITY_DRIFT`.

### Conflict

Phase 1.5 inventory states, in effect:

```text
project-specific binary payloads remain project-owned by default
shared axdeps registry is deferred
NearCast seed release is proposed under Mostorm-Labs/NearCast
```

Later accepted C2 authority states:

```text
Mostorm-Labs/axbuild
  public resolver / schemas / tooling / provider contracts

Mostorm-Labs/axdeps
  private NearCast AirPlay dependency assets
  private publication
  release lifecycle authority for the C2 family
```

C2 implementation and immutable release occurrence follow the later authority.

### P22 ownership decision for `axdeps`

The evidence supports only the following current policy:

```yaml
axdeps_policy:
  current_scope: approved release authority for nearcast-airplay C2
  classification: family-specific current authority
  universal_default: false
  mandatory_for_all_private_families: false
  mandatory_for_project-specific_families: false
```

P22 explicitly rejects silently promoting the C2 decision into a universal platform rule.

Until future authority says otherwise:

- existing Axiom-owned qualified release sets remain project-owned and valid;
- `axdeps` is a proven private publication authority option, not automatic owner of every family;
- release authority must be selected explicitly per family/lifecycle;
- public `axbuild` remains tooling/contracts and must not become a binary dump for `review-required` assets.

### Exact Phase 1.5 claims requiring P23 supersession

P23 must supersede only the affected claims, not the whole inventory:

1. `axdeps` / shared binary registry is wholly deferred;
2. NearCast AirPlay seed publication should be owned by `Mostorm-Labs/NearCast`;
3. NearCast lock/release examples that hard-code NearCast as release repository for the now-published C2 release;
4. `currentRelease: null` / `newSeedReleaseRequired: true` for the NearCast AirPlay family after the immutable r2 release exists;
5. forward roadmap wording that calls the next platform-generalization lifecycle `Phase 2`.

### Phase 1.5 claims that remain current

P23 must preserve unless separately superseded by future authority:

- decision taxonomy;
- Axiom Skia = `ADOPT EXISTING RELEASE`;
- Axiom Semantic SDK = `ADOPT EXISTING RELEASE`;
- do not rebuild/mutate existing qualified bytes merely for AxBuild migration;
- toolchain/vendor `DO NOT REHOST` boundaries;
- NearCast AirPlay remains one monolithic family for this initial closure;
- consumer migration remains a separate lifecycle;
- no floating `latest` authority;
- exact repository/tag/index/digest binding remains required.

### Missing architecture authority after reconciliation

Even after P23, the following is intentionally still **not designed**:

- generic immutable Existing-Release Adoption mechanism;
- generic producer abstraction;
- change classifier contract;
- reusable producer workflow contract;
- general rule deciding project-owned vs `axdeps`-owned future families.

Those are Phase 3 capability/design questions, not facts P23 should invent while repairing old authority.

## Axis 4 — Implementation Drift

### Verdict

`NO_UNAUTHORIZED_IMPLEMENTATION_DRIFT` with bounded family specialization.

The C2 implementation added NearCast-specific qualification/publication code under AxBuild. `src/axbuild/publication.py` is explicitly NearCast AirPlay-specific: it imports the NearCast qualification constants, generates the `nearcast-airplay` index/lock, validates immutable release metadata, and verifies the preserved superseded publication.

That implementation is consistent with the accepted C1.5/C2 scope-specific packages and Gate evidence.

It did **not**:

- migrate NearCast consumer configuration;
- replace `NEARCAST_AIRPLAY_DEPS_URL`;
- publish the binary through public `axbuild`;
- make the old non-immutable release authoritative;
- change redistribution status;
- introduce a floating release selector;
- change the core lock/index contract.

### Important non-inference rule

Because `publication.py` exists inside AxBuild, downstream work must **not** infer:

```text
NearCast-specific publication implementation
        ==
generic producer/publication platform architecture
```

The current code is implementation reality for one qualified family. Phase 3 may reuse, extract, or replace parts only after new authority/design is established.

### Implementation routing

No P35/P36 repair is required from P22.

The implementation is not the earliest untrusted layer. The missing layer is future platform capability/architecture authority.

## Axis 5 — Verification Drift

### Verdict

`NO_C2_VERIFICATION_DRIFT`; `FUTURE_VERIFICATION_AUTHORITY_MISSING` for Phase 3, as expected.

C2 verification covered the frozen high-impact failure modes for its scope, including:

- qualification input integrity;
- release index validation;
- provenance validation;
- SDK lock validation;
- published-asset integrity;
- immutable GitHub release state;
- preservation/non-selection of the old release;
- empty-Store online resolve against r2;
- populated-Store offline replay;
- no consumer migration/public redistribution.

P34 accepted that evidence and repository integration is closed. P22 finds no basis to reinterpret the successful C2 lifecycle as a Verification Design defect.

### Future Phase 3 gap

No P20 Verification Design currently exists for:

- Existing-Release Adoption;
- Generic Producer Model;
- Change Classification;
- Reusable Producer Workflows.

This is not a late omission from C2 because those capabilities were outside C2 scope and are not yet fully defined.

Correct future routing is:

```text
Phase 3 capability authority / design
        -> P20 Verification Design
        -> P30 implementation planning
```

Do not jump directly from P23 to P30.

## Documentation Drift

`README.md` remains downstream/descriptive drift.

Its stale claims include presenting the repository as a Phase 1 framework candidate and describing producer/generalization work as future Phase 2 work.

README must be updated **after** P23 freezes reconciled authority. It is not a blocker requiring its own authority stage.

## Finding Register

### P22-F1 — Product / phase nomenclature drift

- Axis: Product / planning authority
- Severity: moderate
- Owner: P23 governance supersession
- Decision: canonicalize next platform-generalization lifecycle as Phase 3; preserve capability intent from old Phase 2 wording.

### P22-F2 — Core semantic contract remains stable

- Axis: Semantic
- Severity: none
- Owner: none
- Decision: no P12/P13 reopening; v1 lock/index remain current.

### P22-F3 — NearCast publication ownership drift

- Axis: Architecture
- Severity: material
- Owner: P23 governance supersession
- Decision: later C2 `axdeps` authority wins for `nearcast-airplay`; supersede contradictory Phase 1.5 claims only.

### P22-F4 — `axdeps` generalization is not authorized

- Axis: Architecture
- Severity: material boundary finding
- Owner: future Phase 3 authority/design if broader policy is desired
- Decision: current authority is family-specific; `axdeps` is neither universal nor mandatory default.

### P22-F5 — NearCast-specific implementation is bounded, not generic

- Axis: Implementation
- Severity: non-blocking
- Owner: future design, if generalized
- Decision: preserve code; do not classify as implementation defect and do not infer platform architecture from module placement/naming.

### P22-F6 — C2 verification remains valid

- Axis: Verification
- Severity: none for C2
- Owner: none for completed lifecycle
- Decision: no P20 repair and no Gate reopening.

### P22-F7 — Phase 3 verification authority is absent

- Axis: Verification / successor planning
- Severity: expected future gap
- Owner: future P20 after capability/design authority
- Decision: block direct P30 entry, but do not call this a C2 defect.

### P22-F8 — Existing-release adoption remains an unresolved capability authority gap

- Axis: Architecture / capability boundary
- Severity: material successor gap
- Owner: successor capability lifecycle after P23
- Decision: do not implement from inventory prose; establish explicit capability authority first.

### P22-F9 — README descriptive drift

- Axis: downstream documentation
- Severity: low/non-authority
- Owner: documentation sync after P23
- Decision: update after supersession; README must not lead authority.

## P22 Decision

```yaml
stage: P22
owner: aegis-governance
status: READY_WITH_FINDINGS
canonical_baseline: f686192bf1f080b1bb2b26f8c5b23136f56e086e

five_axis_verdict:
  product: BOUNDED_PLANNING_DRIFT
  semantic: NO_MATERIAL_DRIFT
  architecture: MATERIAL_AUTHORITY_DRIFT
  implementation: NO_UNAUTHORIZED_DRIFT
  verification: NO_C2_DRIFT_FUTURE_AUTHORITY_MISSING

blocking_product_failure: false
blocking_semantic_failure: false
reopen_c2_gate: false
implementation_repair_required: false
p23_required: true
safe_to_start_phase3_implementation: false
safe_to_start_consumer_migration: false
next_stage: P23
```

## Required P23 Supersession Boundary

P23 must create explicit replacement authority while preserving history. It must not edit Phase 1.5 v0.1 in place as if the old decision never existed.

Minimum replacement authority must freeze:

1. canonical post-C2 platform boundary:
   - `axbuild` = public framework/tooling/contracts;
   - `axdeps` = current private release authority for `nearcast-airplay`, not automatically universal;
2. existing Axiom qualified releases remain project-owned until a separate adoption lifecycle changes that;
3. NearCast AirPlay authoritative release is the immutable `axdeps` r2 publication;
4. old non-immutable release remains historical/non-authoritative;
5. consumer migration remains a separate lifecycle;
6. canonical phase nomenclature: Phase 3 = Platform Generalization, Phase 4 = Consumer Adoption/Migration;
7. `ADOPT EXISTING RELEASE` remains a valid unresolved capability requiring new authority/design, not an implementation instruction;
8. unchanged Phase 1.5 decisions remain current unless explicitly listed as superseded.

P23 should also identify README and inventory-v0.2 synchronization outputs, but descriptive synchronization must follow the supersession decision rather than replace it.

## Handoff

```yaml
type: stage_handoff
from_owner: aegis-governance
from_stage: P22
to_owner: aegis-governance
requested_stage: P23
repository: Mostorm-Labs/axbuild
canonical_baseline: f686192bf1f080b1bb2b26f8c5b23136f56e086e
governance_branch: governance/axbuild-post-c2-authority-review
predecessor_artifact: docs/governance/AXBUILD-POST-C2-P21-AUTHORITY-REVIEW-v0.1.md
review_artifact: docs/governance/AXBUILD-POST-C2-P22-FIVE-AXIS-DRIFT-REVIEW-v0.1.md
status: READY_WITH_FINDINGS
```
