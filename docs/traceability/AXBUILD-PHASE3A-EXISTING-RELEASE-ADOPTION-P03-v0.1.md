# AxBuild Phase 3A Generic Existing-Release Adoption — P03 Capability Traceability v0.1

## Stage

- Owner: `aegis-discovery`
- Stage: `P03 Capability Traceability`
- Repository: `Mostorm-Labs/axbuild`
- Canonical baseline: `580adc8e015413f6a77b1952321fa6e2caa43ae4`
- Requirement input: `docs/requirements/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P02-v0.1.md`
- Phase: `Phase 3 — Platform Generalization`
- Capability: `Phase 3A — Generic Existing-Release Adoption`
- Profile: `Standard`
- Status: `READY`
- Successor owner: `aegis-modeling`
- Successor stage: `P10 Product Object Model`

## 1. Role

Trace the frozen Phase 3A product requirements into the minimum capability set and downstream design/proof obligations without selecting the final semantic representation, module architecture, provider mechanism, or implementation plan.

P03 is a traceability authority, not architecture authority. Candidate objects, behaviors, module anchors, and operations in this document identify what later design must resolve. They are not final P10-P18 contracts unless a later stage explicitly freezes them.

## 2. Authority

Current upstream authority:

- `docs/authority/AXBUILD-PLATFORM-BOUNDARY-AUTHORITY-v0.1.md`
- `docs/requirements/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P02-v0.1.md`
- preserved Phase 1.5 inventory decisions for Axiom Skia/Semantic `ADOPT EXISTING RELEASE`

Repository reality is used only as an implementation anchor/evidence source, not as design authority.

## 3. Objective

Ensure every Phase 3A requirement has a clear downstream owner and proof path through:

```text
Requirement
  -> Capability
  -> Candidate Object / Behavior
  -> Semantic / Architecture question
  -> Existing or future module boundary
  -> Platform dependency
  -> Verification obligation
```

The result must make it impossible for later design or implementation to accidentally omit the core value constraints:

- preserve existing qualified bytes;
- preserve original release history and ownership;
- no mandatory binary duplication;
- exact repository/tag/asset/digest authority;
- family-neutral behavior;
- verified online acquisition;
- offline Store replay;
- no hidden build/publication fallback;
- adoption is not consumer migration.

## 4. Non-goals

P03 does **not**:

- choose artifact-level locator vs adapter vs adoption-record design;
- authorize `sdk-lock-v2` or `release-index-v2`;
- decide where adoption metadata is stored;
- decide whether adoption metadata is checked into Axiom, AxBuild, or another repository;
- define the exact source immutability proof mechanism;
- define final classes, APIs, CLI commands, file formats, or module names;
- authorize Axiom consumer migration;
- modify existing Axiom releases;
- move Axiom binaries to `axdeps`;
- implement Phase 3A.

## 5. Capability Decomposition

P03 freezes the following capability decomposition as sufficient coverage for P02. Later design may merge implementation modules, but it may not delete an obligation without explicit requirement supersession.

### ERA-CAP-01 — Existing Release Authority Description

Purpose: represent the exact project-owned source release and the release-set identity AxBuild is permitted to adopt.

Must cover:

- source repository;
- exact tag/release identity;
- release-set identity;
- artifact role identity;
- exact asset identity/name;
- SHA256;
- ownership provenance;
- no floating selectors.

Primary requirements: `FR-01`, `FR-02`, `FR-05`, `FR-07`, `FR-08`, `FR-13`, `NFR-01`, `NFR-05`.

### ERA-CAP-02 — Source Immutability / Integrity Qualification

Purpose: decide whether the existing source release can safely become AxBuild dependency authority without requiring mutation of that source release.

Must cover:

- effective immutability or equivalent mutation-detection contract;
- exact release/tag existence;
- asset existence and digest validation;
- source ownership preservation;
- explicit rejection when integrity cannot be established.

