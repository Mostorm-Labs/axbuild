# AxBuild Phase 3A Generic Existing-Release Adoption — P02 Product Requirement v0.1

## Stage

- Owner: `aegis-discovery`
- Stage: `P02 Product Requirement`
- Repository: `Mostorm-Labs/axbuild`
- Canonical baseline: `580adc8e015413f6a77b1952321fa6e2caa43ae4`
- Phase: `Phase 3 — Platform Generalization`
- Capability: `Phase 3A — Generic Existing-Release Adoption`
- Profile: `Standard`
- Status: `READY`
- Successor: `P03 Capability Traceability`

## 1. Role

Translate the already-validated Existing-Release Adoption problem into product requirements without selecting the architecture, schema extension, metadata placement, adapter boundary, or implementation mechanism.

## 2. Authority

### Current Authority

`docs/authority/AXBUILD-PLATFORM-BOUNDARY-AUTHORITY-v0.1.md`

This authority establishes that:

- Phase 3 is Platform Generalization;
- Axiom Skia SDK and Axiom Semantic SDK remain `ADOPT EXISTING RELEASE` candidates;
- their existing qualified bytes and project-owned release authority must not be rebuilt, mutated, or moved merely to satisfy AxBuild migration metadata;
- `Mostorm-Labs/axdeps` is not the universal/default owner for future families;
- exact repository/tag/index/digest authority, no floating `latest`, and no hidden source-build fallback remain current;
- publication/adoption and consumer migration remain separate lifecycles;
- Generic Existing-Release Adoption is the first Phase 3 capability that must receive explicit authority before Axiom migration.

### Preserved Phase 1.5 input

`docs/dependencies/2026-09-10-dependency-inventory-seed-releases-v0.1.md`

The preserved inventory provides two concrete existing-release shapes:

1. Axiom Skia SDK
   - current release: `skia-sdk-r1-full-v1-54c1999dc79d094d`;
   - high-cost qualified binary SDK;
   - multiple targets/variants;
   - decision: `ADOPT EXISTING RELEASE`.
2. Axiom Semantic SDK
   - current release: `semantic-sdk-v2-14e3d492c9b7f970`;
   - host-tools plus target-runtime assets;
   - decision: `ADOPT EXISTING RELEASE`.

The inventory explicitly requires that existing release tags remain untouched, large binaries are not duplicated solely for metadata conversion, and the eventual mechanism is family-neutral rather than hard-coded to Axiom/Skia/Semantic.

## 3. Objective

Enable AxBuild to adopt an already-qualified, project-owned release set as an exact dependency authority **without rebuilding, mutating, republishing, relocating, or silently changing the ownership of the existing binary artifacts**.

After adoption, AxBuild must be able to resolve the adopted release deterministically through its common resolver/Store model, validate exact source identity and bytes, replay from Store offline, and fail closed when the adopted authority cannot be proven.

## 4. Problem Statement

AxBuild currently proves two useful models:

- family-neutral consumption from an AxBuild-compatible lock/index contract;
- creation/qualification/publication of a new family such as `nearcast-airplay`.

A different real-world case remains unsolved: valuable qualified release sets already exist in project-owned repositories and must remain there.

The business/engineering waste to avoid is:

```text
already-qualified large release
        -> rebuild only to satisfy AxBuild metadata
        -> duplicate/rehost large binaries
        -> change ownership or tag history
```

The required outcome is:

```text
already-qualified project-owned immutable release
        -> explicit adoption authority
        -> AxBuild canonical resolution view
        -> verified Store materialization
        -> online/offline deterministic reuse

without changing the original qualified bytes or ownership
```

## 5. Jobs To Be Done

### JTBD-01 — Dependency owner

When a project already owns a qualified immutable dependency release, the dependency owner needs to make that release consumable through AxBuild without creating a second copy of the binaries or rewriting the original release.

### JTBD-02 — Consumer integrator

When a consumer selects an adopted release, the integrator needs AxBuild to resolve exactly the intended repository/tag/assets/digests through the same deterministic Store/transport boundary used by other AxBuild families.

### JTBD-03 — Release/review owner

When an existing release is adopted, the reviewer needs to prove that the adopted authority points to the exact already-qualified bytes and that no migration shortcut silently changed release identity, ownership, or artifact content.

### JTBD-04 — Platform maintainer

When additional projects later adopt existing releases, the AxBuild maintainer needs one family-neutral capability rather than per-project core logic for Axiom, Skia, Semantic, or any other specific dependency.

