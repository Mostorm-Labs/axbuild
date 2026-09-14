# AxBuild Phase 3A Generic Existing-Release Adoption — P10 Product Object Model v0.1

## Stage

- Owner: `aegis-modeling`
- Stage: `P10 Product Object Model`
- Repository: `Mostorm-Labs/axbuild`
- Canonical baseline: `580adc8e015413f6a77b1952321fa6e2caa43ae4`
- Working branch: `phase3/existing-release-adoption-p02`
- Upstream requirement: `docs/requirements/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P02-v0.1.md`
- Upstream traceability: `docs/traceability/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P03-v0.1.md`
- Phase: `Phase 3 — Platform Generalization`
- Capability: `Phase 3A — Generic Existing-Release Adoption`
- Profile: `Standard`
- Status: `READY`
- Successor: `P11 Interaction / Behavior`

## 1. Role

Define the durable product concepts required to represent Generic Existing-Release Adoption before choosing wire schema, file format, module API, CLI, provider implementation, or runtime operation vocabulary.

P10 models product truth. It does not equate product objects with Python classes or existing repository types.

## 2. Authority

Current upstream authority:

- `docs/authority/AXBUILD-PLATFORM-BOUNDARY-AUTHORITY-v0.1.md`;
- `docs/requirements/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P02-v0.1.md`;
- `docs/traceability/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P03-v0.1.md`;
- preserved Phase 1.5 decisions for Axiom Skia and Semantic SDK `ADOPT EXISTING RELEASE`.

Repository code is implementation reality only. Existing `ReleaseIndexRef`, `ArtifactRef`, resolver, provider, transport, and Store types are useful anchors but do not define the P10 product model by themselves.

## 3. Objective

Freeze the minimum product object model needed to express:

```text
an already-qualified project-owned release
        +
its exact source identity and ownership
        +
proof that its identity/content can be trusted
        +
an AxBuild adoption authority
        +
a coherent adopted release set and exact artifact mappings
        +
an independent adoption qualification outcome
```

while keeping runtime resolution facts, credentials, Store cache state, mirrors, consumer activation, and implementation-specific objects outside canonical product truth.

## 4. Non-goals

P10 does **not** decide:

- JSON/schema field names;
- whether `axbuild-sdk-lock-v1` or `axbuild-release-index-v1` changes;
- whether adoption metadata lives in Axiom, AxBuild, or another repository;
- whether metadata and binary assets share one repository/tag;
- artifact-level source locator encoding;
- GitHub-specific immutability representation;
- provider/module/API ownership;
- CLI commands;
- operation names or mutation semantics;
- Axiom or NearCast consumer migration;
- any implementation plan.

Those belong to P11-P18/P20 as routed by P03.

## 5. Modeling Principles

P10 freezes these principles:

1. **Original release reality and AxBuild adoption authority are distinct concepts.**
   The project-owned release exists independently of AxBuild and must not become AxBuild-owned merely because it is adopted.
2. **Authority is explicit, never inferred from cache or transport.**
   Store paths, mirrors, downloaded files, credentials, or current API listings do not become dependency authority.
3. **Adoption authority is about permission to consume exact existing bytes, not permission to mutate or republish them.**
4. **One adopted release set may contain many artifact roles.**
   Skia-like multi-target/multi-variant and Semantic-like host-tool/runtime shapes are first-class.
5. **Qualification and consumer activation are separate.**
   Phase 3A can finish without changing any consumer repository.
6. **Historical evidence remains historical.**
   A later source contradiction must be representable without rewriting the fact that a previous qualification happened.
7. **Runtime facts are observations, not canonical authority.**

## 6. Object Classification Summary