Primary requirements: `FR-03`, `FR-04`, `FR-12`, `FR-13`, `FR-18`, `NFR-02`, `NFR-05`.

### ERA-CAP-03 — Canonical Adoption Mapping

Purpose: map an existing release-set shape into a family-neutral AxBuild consumption view while preserving the original source authority.

Must cover:

- one coherent adopted release-set identity;
- multiple artifacts/roles;
- multi-target/multi-variant assets;
- host-tool/runtime combinations;
- deterministic mapping;
- no mandatory repackaging or binary copying.

Primary requirements: `FR-06`, `FR-07`, `FR-08`, `FR-17`, `FR-18`, `NFR-01`, `NFR-03`, `NFR-04`, `NFR-06`.

### ERA-CAP-04 — Family-Neutral Artifact Selection

Purpose: select the exact subset of adopted artifacts for a request without project-name-specific core logic or listing-order ambiguity.

Must cover:

- kind/key/target/variant selection;
- duplicate/ambiguous selector rejection;
- release-set coherence;
- deterministic artifact plan.

Primary requirements: `FR-02`, `FR-06`, `FR-07`, `NFR-01`, `NFR-03`.

### ERA-CAP-05 — Verified Source Acquisition

Purpose: acquire exact source assets from their frozen project-owned authority and verify them before trust.

Must cover:

- exact repository/tag/asset acquisition;
- private access where needed;
- digest verification before Store trust;
- mirror/cache only as non-authoritative byte transport;
- explicit failure on missing/mismatched source.

Primary requirements: `FR-09`, `FR-11`, `FR-12`, `FR-15`, `NFR-02`, `NFR-07`, `NFR-08`.

### ERA-CAP-06 — Verified Store Materialization / Offline Replay

Purpose: preserve current AxBuild content-addressed Store guarantees for adopted artifacts.

Must cover:

- atomic verified materialization;
- Store revalidation;
- offline replay with no release-network access;
- corrupt/missing Store failure;
- no source-build fallback.

Primary requirements: `FR-09`, `FR-10`, `FR-11`, `NFR-01`, `NFR-02`, `NFR-08`.

### ERA-CAP-07 — Family Extension / Provider Boundary

Purpose: keep project-specific install/validation knowledge outside generic adoption semantics.

Must cover:

- generic adoption contract independent of family name;
- project/family-specific selection, install, and validate behavior only through an approved extension boundary;
- third structurally compatible family can be added without a new project-name branch in AxBuild core.

Primary requirements: `FR-06`, `FR-18`, `NFR-03`.

### ERA-CAP-08 — Adoption Diagnostics / Credential Hygiene

Purpose: expose exact reviewer/debug facts while ensuring credentials never become authority.

Must cover:

- adopted release-set identity;
- source repository/tag;
- selected artifacts/digests;
- Store vs network source;
- network-used fact;
- explicit unsupported/failure reason;
- secret-free facts/logs;
- credential rotation independent of dependency identity.

Primary requirements: `FR-14`, `FR-15`, `FR-18`, `NFR-05`, `NFR-07`.

### ERA-CAP-09 — Adoption Qualification Boundary

Purpose: allow Phase 3A to prove an existing release is safely adoptable without changing the consumer repository.

Must cover:

- independent adoption qualification result;
- explicit success/unsupported/fail result;
- reusable evidence for later Phase 4 consumer migration;
- no consumer build/CI mutation as a Phase 3A prerequisite.

Primary requirements: `FR-16`, `FR-18`, `NFR-05`.

## 6. Candidate Product / Semantic Objects for P10

These are trace targets, not frozen object-model names.

