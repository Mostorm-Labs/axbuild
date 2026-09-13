# AxBuild Phase 3A Generic Existing-Release Adoption — P11 Interaction / Behavior v0.1

## Stage

- Owner: `aegis-modeling`
- Stage: `P11 Interaction / Behavior`
- Repository: `Mostorm-Labs/axbuild`
- Canonical baseline: `580adc8e015413f6a77b1952321fa6e2caa43ae4`
- Working branch: `phase3/existing-release-adoption-p02`
- Upstream requirement: `docs/requirements/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P02-v0.1.md`
- Upstream traceability: `docs/traceability/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P03-v0.1.md`
- Upstream product model: `docs/modeling/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P10-v0.1.md`
- Phase: `Phase 3 — Platform Generalization`
- Capability: `Phase 3A — Generic Existing-Release Adoption`
- Profile: `Standard`
- Status: `READY`
- Successor: `P12 Semantic Schema`

## 1. Role

Define the user/system interaction and lifecycle behavior for Generic Existing-Release Adoption before choosing wire schema, file format, operation names, module APIs, CLI syntax, or implementation ownership.

P11 freezes start/transient/commit/cancel/retry/result semantics. It distinguishes:

1. inspecting an existing external release;
2. qualifying source integrity and adoption compatibility;
3. explicitly establishing canonical `AdoptionAuthority`;
4. validating/using an already-established authority;
5. handling later source contradictions without rewriting history;
6. resolving adopted artifacts online/offline without mutating canonical authority;
7. keeping Phase 3A adoption separate from Phase 4 consumer activation.

## 2. Authority

P11 is constrained by:

- `AXBUILD-PLATFORM-BOUNDARY-AUTHORITY-v0.1`;
- P02 Product Requirement;
- P03 Capability Traceability;
- P10 Product Object Model.

P11 must preserve:

- original project-owned binary ownership;
- exact source repository/release/asset/digest authority;
- no floating selectors;
- no source rebuild or automatic republication fallback;
- no mandatory duplicate authoritative binary copy;
- family-neutral common behavior;
- online verified acquisition and offline Store replay;
- adoption qualification independent of consumer migration;
- historical qualification/evidence must not be rewritten when later source reality contradicts it.

## 3. Behavioral Principles

### BP-01 — Inspection is read-only

Inspecting a candidate `ExistingReleaseSource` may query source metadata/assets and produce transient observations. It does not create canonical `AdoptionAuthority` and does not mutate the source release.

### BP-02 — Qualification and authority establishment are separate commits

A source may be inspected and qualified without yet becoming canonical dependency authority.

The first durable commit boundary is a qualification result/record. The second, separate commit boundary is establishment of `AdoptionAuthority`.

### BP-03 — Authority establishment is explicit

`AdoptionAuthority` never appears merely because a resolver successfully downloaded bytes, because a Store entry exists, or because a release looked compatible during inspection.

### BP-04 — Resolution is not an authority mutation

Resolving an established authority may create/update runtime Store state and derived `ResolutionFacts`, but must not silently change the authority, ownership, release-set identity, artifact mappings, or qualification history.

### BP-05 — Contradictions fail closed before any durable repair

If runtime validation detects that current source reality contradicts the frozen authority/integrity contract, the current attempt fails immediately. The system must not keep using alternate bytes, choose a nearby release, rebuild, republish, or silently edit authority.

### BP-06 — History is append/supersede, not rewrite

A later contradiction does not erase the historical fact that qualification previously occurred. Any durable invalidation or supersession is a new canonical fact linked to the prior authority/history. P13 will define mutation vocabulary.

### BP-07 — Cancel before commit means no canonical mutation

Transient inspection/qualification/establishment work may be abandoned before its relevant durable commit. Partial observations, temp downloads, or temporary credentials do not become canonical truth.

### BP-08 — Retry never weakens identity

Retry may repeat the same exact-authority behavior after a transient environmental failure. Retry must never broaden selectors, drop digest verification, switch repository ownership, invoke a producer, or select another release.

### BP-09 — Offline replay uses frozen authority, not source discovery

