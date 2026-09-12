# AxBuild Post-C2 P21 Authority Review v0.1

## Stage

- Owner: `aegis-governance`
- Stage: `P21 Authority Review`
- Repository: `Mostorm-Labs/axbuild`
- Canonical baseline reviewed: `f686192bf1f080b1bb2b26f8c5b23136f56e086e`
- Profile: `Standard`
- Status: `READY_WITH_FINDINGS`
- Successor: `P22 Five-Axis Drift Review`

## Objective

Reconcile the authority map after C2 private release publication and repository integration closure, without silently rewriting historical documents or starting Phase 3 implementation.

This review answers only:

1. which sources are Current Authority for their scope;
2. which sources are historical, execution-only, descriptive, or stale;
3. whether current sources conflict materially;
4. which missing or stale authority must be resolved before the next platform-generalization lifecycle.

## Non-goals

This P21 review does **not**:

- start Phase 3 implementation;
- authorize NearCast consumer migration;
- authorize Axiom consumer migration;
- change `NEARCAST_AIRPLAY_DEPS_URL`;
- change redistribution status;
- delete or rewrite historical authority/evidence;
- declare the old dependency inventory wholly superseded;
- perform P22 drift classification or P23 supersession.

## Repository Reality / Evidence Baseline

The following facts are accepted implementation/release reality, not architecture authority merely because they exist:

- `main` is integrated at `f686192bf1f080b1bb2b26f8c5b23136f56e086e`.
- PR #5 is merged through that merge commit.
- C2 P34 durable Gate PASS is recorded at PR #5 issue comment `5646716201`.
- authoritative private release repository: `Mostorm-Labs/axdeps`.
- authoritative release id: `387564756`.
- authoritative release tag: `nearcast-airplay-runtime-windows-x64-release-26bdd0c07de1c6db-r2`.
- GitHub reports the authoritative release as immutable.
- runtime SHA256: `0a085cdb439e4d3dbe517d83e40898d6a124ea689ec24cd987b49d7ccf74c44e`.
- the earlier non-immutable release `387538376` remains preserved, superseded, non-authoritative, and unchanged.
- `redistribution.status` remains `review-required`.
- no NearCast consumer migration has been authorized or completed by this lifecycle.

## Source-of-Truth Map

### A. Current Authority — scope-specific

#### A1. `docs/successors/AXBUILD-NEARCAST-AIRPLAY-RELEASE-AUTHORITY-RESOLUTION-P31-v0.1.md`

Classification: **Current Authority for the C2 release-location / publication-ownership boundary**.

Accepted authority within its scope:

```text
Mostorm-Labs/axbuild
  - resolver
  - schemas
  - tooling
  - provider contracts

Mostorm-Labs/axdeps
  - dependency release assets
  - internal/private artifact publication
  - release lifecycle authority
```

This decision is later than the Phase 1.5 inventory and was materially exercised by C2. It therefore governs the NearCast AirPlay private publication boundary unless and until explicitly superseded.

This P21 review does **not** automatically generalize every future family to `axdeps`; that broader platform rule still requires explicit reconciled authority.

### B. Current Authority with stale/conflicting claims requiring P22

#### B1. `docs/dependencies/2026-09-10-dependency-inventory-seed-releases-v0.1.md`
#### B2. `docs/dependencies/dependency-inventory-v0.1.json`

Classification: **Mixed Current Authority; partially stale, not wholly superseded**.

Still trusted unless P22 finds a separate conflict:

- decision taxonomy: `ADOPT EXISTING RELEASE`, `CREATE SEED RELEASE`, `KEEP AS-IS`, `DO NOT REHOST`, `DEFER`;
- Axiom Skia = `ADOPT EXISTING RELEASE`;
- Axiom Semantic SDK = `ADOPT EXISTING RELEASE`;
- do not rebuild Axiom qualified releases merely to change AxBuild metadata;
- toolchain/vendor boundaries remain `DO NOT REHOST` where recorded;
- NearCast AirPlay remains one monolithic `nearcast-airplay` family for the initial Windows x64 closure rather than splitting GStreamer/Bonjour/etc. into independent families without evidence;
- consumer migration remains a later explicit change, not an implicit consequence of publication.