| Object | Classification | Canonical? | Identity / ownership summary |
| --- | --- | --- | --- |
| `ExistingReleaseSource` | External Resource Reference | referenced durable truth | identifies the original project-owned release; AxBuild does not own its lifecycle |
| `AdoptionAuthority` | Aggregate Root / Durable Entity | yes | canonical AxBuild statement authorizing consumption of one exact existing release set |
| `AdoptedReleaseSet` | Entity inside `AdoptionAuthority` | yes | coherent adopted set identity spanning one or more exact artifacts |
| `AdoptedArtifactMapping` | Entity inside `AdoptedReleaseSet` | yes | maps a stable artifact role/key to one exact source asset + digest |
| `SourceIntegrityQualification` | Durable Qualification Record | yes as qualification history | records whether the external source can satisfy the required integrity/immutability contract |
| `AdoptionCompatibilityResult` | Durable Result / Value-bearing Record | yes when used for qualification history | explicit `adoptable / unsupported / invalid` classification and reason |
| `AdoptionQualificationResult` | Durable Gate-input Record | yes | Phase 3A-level conclusion, distinct from consumer activation |
| `SourceReleaseLocator` | Value Object | embedded | exact source platform/repository/release identity |
| `SourceAssetLocator` | Value Object | embedded | exact source asset identity under the original release |
| `ArtifactRoleKey` | Value Object | embedded | family-neutral artifact role selector such as kind/key/target/variant semantics |
| `ContentDigest` | Value Object | embedded | cryptographic byte identity, SHA256 in current authority |
| `OwnershipDescriptor` | Value Object | embedded | records source release owner/repository authority without transferring ownership |
| `IntegrityContract` | Value Object | embedded | declares required mutation-detection / integrity expectations, not provider implementation |
| `ProvenanceLink` | Value Object | embedded | reviewer-visible source provenance linkage |
| `AdoptionInspectionSession` | Session / Transient State | no | temporary work while inspecting/qualifying a candidate release |
| `ResolutionSession` | Session / Transient State | no | one online/offline resolution attempt |
| `ResolutionFacts` | Derived Runtime State | no | exact observed source/store/network facts for diagnostics/evidence |
| `CredentialContext` | External Secret / Transient Context | no | authorizes access but never contributes to dependency identity |
| `StoreEntry` | Runtime Resource / Derived Cache State | no | verified byte materialization; not dependency authority |
| `MirrorOrCache` | External Byte Transport Resource | no | may serve digest-bound bytes but never selects identity |
| `ConsumerActivation` | Separate Lifecycle Object | out of Phase 3A | belongs to Phase 4 and must not be embedded in adoption authority |

## 7. Core Durable Objects

### 7.1 `ExistingReleaseSource`

**Classification:** external resource reference.

Represents the original project-owned release that already exists before adoption.

Logical responsibilities:

- identify the source platform/provider;
- identify the project-owned repository/release namespace;
- bind an exact non-floating release identity;
- expose source ownership separately from AxBuild metadata ownership;
- provide the boundary against which source existence and integrity are inspected.

Examples include the existing Axiom Skia and Semantic release sets, but the object is family-neutral.

Important invariants:

- it is **not created or owned by AxBuild adoption**;
- adoption does not mutate it;
- adoption does not move it to `axdeps`;
- its lifecycle may change externally (for example source removed or content contradicted), and AxBuild must be able to detect/represent that contradiction;
- a Store copy or mirror copy is not another `ExistingReleaseSource`.

Logical identity:

```text
SourceReleaseIdentity :=
    source platform/provider
  + source repository/authority namespace
  + exact release/tag identity
```

The wire representation of this identity is reserved for P12/P17.

### 7.2 `AdoptionAuthority`

**Classification:** canonical aggregate root / durable entity.

This is the central new Phase 3A product object.

It means:

> AxBuild is authorized to treat one exact, already-qualified external release set as dependency authority under the frozen adoption contract.

It owns the canonical adoption relationship, not the original binary release.

Required semantic contents:

- family identity;
- one exact `ExistingReleaseSource` reference;
- one `AdoptedReleaseSet`;
- ownership descriptor preserving original source authority;
- integrity/qualification linkage;
- provenance linkage;
- compatibility/qualification state needed to determine whether the authority is actionable;
- enough information for later semantics to produce deterministic resolver input without inferring identity from network listing order or human release notes.

Aggregate invariants:

1. exactly one source release identity is authoritative for one `AdoptionAuthority` revision;
2. all adopted artifact mappings belong to the same adopted release-set identity;
3. each artifact role key is unique within the release set;
4. every artifact mapping has an exact source asset identity and digest;
5. no artifact mapping may silently transfer source ownership;
6. no floating selector is valid canonical state;
7. no credential, cache path, Store path, mirror URL, local filesystem path, or network session is part of canonical identity;
8. establishment of this object must not imply consumer migration.

Logical identity:

`AdoptionAuthorityId` is stable for one canonical adoption statement. P10 does not choose whether it is content-derived, assigned, or composed; P12 must freeze the identity algorithm/encoding.

Change rule:

A semantic change that selects different source release identity, artifact bytes, artifact role mapping, or ownership must not be treated as an in-place invisible edit. P12/P13 must define whether that produces a new authority identity, revision, or supersession relation.

### 7.3 `AdoptedReleaseSet`

**Classification:** durable entity within `AdoptionAuthority`.

Represents one coherent release-set identity spanning the exact existing artifacts that are adopted together.

Responsibilities:

- preserve one release-set identity across multiple artifact roles;
- support multi-target / multi-variant SDKs;
- support host tools + target runtimes under one qualification boundary;
- provide deterministic subset selection without losing set coherence;
- prevent mixing artifacts from different source release-set identities.

Logical identity:

`AdoptedReleaseSetId` identifies the coherent set, not one asset and not one consumer request.

Invariants:

- at least one artifact mapping exists;
- no duplicate `ArtifactRoleKey`;
- all mappings trace to the frozen source release authority or an explicitly modeled source relation later approved by P12;
- selecting a subset at runtime does not create a different release-set identity;
- host-tool/runtime and target/variant distinctions are roles within the set, not separate ad-hoc downloads.

### 7.4 `AdoptedArtifactMapping`

**Classification:** durable child entity.

Represents one exact mapping from a family-neutral artifact role to one exact existing source asset.

Required logical contents:

- `ArtifactRoleKey`;
- stable artifact identity used by the adoption model;
- `SourceAssetLocator`;
- `ContentDigest`;
- optional size/shape metadata when needed for deterministic validation/selection;
- provenance linkage sufficient to show this is the already-qualified source asset.

Invariants:

- role key is unique inside the release set;
- source asset identity is exact and non-floating;
- digest is mandatory for authoritative binary content;
- same-name/different-bytes is a mismatch, not a valid alternate;
- listing order is never identity;
- one mapping cannot silently resolve to a different release/tag when credentials, cache state, or API ordering changes.

### 7.5 `SourceIntegrityQualification`

**Classification:** durable qualification record.

Represents the result of evaluating whether the external source release can satisfy Phase 3A's required immutability/integrity contract without mutating the source release.

It is deliberately distinct from `ExistingReleaseSource` because source reality and AxBuild's qualification of that reality are different facts.

Logical contents:

- source release identity being qualified;
- `IntegrityContract` applied;
- observed/proven source properties;
- exact artifact digest coverage relevant to adoption;
- qualification outcome;
- evidence/provenance references;
- time/revision context sufficient for later review without making wall-clock time itself authority.

Invariants:

- qualification cannot change the source release;
- `qualified` cannot be asserted if source mutation could occur undetectably under the selected contract;
- inability to establish required integrity is explicit, not converted into availability fallback;
- later contradiction does not erase historical qualification evidence; P13 must define invalidation/supersession semantics.

P10 does not require GitHub `immutable=true`; the product object is provider-neutral.

### 7.6 `AdoptionCompatibilityResult`

**Classification:** durable result record / value-bearing product result.