Offline replay may rely on established canonical authority plus verified Store content. It does not perform release discovery or silently reinterpret external source state.

### BP-10 — Adoption completion is not consumer activation

No P11 behavior changes Axiom/NearCast consumer build files, CI, product locks, or active runtime dependency selection.

## 4. Behavioral States

P11 freezes semantic lifecycle states, not wire enum names.

### 4.1 Candidate / inspection state

A candidate existing release can be under transient inspection.

This state is not canonical authority. It may terminate as:

- inspection completed with observations;
- transient failure;
- cancelled.

### 4.2 Qualification outcome

Qualification produces a durable outcome when explicitly committed:

- `ADOPTABLE` — source and mapping satisfy the frozen qualification contract;
- `UNSUPPORTED` — source shape/integrity mechanism cannot satisfy the current generic adoption contract without weakening guarantees;
- `INVALID` — exact source/mapping/integrity inputs contradict required authority guarantees.

Names are semantic labels for P11; exact schema encoding belongs to P12.

Qualification outcome alone does not create `AdoptionAuthority`.

### 4.3 Established authority

An `AdoptionAuthority` becomes canonical only after explicit establishment commit using an `ADOPTABLE` compatible qualification state and exact release/artifact mappings.

Established means:

- the canonical adoption statement exists;
- exact source release and artifact mappings are frozen;
- the authority may be considered for validation/resolution subject to its current actionability state;
- no consumer migration is implied.

### 4.4 Non-actionable authority

An authority can become known to be non-actionable because of a later source contradiction or explicit supersession/invalidation.

P11 freezes the behavior that a known non-actionable authority must not resolve successfully.

P12/P13 will define the durable state representation and mutation relation. Historical qualification/authority records remain addressable for audit.

## 5. Flow A — Inspect Existing Release

### Start

Inputs conceptually include:

- candidate `ExistingReleaseSource` identity;
- intended family/release-set context;
- optional credentials as transient access context;
- expected qualification policy/context.

### Transient work

The system may:

- query exact release/tag metadata;
- enumerate or look up source assets;
- observe provider integrity/immutability signals;
- calculate or verify asset digests where required;
- construct candidate artifact-role mappings;
- collect provenance observations.

### Canonical mutation

None.

### Successful result

A deterministic inspection result suitable as input to qualification.

### Cancel

Allowed before qualification commit. Cancellation produces no canonical authority or qualification mutation.

### Retry

Allowed for transient provider/network/authentication failures using the same candidate source identity. Changed credentials may be supplied without changing dependency identity.

### Terminal/fail-closed conditions

Examples:

- exact release/tag absent;
- asset identity ambiguous;
- required source metadata structurally unusable;
- explicit source identity contradiction.

No alternate release may be selected automatically.

## 6. Flow B — Qualify Existing Release

### Start

Qualification consumes:

- exact source identity;
- inspection observations;
- candidate release-set/artifact mappings;
- applicable `IntegrityContract`;
- provenance inputs.

### Transient work

The system evaluates:

- exact source release identity;
- artifact existence and unambiguous mapping;
- digest coverage;
- effective source immutability/mutation-detection property;
- family-neutral representability;
- release-set coherence;
- ownership preservation;
- whether adoption would require forbidden source mutation/rebuild/mandatory republish.

### Qualification commit

An explicit commit may persist durable:

- `SourceIntegrityQualification`;
- `AdoptionCompatibilityResult`;
- supporting provenance/evidence references.

This commit does **not** establish `AdoptionAuthority`.

### Commit outcomes

#### `ADOPTABLE`

The candidate satisfies the current Phase 3A qualification contract and may proceed to explicit authority establishment.

#### `UNSUPPORTED`

The source/release shape cannot be safely represented under current authority/design without weakening guarantees. No source modification, rebuild, automatic `axdeps` transfer, or hidden republish occurs.

#### `INVALID`

Observed source facts contradict the required exact identity/integrity contract.

### Cancel

Before qualification commit: no durable qualification record is created.

