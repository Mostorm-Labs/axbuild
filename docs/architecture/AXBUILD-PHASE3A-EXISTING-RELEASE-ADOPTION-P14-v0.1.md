# AxBuild Phase 3A Generic Existing-Release Adoption — P14 System Architecture v0.1

## Stage

- Owner: `aegis-architecture`
- Stage: `P14 System Architecture`
- Repository: `Mostorm-Labs/axbuild`
- Canonical baseline: `580adc8e015413f6a77b1952321fa6e2caa43ae4`
- Working branch: `phase3/existing-release-adoption-p02`
- Upstream semantic authority:
  - `docs/modeling/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P10-v0.1.md`
  - `docs/modeling/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P11-v0.1.md`
  - `docs/modeling/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P12-v0.1.md`
  - `docs/modeling/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P13-v0.1.md`
- Phase: `Phase 3 — Platform Generalization`
- Capability: `Phase 3A — Generic Existing-Release Adoption`
- Profile: `Standard`
- Status: `READY`
- Successor: `P15 Module Design`

## 1. Role

Freeze the system-level ownership, trust boundaries, dependencies, public boundaries, lifecycle, failure domains, and explicit non-ownership for Generic Existing-Release Adoption.

P14 turns the already-frozen product and semantic model into system architecture. It does not redesign P10-P13, choose implementation classes, define concrete APIs/CLIs, or authorize implementation.

## 2. Authority

P14 consumes P02/P03 and P10-P13 as Current Authority for this Phase 3A scope.

In particular P14 must preserve these upstream facts:

- `AdoptionAuthority` is canonical AxBuild truth, distinct from `ExistingReleaseSource` ownership.
- Original project-owned releases remain externally owned and are not rebuilt, mutated, republished, relocated, or silently transferred.
- `axbuild-adoption-authority-v1` carries explicit source repository/release/asset/digest semantics.
- authority-document location is not artifact ownership.
- same-location v1 projection is permitted only when lossless.
- cross-location projection that erases artifact source identity is forbidden.
- qualification, authority establishment, validation, invalidation, supersession, runtime resolve, and consumer activation are distinct lifecycle concerns.
- runtime success, Store state, cache state, credentials, and transport observations are not canonical authority.

## 3. Objective

Establish one architecture in which:

```text
external project-owned release
        -> inspection / qualification
        -> canonical AdoptionAuthority control plane
        -> authority-preserving resolution boundary
        -> exact artifact acquisition
        -> content-addressed Store
        -> family-specific install / validate
```

without allowing runtime convenience, platform shortcuts, or current v1 resolver assumptions to redefine canonical semantics.

## 4. Non-goals

P14 does not:

- authorize `sdk-lock-v2` or `release-index-v2`;
- reinterpret existing v1 contracts;
- define JSON serialization beyond P12;
- define concrete Python class/module names;
- decide CLI syntax;
- choose database/storage technology for durable authority;
- require a daemon, service, or additional process;
- migrate Axiom/NearCast consumers;
- move Axiom binaries to `axdeps`;
- publish or modify release assets;
- authorize implementation.

## 5. Architecture Principle

AxBuild is a dependency trust coordinator, not the owner of adopted project binaries.

```text
Project owns source release and bytes.
AxBuild owns adoption semantics, qualification, canonical adoption authority,
authority-preserving resolution orchestration, and proof/facts about execution.
```

No component acquires semantic authority merely because it can download, cache, install, or validate bytes.

## 6. System Context

```text
                         External project boundary

                    Project-owned release authority
                    ExistingReleaseSource + assets
                                |
                                v
+---------------------------------------------------------------------+
|                         AxBuild trust domain                         |
|                                                                     |
|  Source Inspection / Qualification Plane                            |
|                 |                                                   |
|                 v                                                   |
|  Adoption Authority Control Plane                                   |
|                 |                                                   |
|                 v                                                   |
|  Adoption Resolution Boundary                                       |
|                 |                                                   |
|                 v                                                   |
|  Artifact Execution Plane                                           |
|      |                 |                   |                        |
|      v                 v                   v                        |
|   Transport           Store             Provider                    |
|                                                                     |
|  Derived Resolution / Diagnostic Facts                              |
+---------------------------------------------------------------------+
                                |
                                v
                      Consumer environment boundary
```