Purpose: make compatibility explicit rather than weakening guarantees.

Canonical outcome vocabulary at the product level:

```text
ADOPTABLE
UNSUPPORTED
INVALID
```

Meaning:

- `ADOPTABLE`: the release shape can be represented without violating P02 requirements;
- `UNSUPPORTED`: current approved adoption contract cannot safely represent the source shape, but source itself is not necessarily corrupt;
- `INVALID`: source authority/content fails required identity/integrity constraints.

P11/P13 will define transition/operation semantics and whether additional machine statuses are required.

Important invariant: `UNSUPPORTED` must never mean "silently rebuild", "silently republish", or "move to axdeps".

### 7.7 `AdoptionQualificationResult`

**Classification:** durable Phase 3A qualification result.

Represents whether a specific adoption authority has satisfied the Phase 3A qualification boundary independently of consumer migration.

Logical contents:

- exact adoption authority identity/revision;
- qualification outcome;
- links to `SourceIntegrityQualification` and compatibility result;
- required proof/evidence references as later defined by P20;
- result suitable as an input to a later Phase 4 consumer lifecycle.

Invariants:

- it cannot assert that Axiom/NearCast consumer migration has occurred;
- it cannot mutate consumer locks/build files/CI;
- a later consumer lifecycle may reference it but must separately authorize activation;
- qualification of one authority does not qualify a different source release or different bytes.

## 8. Value Objects

### 8.1 `SourceReleaseLocator`

Logical immutable value identifying one exact source release.

Must eventually encode enough information to avoid:

- floating/latest lookup;
- ambiguous repository;
- ambiguous tag/release identity;
- identity changes caused by credentials or listing order.

P12/P17 own provider-specific encoding.

### 8.2 `SourceAssetLocator`

Exact source asset identity under the source release.

It must not be interpreted as "find something similarly named".

### 8.3 `ArtifactRoleKey`

Family-neutral semantic role used to distinguish artifacts within one release set.

Conceptually covers dimensions such as:

```text
kind
key
host role / runtime role
target
variant
```

P10 does not require all dimensions to be separate schema fields. P12 decides canonical field structure.

### 8.4 `ContentDigest`

Cryptographic byte identity. Current upstream authority requires SHA256.

Properties:

- immutable value;
- normalized comparison;
- participates in integrity, Store identity, and reviewer reconstruction;
- must not be replaced by filename, release ID, size, ETag, or cache key alone.

### 8.5 `OwnershipDescriptor`

States who owns the original release authority.

Important distinction:

```text
metadata host / adoption authority owner
        != automatically
binary source release owner
```

This value exists specifically to prevent silent authority transfer.

### 8.6 `IntegrityContract`

Provider-neutral statement of what must be true for source identity/content to be considered safely immutable or mutation-detectable.

P10 freezes the concept, not provider-specific checks.

Potential semantic concerns for P12/P17 include release immutability, digest verification, stable source identity, mutation detection, and fail-closed behavior.

### 8.7 `ProvenanceLink`

Reviewer-visible linkage from adopted artifact/authority to original qualified source identity and qualification evidence.

It is not itself permission to consume different bytes.

## 9. Sessions and Transient State

### 9.1 `AdoptionInspectionSession`

**Classification:** transient session; not canonical authority.

May contain:

- fetched source metadata;
- enumerated assets;
- temporary candidate mappings;
- validation progress;
- credential/access errors;
- temporary download locations;
- evidence generation work state.

None of these become authority until an explicit later behavior/operation establishes durable canonical objects.

Cancellation or failure must not leave a partially authoritative adoption state. P11/P13 own exact commit/cancel semantics.

### 9.2 `ResolutionSession`

One online or offline resolution attempt.

May observe:

- request target;
- selected artifact subset;
- Store hits/misses;
- network access;
- download/materialization state;
- provider validation state.

It is runtime/transient and cannot rewrite `AdoptionAuthority` merely because a network source is temporarily unavailable.