After qualification commit: the record is historical and cannot be cancelled away; a later requalification may create another explicit record according to P12/P13 semantics.

### Retry

Transient errors may be retried without changing exact authority inputs.

A committed `UNSUPPORTED`/`INVALID` result does not become `ADOPTABLE` merely by retrying the identical facts. A new result requires changed source reality, changed approved semantic contract, corrected mapping, or another explicit changed input that later stages define.

## 7. Flow C — Establish Adoption Authority

### Start

Authority establishment requires conceptually:

- exact `ExistingReleaseSource`;
- compatible `AdoptedReleaseSet` candidate;
- complete exact `AdoptedArtifactMapping` set;
- valid source integrity qualification;
- `ADOPTABLE` compatibility result;
- ownership/provenance linkage.

### Preconditions

Establishment must fail if:

- qualification is missing or non-adoptable;
- source identity is floating/ambiguous;
- any artifact mapping is missing exact source asset identity or digest;
- role keys collide or release-set coherence is broken;
- ownership would silently transfer;
- establishment would require mutating the original source release;
- required source integrity contract cannot be satisfied.

### Transient work

The system may normalize/check the candidate model and revalidate relevant frozen facts before commit.

### Authority commit

Establishment is an atomic canonical commit of the adoption statement.

The semantic commit contains one coherent authority relation:

```text
AdoptionAuthority
  -> exact ExistingReleaseSource
  -> one AdoptedReleaseSet
  -> exact AdoptedArtifactMapping set
  -> ownership/provenance linkage
  -> qualification linkage
```

No partially established authority is valid canonical state.

### Successful result

A canonical established adoption authority that may later be validated/resolved.

### Cancel

Allowed before commit; no canonical authority is created.

After commit, it cannot be “cancelled.” Later changes require explicit supersession/invalidation behavior rather than deletion/rewriting.

### Retry / idempotency expectation

Retrying establishment for semantically identical exact input must not create conflicting canonical truth. P13 must define the exact idempotency/duplicate rule.

If source identity, artifact bytes, role mapping, ownership, or integrity contract materially differs, the system must not silently overwrite the existing authority. P12/P13 must define revision/new-identity/supersession semantics.

## 8. Flow D — Validate Established Authority

### Purpose

Validate whether an already-established authority is currently safe/actionable under its frozen semantic/integrity contract.

### Start

Input: exact canonical `AdoptionAuthority` identity/revision plus any platform access needed for online validation.

### Behavior

Validation may check:

- canonical structure and semantic invariants;
- known invalidation/supersession state;
- source release existence/identity where online validation is required;
- source integrity/mutation-detection signals;
- exact artifact identity/digest expectations;
- qualification linkage.

### Canonical mutation

Pure validation is read-only.

If a contradiction is discovered, the current validation fails. Persisting that contradiction as a durable invalidation/supersession is a **separate explicit canonical behavior** owned by P13 mutation design.

### Successful result

Authority is currently valid/actionable for the requested operation under the available proof contract.

### Failure result

Explicit non-actionable/contradiction result. No fallback authority is selected.

### Offline note

Offline validation may only establish what is knowable from canonical authority + durable qualification + local verified Store state. It must not pretend to have re-observed external source reality.

P17/P18/P20 must later define freshness/revalidation obligations so this distinction is testable.

## 9. Flow E — Online Resolve Adopted Release

### Start

Inputs:

- one exact established/actionable `AdoptionAuthority`;
- resolution target/request;
- Store root/runtime context;
- optional transient credential context;
- optional non-authoritative mirror/cache transport.

### Preconditions

- authority canonical invariants valid;
- authority not known invalidated/superseded for selection;
- artifact subset selection is deterministic and coherent;
- exact source asset identity/digests available.

### Transient work

```text
AdoptionAuthority
  -> select exact artifact role subset
  -> locate exact original source asset authority
  -> fetch via source/mirror transport
  -> verify digest before trust
  -> materialize/reuse Store
  -> provider-specific install/validate
  -> emit ResolutionFacts
```

### Canonical mutation

None to `AdoptionAuthority`, qualification history, or source ownership.