Consumer activation/migration remains outside Phase 3A.

## 7. Subsystem Ownership

### 7.1 External Project Release Authority

Owns:

- original release lifecycle;
- original repository/tag/release namespace;
- original release assets;
- original binary ownership.

AxBuild may inspect, reference, verify, and consume exact bytes under AdoptionAuthority, but does not mutate the source release.

Explicit non-ownership:

- AxBuild does not own or rewrite the original tag;
- AxBuild does not become release owner merely by storing metadata;
- Store/mirror copies do not become a new source authority.

### 7.2 Source Inspection / Qualification Plane

Owns the system responsibility for turning external source observations into immutable qualification records.

Inputs:

- exact `ExistingReleaseSource` candidate;
- integrity contract;
- candidate artifact-role mapping;
- transient credential/access context where needed.

Outputs:

- source inspection observations;
- `SourceIntegrityQualification`;
- `AdoptionCompatibilityResult` / qualification outcome;
- provenance/evidence references.

It does not establish `AdoptionAuthority` by side effect.

It may perform network access and digest inspection, but network responses remain observations rather than authority.

### 7.3 Adoption Authority Control Plane

Owns durable canonical adoption truth and lifecycle mutations defined by P13:

- establish `AdoptionAuthority`;
- evaluate canonical structural validity/actionability inputs;
- record explicit invalidation;
- record explicit supersession/lineage.

It owns the canonical relation:

```text
AdoptionAuthority
  -> exact ExistingReleaseSource
  -> one AdoptedReleaseSet
  -> exact AdoptedArtifactMappings
  -> qualification / provenance linkage
```

It does not own:

- artifact transfer;
- Store materialization;
- family installation;
- consumer migration;
- source release mutation.

Authority persistence must provide atomic establishment and conflict detection. Concrete persistence technology is deferred to P15/P17/P30.

### 7.4 Adoption Resolution Boundary

This is the architectural bridge between canonical Phase 3A authority and runtime execution.

Responsibilities:

- consume a validated/actionable `axbuild-adoption-authority-v1` authority;
- preserve every authoritative artifact role and exact source locator;
- produce deterministic family-neutral resolution intent/plan;
- reject any projection that would erase provider/repository/release/asset/digest identity;
- expose legacy compatibility only where projection is lossless.

This boundary is not itself a source of authority. It is a semantic-to-runtime translation boundary.

#### Legacy same-location compatibility path

When adoption authority can be represented losslessly by current same-repository/tag v1 semantics, the boundary may project to existing `sdk-lock-v1` / `release-index-v1` resolver inputs.

#### General separated-authority path

For the general Phase 3A case, P12 explicitly permits authority metadata to be hosted separately from original artifact bytes. Current resolver v1 enforces index/artifact repository/tag co-location, so the architecture MUST NOT route general separated authority through v1 by lying about or erasing artifact source locators.

Therefore the general path is:

```text
axbuild-adoption-authority-v1
        -> authority validation
        -> source-preserving resolution plan
        -> artifact execution plane
```

P15 will decide whether this is implemented by factoring the existing resolver, adding a new adjacent execution entry point, or another module decomposition. P14 freezes only that the semantic source locator survives intact.

### 7.5 Artifact Execution Plane

Owns runtime orchestration after semantic authority has already been validated and translated into an exact source-preserving plan.

Responsibilities:

- deterministic artifact-role subset selection;
- invoke exact artifact acquisition;
- coordinate Store lookup/materialization;
- invoke family-specific install/validate behavior;
- emit derived resolution facts.

It does not establish, invalidate, supersede, or rewrite AdoptionAuthority.