| Candidate concept | Why P10 must represent it | Status |
| --- | --- | --- |
| Existing Release Source | distinguishes the original project-owned authority from AxBuild metadata/transport | `TBD_BY_P10` |
| Adoption Authority | machine-readable statement of what existing release may be consumed | `TBD_BY_P10` |
| Adopted Release Set | preserves one coherent identity across multiple existing assets | `TBD_BY_P10` |
| Adopted Artifact Reference | exact source asset + digest + role | `TBD_BY_P10` |
| Source Integrity Qualification | records whether source mutation can be detected / rejected | `TBD_BY_P10` |
| Adoption Compatibility Result | makes `adoptable / unsupported / invalid` explicit | `TBD_BY_P10` |
| Adoption Qualification Result | separates Phase 3A qualification from Phase 4 consumer activation | `TBD_BY_P10` |
| Resolution Facts | reviewer/debug output for source identity, Store/network use, selected artifacts | `EXISTING_ANCHOR + EXTENSION_REVIEW` |

P10 may use different names or merge concepts only if all trace obligations remain representable.

## 7. Candidate Behavior Trace for P11

P11 must freeze behavior for at least these flows:

```text
inspect source release
    -> validate exact authority
    -> qualify integrity / compatibility
    -> establish canonical adoption authority
    -> resolve selected artifact set
    -> verify acquisition
    -> materialize Store
    -> emit facts
```

and:

```text
populated Store
    -> offline resolve
    -> revalidate exact content
    -> materialize / reuse
    -> emit networkUsed=false
```

and fail-closed branches:

```text
missing release/tag/asset
wrong digest
ambiguous asset mapping
unsupported release shape
source integrity cannot be established
credential denied
corrupt Store
        -> explicit terminal failure/unsupported
        -> no nearby release
        -> no latest
        -> no source build
        -> no republish
        -> no ownership transfer
```

P11 must also define whether adoption itself is a one-time qualification/commit behavior, a pure declarative authority-validation behavior, or another explicit lifecycle. P03 does not choose.

## 8. Semantic / Contract Questions for P12

P12 is required because current v1 runtime semantics expose a concrete compatibility question.

Current repository reality:

- `ReleaseIndexRef` binds an index to `repository + release_tag + asset + sha256`;
- `ArtifactRef` can carry its own `repository + release_tag + asset + sha256`;
- however current resolver validation requires every provider artifact repository/tag to equal the verified index repository/tag;
- `release-index-v1` artifact records themselves do not encode an independent artifact repository/tag locator.

Therefore the current implementation assumes, in effect, that verified index authority and artifact release authority are co-located under the same repository/tag.

That assumption fits the current C2 `nearcast-airplay` release but may not fit Phase 3A when:

```text
canonical adoption metadata
        lives outside
original immutable project-owned release assets
```

P12 must determine, without weakening P02 requirements, whether:

1. existing v1 semantics can represent adoption through an approved compatibility/adaptor boundary without semantic change; or
2. a new semantic object/field/version is required to distinguish canonical adoption metadata authority from original artifact source authority.

P03 does **not** authorize option 2; it only establishes that P12 must resolve the question explicitly.

P12 must preserve:

- exact source repository/tag/asset/digest;
- no floating selectors;
- source ownership visibility;
- coherent release-set identity;
- deterministic artifact roles;
- compatibility with Store identity and proof;
- no implicit authority transfer from metadata host to binary owner.

## 9. Operation / Mutation Questions for P13

P13 is required because Phase 3A has an authority-establishment boundary that must not be confused with ordinary runtime resolve.

P13 must determine whether the system has explicit operations analogous to:

```text
InspectExistingRelease
QualifyExistingRelease
EstablishAdoptionAuthority
ValidateAdoptionAuthority
ResolveAdoptedRelease
InvalidateOrRejectChangedSource
```

These names are illustrative only.

P13 must make clear:

- which operations create/change durable authority versus merely read/validate it;
- whether qualification is idempotent;
- what can be retried;
- what fails terminally;
- how a later detected source mutation affects previously established adoption authority;
- why consumer activation/migration is not an adoption operation.

## 10. System Architecture Questions for P14

P14 must freeze ownership and trust flow among at least these conceptual boundaries:

```text
project-owned source release
        |
        v
source integrity / compatibility qualification
        |
        v
canonical adoption authority
        |
        v
family-neutral resolver
        |
        +--> verified transport
        |
        +--> Store
        |
        +--> family/provider install + validate
        |
        v
resolution facts
```

P14 must decide where provider-specific source-release inspection ends and where family-neutral authority begins.

It must also freeze who owns:

- adoption authority generation;
- source integrity proof/validation;
- release-set mapping;
- artifact source locator interpretation;
- provider-specific install/validate;
- invalidation when source reality contradicts frozen authority.

P14 must not infer architecture from the location of existing NearCast-specific `publication.py` or qualification code.

## 11. Module Design Questions for P15

Current implementation anchors that may be reused but are not automatically future ownership:

| Existing module | Current useful behavior | P03 classification |
| --- | --- | --- |
| `contracts.py` / schemas | validates current SDK lock/release-index contracts | `EXISTING_ANCHOR` |
| `model.py` | immutable refs, provider plan, resolution result | `EXISTING_ANCHOR` |
| `provider.py` | project-owned provider contract and registry | `EXISTING_ANCHOR` |
| `resolver.py` | family-neutral verified-index orchestration | `EXISTING_ANCHOR` |
| `transport.py` | exact GitHub release asset acquisition, credentials, SHA256, offline failure | `EXISTING_ANCHOR` |
| `store.py` | content-addressed storage, locking, atomic materialization, validation | `EXISTING_ANCHOR` |
| NearCast qualification/publication modules | one-family evidence/implementation precedent | `EVIDENCE_NOT_GENERIC_AUTHORITY` |

P15 must decide whether new adoption responsibilities belong in:

- new generic adoption modules;
- provider/adapter interfaces;
- contract/model extensions;
- resolver changes;
- or another bounded design.

No current module name is frozen as the final owner by P03.

## 12. Runtime Data Flow Questions for P16

P16 must freeze at least four data flows:

### Flow A — Adoption qualification

```text
source release metadata/assets
        -> integrity/compatibility inspection
        -> exact artifact mapping
        -> adoption authority
        -> qualification result/evidence
```

### Flow B — Empty-Store online resolve

```text
adoption authority
        -> resolver/provider plan
        -> exact source release asset
        -> digest verification
        -> Store
        -> install/validate
        -> facts
```

### Flow C — Offline replay

```text
same adoption authority
        -> Store lookup
        -> digest / package validation
        -> install/reuse
        -> facts(networkUsed=false)
```

### Flow D — Drift/failure

```text
source missing / changed / ambiguous / unauthorized
        -> validation failure
        -> no Store trust update
        -> no alternate identity
        -> explicit fail/unsupported result
```

## 13. Platform Contract Questions for P17

P17 must define provider/platform contracts for:

- exact release/tag lookup;
- asset enumeration/lookup without listing-order authority;
- authenticated private asset fetch;
- provider-specific immutable-release or equivalent integrity signals;
- behavior when a platform cannot prove immutability directly;
- redirect/auth credential boundaries;
- offline behavior;
- source metadata limits/errors;
- secret handling in logs/facts;
- mirror/cache byte transport without authority transfer.

GitHub is the first reference platform because the real Skia/Semantic candidates are project-owned releases, but the generic product capability must not define `GitHub immutable=true` as the only concept of source integrity.

## 14. Engineering / Optimization Questions for P18

P18 is required, but narrowly scoped to product-relevant engineering constraints rather than premature optimization.

It must cover:

- large SDK transfer/storage amplification;
- avoiding mandatory duplicate binary publication;
- Store reuse across repeated resolves;
- bounded metadata inspection rather than downloading every asset to discover identity;
- concurrency/locking when several jobs adopt/resolve the same digest;
- atomicity of first materialization;
- whether integrity qualification requires expensive full-download checks and how those checks can be cached without weakening mutation detection.

Performance optimization that does not affect these product constraints may remain implementation-level later.

## 15. Requirement -> Capability Trace Matrix