### 9.3 `CredentialContext`

External transient secret context.

Invariants:

- never part of `AdoptionAuthorityId`;
- never part of `AdoptedReleaseSetId`;
- never persisted into ordinary resolution facts;
- rotation does not change dependency identity;
- denial causes explicit access failure, not repository substitution.

## 10. Derived / Non-Canonical State

### 10.1 `ResolutionFacts`

Derived runtime output useful for diagnostics, CI, and evidence.

May report:

- family;
- adoption/release-set identity;
- original source repository/tag identity;
- selected artifact identities/digests;
- Store vs network source;
- `networkUsed`;
- materialized locations as runtime observations;
- explicit failure/unsupported reason where appropriate.

Must not contain secrets.

`ResolutionFacts` are not the authority from which future resolution identity is chosen.

### 10.2 Store / materialized package state

Store entries are verified runtime resources, not product authority.

A Store hit proves bytes are locally available and valid under the frozen digest; it does not select a new release identity.

### 10.3 Mirror/cache state

Mirrors/caches are byte sources only.

They cannot:

- choose a different release;
- change ownership;
- become canonical because the original source is temporarily unavailable.

## 11. External Resources

Phase 3A depends on external systems but does not own them:

- project-owned release repository and release objects;
- release-provider APIs such as GitHub Releases;
- authentication service/token issuance;
- network transport;
- optional mirror/cache infrastructure;
- filesystem/Store resources.

P17 later defines platform contracts. P10 only freezes that these are external resources, not canonical product objects.

## 12. Aggregate Boundary

P10 freezes one primary canonical aggregate:

```text
AdoptionAuthority                         [aggregate root]
  |
  +-- ExistingReleaseSource reference    [external authority reference]
  |
  +-- OwnershipDescriptor
  |
  +-- AdoptedReleaseSet                  [entity]
  |     |
  |     +-- AdoptedArtifactMapping *     [entities]
  |           +-- ArtifactRoleKey
  |           +-- SourceAssetLocator
  |           +-- ContentDigest
  |           +-- ProvenanceLink
  |
  +-- SourceIntegrityQualification ref
  +-- AdoptionCompatibilityResult ref/value
```

Separate durable result:

```text
AdoptionQualificationResult
  -> exact AdoptionAuthority identity/revision
  -> qualification evidence/result
  -> reusable by later Phase 4
```

This separation is intentional:

- authority says **what exact existing release may be consumed**;
- qualification says **whether that authority has passed the Phase 3A proof boundary**;
- consumer activation later says **whether a product actually switched to it**.

These must not collapse into one object.

## 13. Lifecycle Boundaries for P11

P10 freezes lifecycle categories but leaves transition behavior to P11.

### Source release

```text
external existing
    -> inspected by AxBuild
    -> may remain available/consistent
    -> may later become missing/contradictory externally
```

AxBuild does not own source creation/deletion lifecycle.

### Adoption candidate/session

```text
not canonical
    -> inspect / map / qualify
    -> cancel/fail/unsupported
    OR
    -> explicit establishment boundary
```

### Adoption authority

```text
established canonical authority
    -> valid/actionable while required qualification/integrity remains satisfied
    -> later contradiction must be represented explicitly
```

P11/P13 must decide whether later contradiction means `invalidated`, `superseded`, non-actionable derived validity, or another authority-safe model. P10 does not silently choose mutation semantics.

### Adoption qualification result

```text
not evaluated
    -> qualification result recorded
    -> historical result preserved
```

Later source contradiction may affect current validity but must not rewrite historical evidence.

### Consumer activation

Separate Phase 4 lifecycle. No Phase 3A transition enters an `active consumer` state.

## 14. Identity Rules

P10 freezes logical identity requirements:

1. `ExistingReleaseSource` identity depends on exact external source authority, never on local Store path.
2. `AdoptedReleaseSetId` identifies one coherent set, not one selected runtime subset.
3. `AdoptedArtifactMapping` identity is stable within a release set and cannot depend on API enumeration order.
4. `ContentDigest` is mandatory byte identity for adopted binary assets.
5. credential identity is excluded.
6. mirror/cache identity is excluded.
7. materialized filesystem path is excluded.
8. consumer repository/branch is excluded from Phase 3A adoption identity.
9. changing source release identity or authoritative bytes is semantically significant and cannot be an invisible in-place update.

P12 owns exact canonical ID fields/algorithms.

## 15. Skia Reference-Shape Object Trace

For a Skia-like existing SDK release:

```text
ExistingReleaseSource
  repository: project-owned Axiom release authority
  exact release: skia-sdk-r1-full-v1-54c1999dc79d094d
        |
        v
AdoptionAuthority
  family: skia
  AdoptedReleaseSet
    +-- artifact mapping: Windows release
    +-- artifact mapping: Windows debug
    +-- artifact mapping: Web
    +-- artifact mapping: Apple
    +-- artifact mapping: Android
    +-- ... exact qualified target/variant roles
```

P10 requirement:

- all artifact mappings remain one coherent adopted release set;
- selecting one target later does not imply the other artifacts are unrelated downloads;
- none of the source binaries must be copied to `axdeps` merely to construct the aggregate.

## 16. Semantic Reference-Shape Object Trace

For a Semantic-like existing release:

```text
ExistingReleaseSource
  repository: project-owned Axiom release authority
  exact release: semantic-sdk-v2-14e3d492c9b7f970
        |
        v
AdoptionAuthority
  family: semantic
  AdoptedReleaseSet
    +-- host-tool artifact mappings
    |     +-- Linux
    |     +-- Windows
    |     +-- macOS
    |
    +-- runtime artifact mappings
          +-- desktop/mobile/web targets as published
```

P10 requirement:

- host tools and runtimes may have distinct artifact roles;
- they remain members of one coherent adopted release-set authority when that is the source qualification boundary;
- runtime selection cannot silently mix another release set's host tools.

## 17. Boundary Against Existing Implementation Objects

Current repository model contains `ReleaseIndexRef`, `ArtifactRef`, `ProviderPlan`, `ReleaseIndex`, and `ResolutionResult`.

P10 classification:

```text
existing types = implementation anchors
not automatically = canonical product object model
```

Likely conceptual alignment exists:

- `ArtifactRef` resembles part of `AdoptedArtifactMapping`;
- `ReleaseIndexRef` resembles part of authority lookup;
- `ReleaseIndex` resembles part of coherent release-set metadata;
- `ResolutionResult.facts` resembles derived `ResolutionFacts`.

But P10 deliberately does not claim one-to-one mapping.

The known P03 compatibility issue remains open: current resolver requires artifact repository/tag to match verified index repository/tag. P10's separation of `ExistingReleaseSource` from `AdoptionAuthority` means P12 must explicitly decide whether current v1 semantics can encode the model without semantic change or require a new canonical representation.

## 18. Requirement Coverage Check

| Requirement concern | P10 object coverage |
| --- | --- |
| exact source release | `ExistingReleaseSource`, `SourceReleaseLocator` |
| exact artifact bytes | `AdoptedArtifactMapping`, `SourceAssetLocator`, `ContentDigest` |
| preserve bytes/history | external-source boundary + `SourceIntegrityQualification` |
| preserve ownership | `OwnershipDescriptor`, external `ExistingReleaseSource` |
| family neutrality | generic `AdoptionAuthority` / release-set / artifact-role model |
| multi-artifact coherence | `AdoptedReleaseSet` aggregate entity |
| canonical consumption boundary | `AdoptionAuthority` |
| source integrity | `IntegrityContract`, `SourceIntegrityQualification` |
| provenance/reviewability | `ProvenanceLink`, qualification records |
| diagnostics | derived `ResolutionFacts` |
| credentials not authority | transient `CredentialContext` |
| independent adoption Gate | `AdoptionQualificationResult` |
| unsupported outcome | `AdoptionCompatibilityResult` |
| no mandatory duplication | external source remains authoritative; mirror/Store are non-authoritative resources |
| consumer separation | `ConsumerActivation` explicitly outside aggregate / Phase 3A |