Claims that are no longer safe to treat as current without reconciliation:

1. shared binary registry / `Mostorm-Labs/axdeps` is deferred until at least two projects require it;
2. project-specific binary payloads stay with the project owner by default as a sufficient description of the current NearCast publication boundary;
3. the proposed NearCast seed-release owner repository is `Mostorm-Labs/NearCast`;
4. the proposed NearCast lock/release examples point to a NearCast-owned release instead of the now-established private `axdeps` publication authority;
5. roadmap language names producer/adoption generalization as `Phase 2`, while the post-C2 working roadmap has evolved and requires one canonical phase nomenclature.

P21 does not overwrite these claims. P22 must classify their Product/Semantic/Architecture/Implementation/Verification drift and determine the minimum replacement authority.

### C. Historical / fulfilled execution authority

#### C1. `docs/packages/AXBUILD-NEARCAST-AIRPLAY-RELEASE-PUBLICATION-P31-v0.4.md`

Classification: **Historical / fulfilled Task Package authority**.

It remains authoritative for what C2 P32 was allowed and required to do, including:

- preservation of the first non-immutable release;
- `-r2` release identity;
- immutable-release precondition;
- exact artifact digest;
- online/offline resolver verification;
- no consumer migration;
- no public redistribution.

It is **not** the general platform architecture or future-phase roadmap authority after C2 closure.

Earlier P31 package revisions are superseded historical execution packages and must not be reused as current implementation authority.

### D. Evidence / repository occurrence

Classification: **Evidence / Implementation Reality**.

Includes:

- PR #5 and merge commit `f686192bf1f080b1bb2b26f8c5b23136f56e086e`;
- C1.5 and C2 P34 durable Gate records;
- AxBuild CI and axdeps release-verification runs;
- release `387564756` and its immutable assets;
- preserved failed publication `387538376`.

These sources prove that a scope-specific authority was implemented and integrated. They do not by themselves define the next platform capability model.

### E. Descriptive / downstream documentation

#### E1. `README.md`

Classification: **Descriptive documentation; stale downstream status language**.

The README still describes the repository as a `Phase 1 framework candidate`, says Phase 1 deliberately does not modify Axiom or NearCast, and places producer matrix/change classification/reusable workflows/migrations in a later phase. This wording is no longer an accurate status summary after C1.5/C2 integration.

README drift is not an authority blocker by itself, but it must be repaired after the corresponding authority is reconciled; documentation must not be updated first and then treated as authority.

## Missing Current Authority

No single current platform-level authority presently consolidates all of the following post-C2 facts and future boundaries:

1. the role of public `axbuild` versus private `axdeps`;
2. whether `axdeps` is the default release authority for all AxBuild-managed private binary families or only an approved authority option selected per family;
3. current release-ownership rules for project-specific versus shared families;
4. the canonical phase nomenclature after C2;
5. the exact boundary between release publication and consumer migration;
6. the generic mechanism for `ADOPT EXISTING RELEASE` without rebuilding or mutating existing qualified bytes;
7. how Generic Producer Model, Change Classification, and Reusable Producer Workflows relate to existing-release adoption;
8. when a family may remain project-owned instead of `axdeps`-owned.

This missing consolidated authority is the principal governance gap before Phase 3 capability authority can be safely established.

## Conflict Review

### Material authority conflict found

Yes, but it is bounded and explainable:

```text
Phase 1.5 inventory claim
  shared axdeps registry deferred / NearCast-owned seed publication

versus

later C2 release-authority decision
  axbuild = public tooling
  axdeps = private dependency release authority

plus

repository/release occurrence
  immutable nearcast-airplay r2 actually published in axdeps
```