| Requirement | Capability owner(s) | Primary downstream stages | Proof obligation summary |
| --- | --- | --- | --- |
| FR-01 exact source binding | CAP-01, CAP-02 | P10/P12/P14/P17 | same authority always selects exact source repo/tag; missing exact release fails |
| FR-02 artifact identity/digest | CAP-01, CAP-04, CAP-05 | P10/P12/P16/P20 | wrong bytes/name ambiguity rejected independent of listing order |
| FR-03 preserve bytes | CAP-02, CAP-03 | P11/P14/P20 | adoption succeeds with original digest and no producer build |
| FR-04 preserve release history | CAP-02, CAP-09 | P11/P13/P17/P20 | original tag/assets unchanged; later mutation is detected/rejected |
| FR-05 preserve ownership | CAP-01, CAP-03 | P10/P12/P14/P20 | source repo remains explicit; no implicit `axdeps` transfer |
| FR-06 family-neutral | CAP-03, CAP-04, CAP-07 | P10/P14/P15/P20 | Skia/Semantic + third compatible family without project-name core branch |
| FR-07 multi-artifact coherence | CAP-03, CAP-04 | P10/P12/P16/P20 | host/runtime and multi-target assets share one release-set identity |
| FR-08 canonical consumption boundary | CAP-01, CAP-03, CAP-07 | P12/P14/P15 | deterministic machine-readable authority reaches resolver boundary |
| FR-09 verified online acquisition | CAP-05, CAP-06 | P16/P17/P20 | empty Store fetches exact assets, verifies before trust |
| FR-10 offline replay | CAP-06 | P16/P17/P20 | same authority resolves from Store with no network |
| FR-11 no hidden build fallback | CAP-05, CAP-06, CAP-09 | P11/P16/P20 | missing/invalid bytes terminate without build/republication/substitute |
| FR-12 source integrity qualification | CAP-02 | P11/P12/P14/P17/P20 | mutable/undetectable source cannot become authority |
| FR-13 provenance | CAP-01, CAP-02, CAP-08 | P10/P12/P20 | reviewer traces adopted artifact back to original source identity/digest |
| FR-14 machine facts | CAP-08 | P10/P15/P16/P20 | exact source, selected artifacts, Store/network facts, no secrets |
| FR-15 credential boundary | CAP-05, CAP-08 | P14/P17/P20 | credential rotation does not change identity; denied auth has no fallback |
| FR-16 independent adoption qualification | CAP-09 | P11/P13/P14/P20 | Phase 3A Gate without consumer repo changes |
| FR-17 no mandatory duplication | CAP-03, CAP-05 | P12/P14/P18/P20 | existing authoritative bytes remain in place; mirrors non-authoritative |
| FR-18 explicit compatibility outcome | CAP-02, CAP-03, CAP-08, CAP-09 | P11/P13/P20 | unsupported is explicit and does not weaken guarantees or auto-migrate |
| NFR-01 determinism | CAP-01, CAP-03, CAP-04, CAP-06 | P12/P16/P20 | repeat resolution identity stable across supported hosts |
| NFR-02 integrity over availability | CAP-02, CAP-05, CAP-06 | P11/P16/P20 | substitution/fallback rejected |
| NFR-03 family neutrality | CAP-03, CAP-07 | P10/P14/P15/P20 | generic core has no project-specific semantic branch |
| NFR-04 backward compatibility | CAP-01, CAP-03 | P12/P14/P20 | v1 preserved unless explicit semantic authority proves change necessary |
| NFR-05 reviewability | CAP-01, CAP-02, CAP-08, CAP-09 | P10/P12/P20 | machine-readable source/evidence reconstruction |
| NFR-06 large-artifact efficiency | CAP-03, CAP-05, CAP-06 | P18/P20 | no inherent duplicate authoritative publication/storage multiplication |
| NFR-07 credential hygiene | CAP-05, CAP-08 | P17/P20 | secrets excluded from authority, Store identity, facts/logs |
| NFR-08 resolver/Store consistency | CAP-05, CAP-06, CAP-07 | P14/P16/P20 | adopted artifacts retain established online/offline/atomic/fail-closed behavior |