Current `resolver.py` is a strong existing implementation anchor for orchestration, but its present v1 co-location invariant is implementation reality, not future semantic authority.

### 7.6 Provider Extension Boundary

Owns family-specific realization only:

- family-specific artifact selection rules that are already constrained by canonical role identities;
- package layout interpretation;
- install/materialization behavior;
- package/runtime validation;
- environment output.

Provider code must not:

- select a floating release;
- change source repository/tag/asset/digest;
- create or modify AdoptionAuthority;
- transfer ownership;
- add project-name branches to generic core semantics.

### 7.7 Transport Boundary

Owns byte acquisition for an already-authorized exact source locator.

Responsibilities:

- exact provider/repository/release/asset acquisition;
- authenticated access where needed;
- redirect/auth boundary safety;
- digest verification before bytes become trusted input;
- optional mirror/cache byte transport constrained by exact digest.

Transport does not choose identity and cannot make a fallback release authoritative.

Credentials authorize access only; they are transient and not part of authority identity.

### 7.8 Content-addressed Store

Owns verified local byte/materialization state keyed by frozen identity/digest.

Responsibilities preserve current Store guarantees:

- digest-keyed archive storage;
- integrity revalidation;
- concurrency locking;
- staged/atomic materialization;
- offline replay inputs.

Store state is runtime state, not adoption authority.

A corrupt Store entry may be rejected/removed/re-materialized according to runtime policy; corruption alone does not mutate AdoptionAuthority.

### 7.9 Resolution / Diagnostic Facts

Derived facts may record:

- authority/release-set identity;
- selected artifact identities/digests;
- source/store/mirror observation;
- `networkUsed`;
- provider validation/install outcome;
- explicit failure reason.

They must be secret-free and must not become canonical authority merely because they are persisted as evidence/logs.

## 8. Dependency Direction

Allowed logical dependency direction:

```text
External Source
     |
     v
Inspection / Qualification
     |
     v
Authority Control Plane
     |
     v
Adoption Resolution Boundary
     |
     v
Artifact Execution Plane
   /   |    \
  v    v     v
Transport Store Provider
```

Key forbidden reverse dependencies:

- Transport -> authority selection: forbidden.
- Store -> authority creation/identity: forbidden.
- Provider -> adoption semantic mutation: forbidden.
- Runtime resolve -> authority establishment: forbidden.
- Successful download/install -> qualification upgrade: forbidden.
- Consumer state -> adoption authority mutation: forbidden.

## 9. Public / Stable Boundaries

P14 freezes these logical public boundaries for later P15/P17 refinement:

1. **Source inspection boundary** — exact external source identity in; observations out.
2. **Qualification boundary** — observations + integrity contract + mapping in; immutable qualification result out.
3. **Authority control boundary** — qualification + canonical candidate in; atomic authority lifecycle result out.
4. **Authority-to-resolution boundary** — actionable authority in; exact source-preserving resolution plan out.
5. **Artifact transport boundary** — exact source locator + digest + access context in; verified bytes/failure out.
6. **Store boundary** — exact digest/identity + verified bytes in; verified local artifact/materialization out.
7. **Provider boundary** — selected exact artifact set/materialization in; install/validate/environment result out.
8. **Facts boundary** — secret-free derived runtime facts only.

P15 owns concrete interfaces and module ownership. P17 owns platform/provider realization contracts.

## 10. Lifecycle and Temporal Ownership

### 10.1 Qualification lifecycle

```text
candidate source
 -> inspect external facts
 -> evaluate integrity/compatibility
 -> explicit qualification commit
```

Owner of canonical mutation: Qualification Plane.

No AdoptionAuthority exists merely because qualification is `ADOPTABLE`.

### 10.2 Authority establishment lifecycle

```text
ADOPTABLE qualification
 + exact source
 + exact coherent artifact mappings
 -> validate canonical candidate
 -> atomic authority establishment
```

Owner of canonical mutation: Adoption Authority Control Plane.