## 6. Primary Scenarios

### S1 — Adopt a large multi-target SDK release

A project has an existing qualified release set such as Axiom Skia with multiple target/variant artifacts. AxBuild adoption represents those exact existing artifacts without rebuilding or copying them to a new release repository.

Success means each selected artifact resolves to the already-qualified source asset and exact digest.

### S2 — Adopt a mixed host-tool/runtime release set

A project has an existing release set such as Axiom Semantic containing host-tool artifacts and target-runtime artifacts under one qualified release-set boundary.

Success means adoption can express and resolve the release as a coherent set while retaining distinct artifact kind/key/target roles.

### S3 — First online materialization

An empty AxBuild Store receives an adopted authority and valid credentials when required. AxBuild fetches only the exact frozen source assets, verifies them, materializes them, and returns deterministic machine-readable resolution facts.

### S4 — Offline replay

After S3 has populated the Store, network/release credentials are removed or network access is unavailable. The same adopted authority resolves successfully from verified Store content only.

### S5 — Source mismatch or authority ambiguity

A source tag/asset is missing, a digest differs, metadata is ambiguous, the authority points to an unapproved repository, or the source release cannot satisfy the adopted immutability/integrity contract.

AxBuild fails closed. It must not select a nearby release, floating `latest`, rebuild source, substitute a mirror identity, or create a new binary publication automatically.

### S6 — Adoption without consumer migration

An existing release can become AxBuild-adoptable and verified without changing the actual consumer repository. Adoption completion alone does not authorize Axiom or any other project to switch its build/CI path to AxBuild.

## 7. Functional Requirements

Priority vocabulary:

- `P0`: required for Phase 3A to be considered complete;
- `P1`: required for the first production-ready general capability but may be sequenced after the minimum P0 path;
- `P2`: useful extension, explicitly non-blocking for Phase 3A unless later authority promotes it.

### ERA-FR-01 — Exact source-release binding (`P0`)

An adopted release set must bind to an explicit source repository and an exact immutable release/tag identity. Floating selectors such as `latest`, unpinned branches, or search-by-version are forbidden dependency authority.

Acceptance criteria:

- two resolutions from the same adopted authority cannot legitimately choose different release identities;
- the selected source repository/tag is machine-readable and reviewer-visible;
- absence of the exact frozen source release causes failure rather than fallback.

### ERA-FR-02 — Exact artifact identity and digest (`P0`)

Every adopted binary artifact must be identified by an exact asset identity/name and cryptographic digest, with sufficient kind/key/target/variant information to select the correct artifact deterministically.

Acceptance criteria:

- an asset with the correct name but wrong bytes is rejected;
- duplicate or ambiguous artifact selectors are rejected;
- artifact selection is independent of API listing order.

### ERA-FR-03 — Preserve existing binary bytes (`P0`)

Adoption must not require rebuilding already-qualified binaries merely to satisfy AxBuild naming, metadata, or packaging conventions.

Acceptance criteria:

- a conforming adoption can complete using the bytes of the original qualified release;
- no build of Skia/Semantic or equivalent source producer is a mandatory adoption step;
- source binary digest before and after adoption is identical.

### ERA-FR-04 — Preserve source release history (`P0`)

Adoption must not require modifying the existing qualified release/tag or attaching/replacing binary content on the existing release as a migration shortcut.

Acceptance criteria:

- the original release/tag remains unchanged by adoption;
- adoption metadata can be established without mutation of original release assets;
- a source release mutation discovered after adoption invalidates or blocks resolution according to the frozen integrity contract rather than being silently accepted.

### ERA-FR-05 — Preserve release ownership (`P0`)

Adoption must not silently transfer a project-owned existing release to `Mostorm-Labs/axdeps` or another repository.

Acceptance criteria:

- source repository remains explicit authority data;
- Axiom-owned releases can remain Axiom-owned throughout Phase 3A;
- any future ownership transfer requires separate explicit authority and is not an automatic side effect of adoption.

### ERA-FR-06 — Family-neutral adoption (`P0`)

The capability must represent existing release families without embedding Axiom-, Skia-, Semantic-, NearCast-, or other project-specific semantics into AxBuild core.

Acceptance criteria:

- both the Skia-like multi-target release shape and Semantic-like host-tool/runtime release shape can be represented through the same generic capability boundary;
- project-specific validation/install behavior may remain in trusted provider/adapter code, but common adoption semantics are family-neutral;
- adding another structurally compatible existing-release family does not require modifying AxBuild core merely to add the family name.