The conflict does **not** invalidate C2. The later scope-specific authority was explicit, Gate-reviewed, and integrated. The problem is that the older platform/inventory authority was never formally reconciled/superseded at the affected claims.

### No earlier untrusted product/problem layer identified

The underlying product problem remains coherent: reduce repeated expensive dependency builds and consume exact qualified artifacts. P21 found no evidence that the problem statement or dependency-supply objective itself is invalid.

The earliest untrusted layer remains **Authority Reconciliation**, not Product Discovery and not Implementation.

## P21 Findings

### P21-F1 — Release authority ownership drift

Severity: material governance finding.

The Phase 1.5 inventory and C2 authority disagree on publication ownership/location for NearCast AirPlay. C2 reality follows the later C2 authority.

Route: `P22 Architecture drift` -> replacement/supersession decision.

### P21-F2 — Phase nomenclature drift

Severity: moderate governance finding.

Older repository docs call producer/adoption generalization `Phase 2`; the post-C2 working roadmap refers to the next platform-generalization lifecycle as Phase 3. One nomenclature must become canonical before new lifecycle documents are created.

Route: `P22 Product/Architecture planning drift`.

### P21-F3 — README status drift

Severity: non-authority documentation finding.

README does not describe C1.5/C2 reality and still presents AxBuild as a Phase 1 candidate.

Route: repair only after authority reconciliation; do not use README as replacement authority.

### P21-F4 — Generic existing-release adoption authority still missing

Severity: material capability-authority gap.

The inventory correctly identifies Axiom Skia/Semantic as `ADOPT EXISTING RELEASE`, but no current authority defines the generic immutable adoption mechanism. C2 seed-publication success does not answer this problem.

Route: after P22/P23 reconciliation, establish a new capability lifecycle for generic existing-release adoption before Axiom migration.

### P21-F5 — Consumer migration remains explicitly out of scope

Severity: boundary preservation finding.

Nothing in C2 publication or integration authorizes NearCast consumer migration. Publication success must not be interpreted as permission to replace NearCast's current restore/CI authority.

Route: preserve boundary; future consumer adoption requires its own authority and verification lifecycle.

## P21 Decision

```yaml
stage: P21
owner: aegis-governance
status: READY_WITH_FINDINGS
canonical_baseline: f686192bf1f080b1bb2b26f8c5b23136f56e086e
earliest_untrusted_layer: Authority Reconciliation
blocking_product_authority_failure: false
material_authority_drift: true
safe_to_start_phase3_implementation: false
safe_to_start_consumer_migration: false
next_stage: P22
```

P21 concludes that there is enough trusted authority to proceed to a bounded Five-Axis Drift Review. There is **not** enough reconciled authority to enter P30 or consumer migration.

## Required P22 Scope

P22 must review only the drift relevant to the post-C2 boundary and classify each finding across:

- Product;
- Semantic;
- Architecture;
- Implementation;
- Verification.

At minimum P22 must decide:

1. whether the `axdeps` authority established by C2 is family-specific, policy-default, or universal;
2. which exact Phase 1.5 inventory claims are superseded versus still current;
3. canonical phase nomenclature;
4. whether C2 introduced any semantic/contract change to the core lock/index authority model (expected answer may be `no`, but must be reviewed rather than assumed);
5. whether implementation reality drifted beyond accepted authority;
6. whether verification authority needs revision for future generic adoption/producer slices;
7. whether a P23 replacement/supersession artifact is required before new capability discovery/design.

## Handoff

```yaml
type: stage_handoff
from_owner: aegis-governance
from_stage: P21
to_owner: aegis-governance
requested_stage: P22
repository: Mostorm-Labs/axbuild
canonical_baseline: f686192bf1f080b1bb2b26f8c5b23136f56e086e
review_artifact: docs/governance/AXBUILD-POST-C2-P21-AUTHORITY-REVIEW-v0.1.md
status: READY_WITH_FINDINGS
```