### 10.3 Runtime resolve lifecycle

```text
existing actionable AdoptionAuthority
 -> authority-to-resolution boundary
 -> exact plan
 -> Store lookup / exact transport fetch
 -> digest validation
 -> provider install/validate
 -> derived facts
```

Canonical authority mutation: none.

### 10.4 Source contradiction lifecycle

```text
online validation/acquisition observes contradiction
 -> current operation fails closed immediately
 -> contradiction evidence may be produced
 -> separate explicit invalidation/supersession mutation may follow
```

Runtime components never silently repair authority.

### 10.5 Successor authority lifecycle

A changed source release, bytes, mapping, ownership, or semantic contract proceeds through new qualification/establishment and explicit supersession. No `latest` tracking exists.

## 11. Online / Offline Architecture

### Online resolve

```text
AdoptionAuthority
 -> exact source-preserving plan
 -> Store lookup
 -> if required, Transport exact source asset
 -> digest verification
 -> Store materialization
 -> Provider install/validate
 -> ResolutionFacts
```

A mirror may transport digest-bound bytes but never becomes authority.

### Offline replay

```text
same AdoptionAuthority
 -> same deterministic source-preserving plan
 -> verified Store only
 -> materialize/reuse
 -> Provider install/validate
 -> ResolutionFacts(networkUsed=false)
```

Offline mode forbids dependency-network discovery, source release lookup, mirror fetch, alternate release selection, source build, or republish fallback.

Offline replay can prove local reproduction of frozen identity; it cannot pretend to have freshly observed external source reality.

## 12. Failure Domains

Architecture separates failure domains so one failure cannot silently mutate another layer's truth.

### External source / provider API failure

Effects:

- inspection/online acquisition may fail;
- canonical authority remains unchanged;
- retry may use corrected credentials or transient recovery against the same identity.

### Qualification failure

Effects:

- records `UNSUPPORTED` / `INVALID` as appropriate;
- authority establishment is blocked;
- no fallback release/source/owner is selected.

### Authority conflict / stale mutation

Effects:

- mutation fails atomically;
- no partial authority state;
- retry must re-read canonical state rather than overwrite conflicting truth.

### Transport failure

Effects:

- current runtime resolve fails/retries same exact asset;
- authority and qualification history are unchanged.

### Digest mismatch / source contradiction

Effects:

- current operation fails closed;
- changed bytes are never trusted;
- a separate invalidation/supersession path may later mutate canonical lifecycle state.

### Store corruption

Effects:

- local entry is not trusted;
- online mode may reacquire the same exact identity if policy allows;
- offline mode fails if exact verified local bytes cannot be restored without network;
- authority remains unchanged.

### Provider install/validation failure

Effects:

- runtime resolve fails;
- does not imply source bytes or authority changed;
- does not mutate authority automatically.

## 13. Process, Thread, and Concurrency Boundary

P14 does not require separate processes or a daemon. The initial implementation may co-locate all AxBuild subsystems in one CLI/library process.

Process placement has no authority meaning.

Concurrency invariants:

- canonical authority establishment/invalidation/supersession requires atomic conflict-detecting persistence semantics;
- two concurrent semantically identical establishment attempts must converge on the same authority identity rather than produce conflicting truth;
- conflicting authority mutations fail rather than last-writer-wins overwrite;
- Store concurrency remains independently governed by content/digest identity and lock/atomic-materialization rules;
- runtime artifact acquisition cannot hold authority mutation state open while waiting on slow network transfer;
- credentials and network sessions stay request-scoped/transient.

Exact locking/CAS/file/database mechanisms belong to P15/P17/P30.

## 14. Architecture Compatibility with Current Repository

Current anchors:

- `resolver.py`: strong existing orchestration anchor;
- `provider.py`: strong family extension anchor;
- `transport.py`: strong exact-acquisition anchor;
- `store.py`: strong content-addressed Store anchor;
- current lock/index contracts: preserved for existing same-authority flows.