### ERA-FR-07 — Multi-artifact release-set coherence (`P0`)

The capability must support one adopted release set containing multiple artifacts with distinct roles while retaining one coherent release-set identity.

Acceptance criteria:

- host-tool and target-runtime artifacts can belong to one adopted release set;
- multiple target/variant artifacts can coexist without identity collision;
- the resolver can select the required subset while preserving the release-set identity used for the resolution.

### ERA-FR-08 — AxBuild canonical consumption boundary (`P0`)

An adopted release must be consumable by the AxBuild family-neutral resolver/Store boundary using a deterministic machine-readable authority representation.

P02 does **not** decide whether that representation is an extension of current release-index semantics, an adoption record, a project-owned adapter output, or another design.

Acceptance criteria:

- downstream resolver input is deterministic and machine-readable;
- the resolver does not need to scrape human release notes;
- adoption authority can be validated before artifact installation.

### ERA-FR-09 — Verified online acquisition (`P0`)

With an empty Store, AxBuild must be able to obtain each selected adopted artifact from its frozen source authority, verify identity/digest, and materialize it through the normal verified Store path.

Acceptance criteria:

- fetched bytes are verified before becoming trusted Store content;
- source authentication, when required, does not alter dependency identity;
- mirrors/caches may provide bytes only when they preserve the frozen identity/digest contract.

### ERA-FR-10 — Offline replay (`P0`)

After successful verified materialization, the same adopted authority must resolve from Store with release/mirror network access unavailable.

Acceptance criteria:

- populated Store content is revalidated according to normal AxBuild rules;
- no network is required when all required adopted artifacts are present and valid;
- missing/corrupt Store content in offline mode fails closed.

### ERA-FR-11 — No hidden source-build fallback (`P0`)

Failure to acquire or validate a frozen adopted artifact must not trigger an implicit source build, repackaging step, substitute release, or automatic publication.

Acceptance criteria:

- missing locked bytes produce an explicit terminal resolution error;
- failure output identifies the missing/invalid authority or artifact;
- no producer/build pipeline is invoked as resolver fallback.

### ERA-FR-12 — Effective source immutability/integrity qualification (`P0`)

An existing release must satisfy an adoption-time immutability/integrity contract appropriate to its source system before becoming authoritative for AxBuild resolution.

P02 does not require one particular provider mechanism such as GitHub native immutable releases; later design/verification must define acceptable proof and mutation-detection behavior.

Acceptance criteria:

- adoption cannot accept a source whose effective identity/content may change undetectably;
- any accepted source mechanism has an explicit mutation-detection/fail-closed contract;
- inability to establish the required immutability/integrity property blocks adoption.

### ERA-FR-13 — Provenance preservation (`P0`)

Adoption must preserve enough provenance to demonstrate where the already-qualified release came from and that the adopted artifacts are the same qualified artifacts rather than newly produced substitutes.

Acceptance criteria:

- reviewer can trace adopted artifact -> source repository/tag/asset/digest;
- original release identity remains observable;
- adoption metadata cannot claim qualification for different bytes.

### ERA-FR-14 — Machine-readable resolution facts (`P1`)

Resolution must expose machine-readable facts sufficient for CI/debugging to identify the adopted release-set identity, selected source authority, artifact identities, Store/network source, and whether network was used.

Acceptance criteria:

- CI can distinguish source release selection from Store replay;
- facts do not contain authentication secrets;
- diagnostics can identify the exact failed authority/artifact when resolution fails.

### ERA-FR-15 — Authentication without credential authority (`P1`)

Private project-owned releases must be consumable using authorized credentials while keeping credentials outside lock/adoption identity and persistent resolution facts.

Acceptance criteria:

- credentials are not written into checked-in authority files or Store identity paths;
- credential rotation does not change dependency identity;
- lack of access fails clearly without selecting another repository/release.

### ERA-FR-16 — Adoption-state validation independent of consumer migration (`P0`)

The platform must be able to qualify an existing release as adoptable before any product repository switches its active dependency path.

Acceptance criteria:

- Phase 3A can reach its own Gate without modifying Axiom consumer build/CI;
- successful adoption does not itself authorize Axiom migration;
- Phase 4 consumer adoption can later reference Phase 3A evidence as an input rather than repeating binary qualification from scratch.

### ERA-FR-17 — No mandatory binary duplication (`P0`)