Store population/materialization is runtime state, not canonical product-authority mutation.

### Successful result

Exact selected artifact set is materialized/usable and derived facts identify:

- adoption/release-set identity;
- exact artifact identities/digests;
- source/store/mirror transport observation;
- network-used observation;
- no credentials.

### Retry

Retry is allowed for transient transfer/provider access errors while preserving exact identity.

### Fail-closed / non-retry-as-fallback

The current attempt must terminate without substitution on:

- digest mismatch;
- missing exact tag/asset;
- ambiguous mapping;
- known source contradiction;
- invalid/non-actionable authority;
- release-set coherence violation.

Authentication denial may be retried with corrected credentials, but never by switching repository/release identity.

## 10. Flow F — Offline Replay

### Start

The same exact canonical authority/request is evaluated with dependency network access disabled/unavailable.

### Preconditions

- authority is not known non-actionable;
- all required exact bytes/materializations exist in verified Store state or can be produced from verified local Store archives without network;
- local content validates against frozen digest/structural rules.

### Behavior

```text
same AdoptionAuthority
  -> same artifact selection
  -> Store lookup
  -> digest/package validation
  -> materialize/reuse locally
  -> emit ResolutionFacts(networkUsed=false)
```

### Canonical mutation

None.

### Success

Same release-set/artifact identity is reproduced from Store with zero dependency-network access.

### Failure

Missing/corrupt Store state fails explicitly.

Offline mode must not:

- contact source release platform;
- select another release;
- download from mirror;
- invoke source build;
- republish artifacts.

### Retry

A failed offline attempt can be retried offline after local Store state is corrected by an explicitly separate process. It must not automatically switch itself into online mode.

## 11. Flow G — Detect Later Source Contradiction

This flow is essential because P10 separates historical qualification from later external source reality.

### Detection triggers

Examples include:

- exact release/tag removed or replaced;
- source asset absent;
- source bytes no longer match frozen digest;
- provider integrity/immutability condition no longer satisfies the authority contract;
- source identity/ownership relation contradicts frozen authority;
- previously assumed source facts become demonstrably invalid.

### Immediate behavior

The current online validation/resolution attempt must fail closed.

It must not:

- continue using newly changed bytes;
- select a nearby release;
- silently use a cache under a different authority interpretation;
- rewrite historical qualification;
- rebuild/repackage;
- transfer ownership;
- mutate the source release.

### Durable behavior boundary

The contradiction observation itself does not silently edit canonical authority.

A separate explicit canonical action must record invalidation/supersession/non-actionability according to P12/P13 semantics.

After such durable state is established, future resolution attempts must fail/redirect only according to explicit successor authority—not implicit fallback.

### Historical preservation

Prior `SourceIntegrityQualification`, compatibility result, and authority history remain inspectable as historical facts.

## 12. Flow H — Requalification / Successor Authority

P11 freezes that changed release identity or changed bytes are **not** an in-place edit of the old authority.

A later valid source version may undergo:

```text
inspect
  -> qualify
  -> establish new/revised authority
  -> explicit supersession relation to prior authority
```

Exact identity/revision/supersession representation is reserved for P12/P13.

No “update to latest” behavior exists.

## 13. Flow I — Consumer Activation Boundary

Phase 3A ends at safe adoption authority/qualification.

A later Phase 4 consumer migration may consume the established authority/evidence, but it is a separate interaction lifecycle.

P11 explicitly forbids the following as side effects of Phase 3A flows:

- editing Axiom/NearCast consumer repositories;
- replacing product dependency URLs/locks;
- changing product CI acquisition path;
- changing runtime product dependency selection;
- asserting that publication/adoption alone activates a consumer.

## 14. Cancel Semantics Matrix