## 16. Reference Shape Trace

### A. Skia-like multi-target / multi-variant SDK

Must exercise:

- CAP-01 exact project-owned release identity;
- CAP-02 source integrity qualification;
- CAP-03 mapping of many target/variant assets under one release set;
- CAP-04 deterministic target/variant selection;
- CAP-05/06 online + offline exact asset reuse;
- CAP-07 provider-specific SDK layout install/validate without Skia logic in core;
- CAP-09 adoption Gate with zero Axiom consumer migration.

A design that only supports one artifact per release does not satisfy this trace.

### B. Semantic-like host-tools + target-runtime release set

Must exercise:

- one coherent adopted release-set identity;
- host-tool artifact selection independent of target runtime selection;
- multiple artifact roles under the same qualification boundary;
- exact source asset provenance/digests;
- common resolver/Store flow;
- provider-specific environment/install behavior outside generic adoption semantics.

A design that treats host tools and runtimes as unrelated ad-hoc downloads does not satisfy this trace.

## 17. Current Implementation Anchor Review

P03 reviewed current repository reality only to determine reuse boundaries.

### Resolver

Current `resolver.py` already:

- verifies an index before provider planning;
- rejects duplicate kind/key artifacts;
- requires provider artifact identity/asset/digest/metadata to match the verified index;
- uses Store + verified transport;
- emits releaseSetId, artifact, source, and `networkUsed` facts.

Classification: `STRONG_EXISTING_ANCHOR`.

Gap relevant to design: current resolver also requires artifact repository/tag to equal index repository/tag. Existing-release adoption must explicitly resolve whether that invariant remains valid or needs a new authorized semantic boundary.

### Provider

Current `provider.py` already separates project-owned planning/install/validate/environment behavior behind a family registry.

Classification: `STRONG_EXISTING_ANCHOR`, but P15 must decide whether source-adoption inspection belongs in this same contract or a separate one.

### Transport

Current `transport.py` already provides exact GitHub release asset lookup, private-token support, redirect credential stripping, digest verification, mirror fallback with digest authority, and offline fail-closed.

Classification: `STRONG_EXISTING_ANCHOR`.

### Store

Current `store.py` already provides content-addressed archive paths, locking, SHA verification, staging, validation, and atomic materialization.

Classification: `STRONG_EXISTING_ANCHOR`.

### Current schemas/model

Current model types can carry repository/tag on refs, but current v1 release index artifact records do not independently express artifact repository/tag and current resolver enforces co-location with index authority.

Classification: `SEMANTIC_COMPATIBILITY_QUESTION`, owned by P12 rather than inferred by P03.

## 18. Downstream Design Route

P03 finds the following design stages materially affected and therefore not safely skippable:

```yaml
required_design_stages:
  P10_Product_Object_Model: required
  P11_Interaction_Behavior: required
  P12_Semantic_Schema: required
  P13_Operation_Mutation_Model: required
  P14_System_Architecture: required
  P15_Module_Design: required
  P16_Runtime_Data_Flow: required
  P17_Platform_Contract: required
  P18_Engineering_Optimization: required_bounded_scope
```

Reasoning:

- P10/P11: adoption introduces new authority/qualification concepts and lifecycle behavior;
- P12: current index/artifact co-location assumption may be insufficient;
- P13: adoption authority establishment/invalidation must be distinct from runtime resolution and consumer migration;
- P14/P15: trust and ownership boundaries must be frozen before code reuse/refactor decisions;
- P16: online/offline/failure flows are product-critical;
- P17: private source platforms, integrity signals, credentials, and mirrors are contract-critical;
- P18: avoiding duplicate large binaries is a core product constraint, not optional micro-optimization.