The generic adoption mechanism must not require copying large existing release assets into another GitHub release/repository solely to make them AxBuild-compatible.

Acceptance criteria:

- the authoritative source asset can remain at its existing project-owned release location;
- any optional cache/mirror copy is non-authoritative and digest-bound;
- an architecture that requires a second authoritative binary publication for every existing release does not satisfy Phase 3A.

### ERA-FR-18 — Compatibility outcome must be explicit (`P1`)

If an existing release cannot be represented safely under the eventual generic adoption contract, the system must report that the family is not adoptable under that contract rather than silently weakening identity/integrity guarantees.

Acceptance criteria:

- incompatible source-release shapes have an explicit fail/unsupported result;
- unsupported does not trigger source rebuild or automatic migration to `axdeps`;
- later lifecycle work may define a different approved path without changing Phase 3A history.

## 8. Non-Functional Requirements

### ERA-NFR-01 — Determinism (`P0`)

Given the same adoption authority and valid immutable source content, artifact selection and resolution identity must be deterministic across supported hosts.

### ERA-NFR-02 — Integrity over availability (`P0`)

When exact authority cannot be validated, the system must fail rather than maximize availability through substitution or fallback.

### ERA-NFR-03 — Family neutrality (`P0`)

Common AxBuild code must not encode release naming/layout rules specific to Axiom/Skia/Semantic as the generic contract.

### ERA-NFR-04 — Backward compatibility discipline (`P0`)

Current `axbuild-sdk-lock-v1` / `axbuild-release-index-v1` semantics remain Current Authority. P02 does not authorize a v2 contract or a breaking semantic change. If later design proves current semantics insufficient, that change must receive explicit semantic authority before implementation.

### ERA-NFR-05 — Reviewability (`P0`)

A reviewer must be able to reconstruct, from machine-readable authority/evidence, the exact source release and asset bytes that an adopted resolution is permitted to consume.

### ERA-NFR-06 — Large-artifact efficiency (`P1`)

The capability should avoid unnecessary transfer/storage multiplication for large SDK artifacts. The authoritative design must not inherently require duplicate large binary publication solely for metadata compatibility.

### ERA-NFR-07 — Credential hygiene (`P1`)

Secrets used for private release access must not become dependency identity, be persisted in locks, or appear in normal resolution facts/logs.

### ERA-NFR-08 — Existing resolver/Store behavioral consistency (`P1`)

Where the capability crosses the existing resolver/Store boundary, online/offline, digest verification, atomic materialization, and fail-closed behavior should remain consistent with AxBuild's established common behavior unless later authority explicitly changes it.

## 9. Requirement Priorities / Release Threshold

### Phase 3A blocking requirement set

The following are blocking for Phase 3A completion:

- ERA-FR-01 through ERA-FR-13;
- ERA-FR-16;
- ERA-FR-17;
- ERA-NFR-01 through ERA-NFR-05.

### Production-hardening requirement set

The following remain required for a production-ready generic capability but can be sequenced after the minimum P0 model is proven if P03/P20 explicitly preserve them:

- ERA-FR-14;
- ERA-FR-15;
- ERA-FR-18;
- ERA-NFR-06 through ERA-NFR-08.

No requirement may be silently downgraded by implementation planning.

## 10. Product Acceptance Scenarios

These are product-level acceptance outcomes. P20 later defines the independent evidence/oracles and exact Gate execution.

### AC-01 — Skia-like existing release adoption

Given a project-owned qualified Skia-like release set with multiple target/variant assets, adoption completes without rebuilding the SDK, editing the original release, or copying the authoritative binaries to `axdeps`; exact assets resolve by frozen identity/digest.

### AC-02 — Semantic-like mixed release set

Given a project-owned qualified release set containing host tools plus target runtimes, adoption represents one coherent release set and resolves the correct subset for a requested host/target without artifact ambiguity.

### AC-03 — Empty-Store online resolve

Given valid adoption authority and credentials, an empty Store obtains only exact frozen assets, verifies them, materializes them, and reports the selected release/artifact identities.

### AC-04 — Offline replay

After AC-03, with network/release credentials unavailable, the same request resolves from verified Store content with no dependency-network access.

### AC-05 — Tampered or changed source asset

If source bytes no longer match the adopted digest or the source authority cannot satisfy the frozen mutation-detection contract, resolution/adoption fails closed and no substitute/build/republication occurs.

### AC-06 — Missing exact release/tag/asset