| Flow | Cancel before commit | After commit |
| --- | --- | --- |
| Inspect | discard transient session/observations | no canonical commit exists |
| Qualify | no durable qualification result | cannot erase; later record may supersede/requalify |
| Establish authority | no authority created | cannot cancel; explicit invalidation/supersession required |
| Validate | stop validation, no canonical mutation | N/A unless separate invalidation commit requested |
| Online resolve | stop attempt; temp/runtime cleanup | completed Store/runtime state may remain valid derived state; authority unchanged |
| Offline resolve | stop attempt; no authority mutation | same |
| Durable invalidation/supersession | P13 defines atomic pre-commit cancellation | once committed, history preserved; successor mutation required |

## 15. Retry Classification

### Retryable without semantic change

- transient network errors;
- temporary GitHub/provider service errors;
- authentication failure with corrected credentials;
- interrupted temp download before trust;
- transient Store lock contention;
- transient filesystem/materialization failure where no invalid package was committed.

### Not retryable by weakening authority

- digest mismatch;
- missing exact source release/tag when that exact identity is required;
- ambiguous asset identity;
- release-set coherence violation;
- incompatible/unsupported source shape;
- inability to establish required integrity property;
- known invalidated authority.

These can only proceed after an explicit changed input/authority/design condition—not by relaxed retry.

## 16. Atomicity Expectations for P13

P11 requires P13 to define atomic behavior for at least:

1. qualification-result commit;
2. `AdoptionAuthority` establishment;
3. durable invalidation/non-actionability recording;
4. successor/supersession relation establishment.

At no time may partially written canonical state create an apparently actionable authority lacking complete source/artifact/integrity linkage.

## 17. Idempotency Expectations for P13

P11 requires P13 to make explicit:

- repeated pure inspection/validation is observational and non-mutating;
- same exact qualification inputs may be recomputed, but durable duplicate-record policy must be explicit;
- repeated authority-establishment request for semantically identical content cannot create conflicting authorities;
- repeated invalidation of the same authority/reason cannot create inconsistent actionability;
- resolution retries may populate/reuse Store idempotently but do not mutate authority.

P11 does not freeze IDs/idempotency keys.

## 18. Derived State vs Canonical State

### Canonical/durable product truth

- established `AdoptionAuthority`;
- coherent adopted release-set/artifact mapping;
- qualification history;
- compatibility outcome;
- explicit durable invalidation/supersession history when later defined.

### Transient/derived/runtime state

- inspection session;
- API response/cache;
- credentials;
- temp download;
- local archive path;
- Store/materialized path;
- mirror response;
- current network availability;
- resolution session;
- `ResolutionFacts` observation.

A transient fact must never silently become authority just because a run succeeded.

## 19. Failure Behavior Register

| Failure | P11 behavior |
| --- | --- |
| exact release/tag missing | fail exact operation; no nearby/floating fallback |
| asset missing/ambiguous | fail; do not select by listing order |
| digest mismatch | fail closed before trust |
| integrity proof unavailable | qualification `UNSUPPORTED`/`INVALID` as appropriate; no authority establishment |
| credentials denied | fail access; retry with credentials allowed; identity unchanged |
| Store corrupt | offline/resolve failure; do not trust corrupt bytes |
| source changed after adoption | current online validation/resolve fails; explicit invalidation path required; history preserved |
| provider-specific incompatible layout | explicit unsupported/failure; no generic guarantee weakening |
| authority already superseded/invalidated | not actionable; no implicit fallback |
| consumer not migrated | not a Phase 3A failure; adoption remains independently valid |

## 20. Behavioral Invariants

P11 freezes these invariants:

- **BI-01:** inspection alone never creates canonical authority.
- **BI-02:** qualification alone never activates a consumer.
- **BI-03:** only explicit authority establishment creates canonical adoption authority.
- **BI-04:** resolution never silently edits adoption authority.
- **BI-05:** source ownership is unchanged by inspection, qualification, authority establishment, or resolution.
- **BI-06:** cancellation before commit leaves no partial canonical authority.
- **BI-07:** retry preserves exact identity/integrity constraints.
- **BI-08:** known contradiction blocks current use before any repair/supersession.
- **BI-09:** later contradiction does not rewrite historical qualification.
- **BI-10:** offline replay does not pretend to observe external source reality.
- **BI-11:** changed release identity/bytes require explicit new/revised/successor authority semantics.
- **BI-12:** no Phase 3A behavior performs Phase 4 consumer activation.