P14 does not grant these modules future ownership merely because they exist.

Critical compatibility rule:

```text
legacy same-location v1 flow
    -> may continue unchanged

general Phase 3A separated metadata/source flow
    -> must preserve explicit source locator
    -> must not be forced through lossy v1 co-location semantics
```

P15 must decide the minimum module-level change that satisfies both paths without semantic duplication.

## 15. Security / Credential Boundary

- credentials are access context only;
- credential rotation cannot change dependency identity;
- secrets must not enter AdoptionAuthority, content-derived IDs, Store identity, resolution facts, durable provenance, or logs;
- auth denial may be retried with corrected credentials against the same exact authority;
- redirect/cross-origin behavior must not leak source credentials;
- no credential availability may trigger alternate source/release fallback.

Detailed provider/platform contract belongs to P17.

## 16. Explicit Non-ownership

- External release owner does not own AxBuild AdoptionAuthority.
- Adoption Authority Control Plane does not own source bytes or transfer.
- Qualification Plane does not establish authority implicitly.
- Resolution Boundary does not invent or weaken semantic source identity.
- Artifact Execution Plane does not mutate authority.
- Provider does not own generic adoption semantics.
- Transport does not select dependency identity.
- Store does not define authority.
- ResolutionFacts do not define authority.
- Phase 3A does not own Phase 4 consumer activation.

## 17. Quality / Architecture Gate

P14 exit criteria:

- upstream P12/P13 semantic authority is preserved without reinterpretation: **PASS**;
- external binary ownership and AxBuild adoption ownership are separated: **PASS**;
- qualification, authority mutation, and runtime execution have explicit owners: **PASS**;
- general separated-authority path retains exact artifact source identity: **PASS**;
- existing v1 same-location compatibility remains valid without redefining v1: **PASS**;
- runtime/download/Store/provider success cannot create or revise authority: **PASS**;
- online/offline and contradiction behavior remain fail-closed: **PASS**;
- failure domains do not silently mutate another layer's truth: **PASS**;
- no daemon/process topology is falsely required for semantic correctness: **PASS**;
- consumer migration/republication/relocation remain out of scope: **PASS**.

## 18. Decision Record

```yaml
stage: P14
owner: aegis-architecture
status: READY
phase: Phase 3A Generic Existing-Release Adoption
canonical_baseline: 580adc8e015413f6a77b1952321fa6e2caa43ae4
working_branch: phase3/existing-release-adoption-p02

architecture:
  external_source_authority: project_owned
  qualification_plane: axbuild_owned
  adoption_authority_control_plane: axbuild_owned
  adoption_resolution_boundary: source_locator_preserving
  artifact_execution_plane: axbuild_owned_runtime
  provider_boundary: family_specific_realization_only
  transport_boundary: byte_acquisition_only
  store_boundary: runtime_content_addressed_state_only

compatibility:
  sdk_lock_v1_preserved: true
  release_index_v1_preserved: true
  v1_reinterpretation_authorized: false
  same_location_lossless_projection_allowed: true
  general_cross_location_lossy_projection_forbidden: true

process_model:
  separate_daemon_required: false
  process_location_has_authority_meaning: false

implementation_authorized: false
consumer_migration_authorized: false
release_relocation_authorized: false
binary_republication_authorized: false

next_stage: P15
```

## 19. Handoff

```yaml
type: stage_handoff
from_owner: aegis-architecture
from_stage: P14
to_owner: aegis-architecture
requested_stage: P15
repository: Mostorm-Labs/axbuild
working_branch: phase3/existing-release-adoption-p02
artifact: docs/architecture/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P14-v0.1.md
status: READY
constraints:
  - preserve axbuild-adoption-authority-v1 semantics
  - preserve exact per-artifact source locator
  - preserve legacy same-location v1 path without v1 reinterpretation
  - do not let runtime components mutate authority
  - no project-name branching in generic core semantics
  - no implementation authorization
  - no consumer migration, release relocation, or binary republication
```