## 19. Verification Obligation Register for Future P20

P03 does not design evidence, but freezes the failure modes P20 must consider.

| Obligation | High-impact failure mode to cover |
| --- | --- |
| VO-01 exact release selection | resolver/adoption selects wrong or floating release |
| VO-02 exact artifact bytes | correct asset name but changed/tampered bytes accepted |
| VO-03 source mutation detection | previously adopted mutable release changes without detection |
| VO-04 ownership preservation | adoption silently changes repository authority or rehosts binaries |
| VO-05 no rebuild/republish | system invokes producer or creates duplicate authoritative publication as fallback |
| VO-06 multi-artifact coherence | host/runtime or target/variant artifacts are mixed across release-set identities |
| VO-07 family neutrality | generic core contains project-name-specific semantic branching |
| VO-08 empty-Store online resolve | adopted authority cannot acquire/verify exact bytes through common resolver path |
| VO-09 offline replay | populated Store still reaches dependency network or cannot reproduce same identity |
| VO-10 corrupt Store fail-closed | corrupt/missing Store bytes are trusted or trigger unsafe fallback |
| VO-11 credential hygiene | secrets become authority or leak into persistent facts/logs |
| VO-12 explicit unsupported result | incompatible source shape silently weakens identity/integrity contract |
| VO-13 consumer separation | Phase 3A proof requires or silently performs Axiom consumer migration |
| VO-14 large-artifact non-duplication | architecture mandates a second authoritative copy solely for AxBuild compatibility |

Per global Aegis evidence policy, P20 must not make every possible artifact blocking. A blocking proof is justified only where it uniquely detects an otherwise uncovered high-impact failure mode.

## 20. Traceability Completeness Check

P03 exit criteria:

- every P02 FR/NFR maps to at least one capability: **PASS**;
- every P0 requirement maps to downstream design and verification ownership: **PASS**;
- both Skia and Semantic reference shapes exercise the capability model: **PASS**;
- no capability requires binary rebuild, source release mutation, ownership transfer, or mandatory duplication: **PASS**;
- current implementation is distinguished from future architecture authority: **PASS**;
- semantic compatibility gap is surfaced rather than silently resolved: **PASS**;
- adoption qualification remains separate from consumer migration: **PASS**;
- future P20 failure-mode obligations are traceable without prematurely defining evidence mechanisms: **PASS**.

## 21. P03 Decision

```yaml
stage: P03
owner: aegis-discovery
status: READY
phase: Phase 3A Generic Existing-Release Adoption
canonical_baseline: 580adc8e015413f6a77b1952321fa6e2caa43ae4
requirement_revision: 59fb3aa1932c8d512efe6634974c9db879f2d1eb

capability_count: 9
requirements_trace_complete: true
reference_shapes_trace_complete: true
consumer_migration_in_scope: false
semantic_change_authorized: false
architecture_selected: false
implementation_authorized: false

next_owner: aegis-modeling
next_stage: P10
```

## 22. Handoff

```yaml
type: ownership_handoff
from_owner: aegis-discovery
from_stage: P03
to_owner: aegis-modeling
requested_stage: P10
repository: Mostorm-Labs/axbuild
canonical_baseline: 580adc8e015413f6a77b1952321fa6e2caa43ae4
working_branch: phase3/existing-release-adoption-p02
requirement_artifact: docs/requirements/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P02-v0.1.md
traceability_artifact: docs/traceability/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P03-v0.1.md
capability: Generic Existing-Release Adoption
status: READY
constraints:
  - preserve project-owned existing releases
  - no rebuild or source-release mutation
  - no mandatory binary duplication
  - exact source repository/tag/asset/digest authority
  - family-neutral common adoption boundary
  - online verified acquisition and offline Store replay
  - no floating latest
  - no hidden source-build/publication fallback
  - adoption qualification is not consumer migration
open_design_question:
  - resolve current index-authority/artifact-authority co-location assumption without weakening P02
```