## 21. Requirement Trace Back

- FR-01/02: exact source/artifact selection is frozen throughout inspect/qualify/establish/resolve.
- FR-03/04/05/17: no flow rebuilds, mutates, republishes, relocates, or transfers ownership as a side effect.
- FR-06/07/08: authority establishment uses one coherent family-neutral release-set model.
- FR-09/10: online resolve and offline replay are distinct explicit flows.
- FR-11: no retry path introduces source-build/publication fallback.
- FR-12/13: qualification and later contradiction behavior preserve integrity/provenance history.
- FR-14/15: resolve emits derived secret-free facts; credentials remain transient.
- FR-16: adoption qualification reaches completion independently of consumer migration.
- FR-18: unsupported/invalid are explicit terminal semantic outcomes, not hidden downgrade paths.

## 22. Decisions Reserved for P12

P11 intentionally does not decide:

- exact canonical field names/types;
- identity generation for `AdoptionAuthorityId` or `AdoptedReleaseSetId`;
- whether authority revisions use new IDs, version fields, content hashes, or supersession links;
- exact schema encoding of `ADOPTABLE / UNSUPPORTED / INVALID`;
- where canonical adoption metadata is stored;
- whether current v1 lock/index remains sufficient;
- how metadata authority and original binary source authority are represented if hosted separately;
- exact durable invalidation/supersession fields;
- exact provider integrity proof representation.

## 23. Decisions Reserved for P13

P13 must define explicit operation/mutation vocabulary for at least:

- qualification commit;
- authority establishment;
- validation/read-only behavior separation;
- invalidation/non-actionability recording;
- successor/supersession establishment;
- idempotency/dedup;
- atomicity;
- conflict/stale-write behavior;
- replay/compatibility of mutations.

P11 behavior semantics constrain P13 but do not choose operation names.

## 24. P11 Exit Check

- start/transient/commit/cancel/retry defined for qualification and establishment: **PASS**;
- resolution separated from canonical authority mutation: **PASS**;
- online/offline behavior distinct: **PASS**;
- source contradiction behavior fail-closed and history-preserving: **PASS**;
- retry cannot weaken authority: **PASS**;
- qualification separated from consumer activation: **PASS**;
- semantic/schema questions preserved for P12: **PASS**;
- operation/atomicity questions preserved for P13: **PASS**.

## 25. P11 Decision

```yaml
stage: P11
owner: aegis-modeling
status: READY
phase: Phase 3A Generic Existing-Release Adoption
canonical_baseline: 580adc8e015413f6a77b1952321fa6e2caa43ae4
working_branch: phase3/existing-release-adoption-p02

behavior_authority:
  inspection: read_only
  qualification_commit: explicit
  adoption_authority_commit: explicit_atomic_boundary
  validation: read_only
  resolution: non_authority_mutating
  source_contradiction: fail_closed_then_explicit_durable_invalidation
  consumer_activation: out_of_scope_phase4

semantic_change_authorized: false
implementation_authorized: false
consumer_migration_authorized: false
next_stage: P12
```

## 26. Handoff

```yaml
type: stage_handoff
from_owner: aegis-modeling
from_stage: P11
to_owner: aegis-modeling
requested_stage: P12
repository: Mostorm-Labs/axbuild
canonical_baseline: 580adc8e015413f6a77b1952321fa6e2caa43ae4
working_branch: phase3/existing-release-adoption-p02
p02: docs/requirements/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P02-v0.1.md
p03: docs/traceability/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P03-v0.1.md
p10: docs/modeling/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P10-v0.1.md
p11: docs/modeling/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P11-v0.1.md
status: READY
open_semantic_question:
  - determine whether current v1 co-location semantics can represent canonical adoption metadata separately from original project-owned artifact source authority; otherwise define the minimum explicitly-authorized semantic extension
constraints:
  - preserve all P02/P03/P10/P11 authority boundaries
  - do not authorize consumer migration
  - do not silently create schema v2
```