All P02 blocking concerns remain representable.

## 19. Required Analysis for P11

P11 must now define behavior for at least:

1. begin inspection of an `ExistingReleaseSource`;
2. transient discovery/mapping state;
3. integrity qualification success/failure/unsupported;
4. compatibility evaluation;
5. explicit establishment of `AdoptionAuthority`;
6. cancel before establishment with zero canonical mutation;
7. retry after transient access/network failure;
8. validate an established authority;
9. later source contradiction/mutation detection;
10. online resolution and offline replay behavior at the product level;
11. why resolution does not mutate authority merely because transport/cache conditions differ;
12. why adoption establishment does not activate any consumer.

P11 must explicitly distinguish:

```text
transient inspection
vs
canonical authority establishment
vs
qualification result
vs
runtime resolution
vs
consumer activation
```

## 20. Quality / Evidence Gate for P10

P10 is acceptable only if:

- every P02/P03 durable concept is representable: **PASS**;
- original release ownership remains external and preserved: **PASS**;
- canonical adoption authority is distinct from source release and runtime cache: **PASS**;
- multi-artifact release-set coherence is first-class: **PASS**;
- Skia and Semantic reference shapes fit the same object model: **PASS**;
- credentials/Store/mirror/runtime facts are non-canonical: **PASS**;
- qualification is distinct from consumer activation: **PASS**;
- current code is not silently promoted to architecture authority: **PASS**;
- P12 semantic compatibility question remains open rather than prematurely resolved: **PASS**;
- no implementation or schema version is authorized: **PASS**.

## 21. P10 Decision

```yaml
stage: P10
owner: aegis-modeling
status: READY
phase: Phase 3A Generic Existing-Release Adoption
canonical_baseline: 580adc8e015413f6a77b1952321fa6e2caa43ae4

primary_aggregate:
  AdoptionAuthority

durable_objects:
  - AdoptionAuthority
  - AdoptedReleaseSet
  - AdoptedArtifactMapping
  - SourceIntegrityQualification
  - AdoptionCompatibilityResult
  - AdoptionQualificationResult

external_authority_resource:
  ExistingReleaseSource

noncanonical_runtime_state:
  - AdoptionInspectionSession
  - ResolutionSession
  - ResolutionFacts
  - CredentialContext
  - StoreEntry
  - MirrorOrCache

consumer_activation_in_scope: false
semantic_schema_selected: false
schema_version_change_authorized: false
implementation_authorized: false

next_stage: P11
```

## 22. Handoff

```yaml
type: stage_handoff
from_owner: aegis-modeling
from_stage: P10
to_owner: aegis-modeling
requested_stage: P11
repository: Mostorm-Labs/axbuild
canonical_baseline: 580adc8e015413f6a77b1952321fa6e2caa43ae4
working_branch: phase3/existing-release-adoption-p02
requirement_artifact: docs/requirements/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P02-v0.1.md
traceability_artifact: docs/traceability/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P03-v0.1.md
product_object_model: docs/modeling/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P10-v0.1.md
status: READY
preserve:
  - project-owned source release remains external authority
  - AdoptionAuthority is canonical aggregate root
  - multi-artifact release-set coherence
  - exact source release / asset / digest identity
  - qualification distinct from consumer activation
  - credentials, Store, mirrors, and runtime facts are non-canonical
open_for_P11:
  - start/transient/commit/cancel/retry semantics
  - qualification lifecycle
  - authority establishment boundary
  - later source contradiction behavior
  - resolution vs authority mutation boundary
```