If the exact frozen source identity is missing, AxBuild fails explicitly rather than selecting another tag, latest release, or similarly named asset.

### AC-07 — Ownership preservation

Completing Phase 3A leaves the example Axiom releases project-owned and leaves `axdeps` ownership policy unchanged.

### AC-08 — No consumer migration side effect

Completing Phase 3A does not change Axiom build files, CI, dependency locks, or runtime selection. Those remain Phase 4 work.

### AC-09 — Family-neutral extension

A third existing-release family with the same generic authority needs only family/provider/adoption configuration within the approved extension boundary; it does not require a new project-name condition in AxBuild core.

## 11. Explicit Out of Scope

Phase 3A P02 does not authorize or require:

- Axiom consumer migration;
- NearCast consumer migration;
- modification of Axiom Skia/Semantic existing releases;
- rebuilding Axiom Skia or Semantic binaries;
- moving Axiom binaries to `Mostorm-Labs/axdeps`;
- public redistribution policy changes;
- generic producer/build automation;
- dependency change classification;
- reusable producer workflows;
- automatic publication of new release sets;
- source dependency/toolchain rehosting;
- splitting NearCast AirPlay into component families;
- a specific schema/version change;
- a specific adapter/plugin/locator design;
- a UI;
- consumer repository edits.

## 12. Open Decisions Reserved for P03 / Design

P02 intentionally does not choose:

1. where adoption metadata lives;
2. whether current v1 index semantics are sufficient or a new semantic object/field is required;
3. whether source-artifact location is represented by an artifact-level locator, project-owned adapter output, or another contract;
4. how source-system immutability is proven for providers that do not expose GitHub-style `immutable=true`;
5. the exact boundary between provider-specific source discovery and family-neutral resolver input;
6. whether adoption metadata is checked into the source project, consumer project, or another authority repository;
7. how legacy releases with partial metadata are qualified as adoptable;
8. what subset of the existing qualification/publication code can be reused without making NearCast-specific behavior architectural authority.

These are downstream decisions, not requirement ambiguities.

## 13. Required Analysis for P03

P03 must trace each blocking requirement through candidate capabilities and downstream proof obligations. At minimum it must determine whether the following capability decomposition is sufficient or requires refinement:

```text
Existing Release Authority Description
        +
Source Immutability / Integrity Qualification
        +
Canonical Adoption Metadata
        +
Family-neutral Artifact Selection
        +
Verified Acquisition / Store
        +
Offline Replay
        +
Adoption Diagnostics / Evidence
```

P03 must specifically trace both reference shapes:

- Skia-like multi-target/multi-variant SDK release;
- Semantic-like host-tool + runtime release set.

P03 must not treat Axiom consumer migration as the implementation proof for Phase 3A.

## 14. Quality / Evidence Gate for P02

P02 is acceptable only if:

- every P0 requirement traces to an established value/constraint from Current Authority or preserved Phase 1.5 inventory;
- no requirement silently changes binary ownership;
- no requirement requires rebuilding/mutating existing qualified bytes;
- no requirement selects the implementation mechanism prematurely;
- product acceptance can be evaluated without performing consumer migration;
- family neutrality is explicit;
- fail-closed and online/offline behavior are explicit;
- unresolved design questions are separated from product requirements.

Review result: `READY`.

## 15. P02 Decision

```yaml
stage: P02
owner: aegis-discovery
status: READY
phase: Phase 3A Generic Existing-Release Adoption
canonical_baseline: 580adc8e015413f6a77b1952321fa6e2caa43ae4
problem_validated: true
product_research_required_before_p02: false
requirements_frozen_for_p03: true
architecture_selected: false
semantic_change_authorized: false
implementation_authorized: false
consumer_migration_authorized: false
next_stage: P03
```

## 16. Handoff

```yaml
type: stage_handoff
from_owner: aegis-discovery
from_stage: P02
to_owner: aegis-discovery
requested_stage: P03
repository: Mostorm-Labs/axbuild
canonical_baseline: 580adc8e015413f6a77b1952321fa6e2caa43ae4
requirement_artifact: docs/requirements/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P02-v0.1.md
status: READY
capability: Generic Existing-Release Adoption
constraints:
  - preserve project-owned existing releases
  - no rebuild/mutation/mandatory binary duplication
  - exact repository/tag/asset/digest authority
  - no floating latest
  - no hidden source-build fallback
  - online verified acquisition
  - offline Store replay
  - family-neutral common boundary
  - adoption is not consumer migration
```
