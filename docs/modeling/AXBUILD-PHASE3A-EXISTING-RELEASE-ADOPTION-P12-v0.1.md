# AxBuild Phase 3A Generic Existing-Release Adoption — P12 Semantic Schema v0.1

## Stage

- Owner: `aegis-modeling`
- Stage: `P12 Semantic Schema`
- Repository: `Mostorm-Labs/axbuild`
- Canonical baseline: `580adc8e015413f6a77b1952321fa6e2caa43ae4`
- Working branch: `phase3/existing-release-adoption-p02`
- Upstream: P02, P03, P10, and P11 artifacts in this PR
- Phase: `Phase 3 — Platform Generalization`
- Capability: `Phase 3A — Generic Existing-Release Adoption`
- Profile: `Standard`
- Status: `READY`
- Successor: `P13 Operation / Mutation Model`

## 1. Role and Scope

P12 freezes canonical state, stable identity, field meaning, defaults, validation, versioning, compatibility, optionality, and extensibility for Generic Existing-Release Adoption.

It does not authorize implementation, choose a storage repository, define CLI/API/module ownership, migrate a consumer, relocate a release, or modify/rebuild/republish existing release assets.

## 2. Preserved Authority

This schema preserves:

- exact provider/repository/release/asset/digest authority;
- no floating selectors or listing-order identity;
- visible original project ownership;
- no rebuild, mutation, republish, relocation, or mandatory binary duplication;
- one coherent family-neutral multi-artifact release set;
- separate qualification history and adoption authority;
- read-only validation/resolution with explicit later mutation for invalidation;
- consumer activation as a separate Phase 4 lifecycle;
- unchanged `axbuild-sdk-lock-v1` and `axbuild-release-index-v1`.

## 3. P12 Decision: Resolve the Co-location Question

### 3.1 Co-location is not canonical

The authority hosting canonical adoption metadata and the authority hosting original artifact bytes are distinct and MAY be located in different repositories/releases.

```text
AdoptionAuthorityDocument
        |
        | authorizes
        v
AdoptedReleaseSet
        |
        +--> exact ArtifactSourceLocator A
        +--> exact ArtifactSourceLocator B
        +--> exact ArtifactSourceLocator N
```

The authority-document host does not inherit ownership of the binaries. Artifact source identity is never inferred from document location.

### 3.2 Current v1 semantics remain valid but do not cover separated authority

Current `release-index-v1` same-repository/tag flows remain valid. They do not represent the general Phase 3A case when adoption metadata is hosted separately from the original project-owned artifacts: artifact repository/tag would be implicit, and current resolver validation requires index/artifact co-location.

Therefore:

- no v1 field reinterpretation is allowed;
- cross-repository adoption cannot pretend that the metadata repository owns the artifacts;
- an adapter cannot discard or overwrite an exact artifact source locator;
- same-location adoption may be projected into v1 only when the projection is lossless;
- separated-authority adoption requires the additive semantic contract below before implementation.

### 3.3 Minimum additive semantic extension

P12 establishes this canonical document kind:

```text
axbuild-adoption-authority-v1
```

It is not `sdk-lock-v2` or `release-index-v2` and changes neither existing v1 contract. It is immutable authority input that later authorized architecture may validate and project into resolver inputs.

## 4. Canonical Root Shape

```yaml
schema: axbuild-adoption-authority-v1
authorityId: aa-sha256:<64-lowercase-hex>
family: <FamilyId>
source:
  provider: <ProviderId>
  repository: <RepositoryLocator>
  release: <ExactReleaseId>
  owner: <OwnerId>
releaseSet:
  releaseSetId: ars-sha256:<64-lowercase-hex>
  artifacts:
    - artifactId: art-sha256:<64-lowercase-hex>
      role:
        kind: <ArtifactKind>
        key: <ArtifactKey>
        target: <TargetId-or-null>
        variant: <VariantId-or-null>
      source:
        provider: <ProviderId>
        repository: <RepositoryLocator>
        release: <ExactReleaseId>
        asset: <ExactAssetId>
      digest:
        algorithm: sha256
        value: <64-lowercase-hex>
      sizeBytes: <non-negative-integer-or-absent>
integrityContract:
  kind: <IntegrityContractKind>
  mutationDetection: required
qualification:
  sourceIntegrityQualificationId: <QualificationId>
  compatibilityResultId: <CompatibilityResultId>
provenance:
  sourceEvidenceRefs: [<EvidenceRef>, ...]
supersedes: <AuthorityId-or-null>
extensions: {}
```

Member order is non-semantic. Artifact/evidence array order is normalized for identity.

## 5. Field Registry

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `schema` | closed string | yes | exactly `axbuild-adoption-authority-v1` |
| `authorityId` | `AdoptionAuthorityId` | yes | content-derived immutable adoption-statement identity |
| `family` | `FamilyId` | yes | family/provider namespace; never a project-name core branch |
| `source` | `ExistingReleaseSourceRef` | yes | original release-level ownership and authority |
| `releaseSet` | `AdoptedReleaseSet` | yes | coherent exact artifact set |
| `integrityContract` | `IntegrityContract` | yes | frozen source mutation-detection requirement |
| `qualification` | `QualificationLinks` | yes | committed qualification history, never runtime success |
| `provenance` | `ProvenanceLinks` | yes | trace to original qualified release |
| `supersedes` | nullable authority ID | no | explicit predecessor; absence means none declared |
| `extensions` | namespaced map | no | additive data constrained by Section 13 |

No omitted field may be inferred from hosting location, filename, network response, credentials, environment, or Store state.

## 6. Value Semantics

### 6.1 Identifiers

Semantic identifiers are non-empty normalized UTF-8 strings. Leading/trailing whitespace, controls, empty path segments, locale-dependent comparison, and case-folded aliases are invalid. Content-derived IDs use lowercase SHA-256 with the prefixes shown above.

### 6.2 Exact release source

`ExistingReleaseSourceRef` requires provider, repository, exact release/tag, and original owner. `latest`, branches, searches, ranges, listing position, and release-title matching are invalid.

### 6.3 Exact artifact source

Each artifact repeats complete provider/repository/release/asset identity. Nothing is inherited from the authority-document host.

For `axbuild-adoption-authority-v1`, every artifact provider/repository/release MUST equal the root source provider/repository/release. The repetition is intentional: the trust boundary stays explicit while v1 preserves one coherent existing release.

Multi-release composition is not enabled by extensions and would require new semantic authority.

### 6.4 Artifact role

Role identity is `(kind, key, target?, variant?)`. Kind/key are required. Target/variant are optional; absence is semantic null, while empty string is invalid. The full tuple is unique in a release set. Runtime subset selection does not change release-set identity.

### 6.5 Digest and size

Digest algorithm is exactly `sha256`; value is 64 lowercase hex characters. Optional `sizeBytes`, when present, is a non-negative integer and authoritative validation input. Asset names, URLs, ETags, timestamps, or provider object IDs cannot replace digest identity.

## 7. Stable Identity

A concrete encoding later supplies deterministic bytes, but it MUST preserve this canonical semantic projection:

- lexicographically sorted keys;
- encoding-defined Unicode normalization;
- no insignificant whitespace;
- absent optional fields remain absent;
- artifacts sorted by role tuple, exact source locator, then digest;
- evidence refs sorted byte-exact and deduplicated;
- declared IDs, signatures, diagnostics, storage location, and non-identity extensions excluded from their own hash;
- `supersedes` and present `sizeBytes` included.

### 7.1 Artifact identity

```text
artifactId = "art-sha256:" + SHA256(
  canonical(role + source + digest + optional sizeBytes)
)
```

Changed role, source, asset, digest, or authoritative size creates a new artifact identity.

### 7.2 Release-set identity

```text
releaseSetId = "ars-sha256:" + SHA256(
  canonical(family + root source + sorted artifact identity set)
)
```

Order and requested subset do not change identity. Adding/removing/changing an artifact does.

### 7.3 Authority identity

```text
authorityId = "aa-sha256:" + SHA256(
  canonical(
    schema + family + source + releaseSet + integrityContract
    + qualification links + ownership/provenance identity + supersedes
  )
)
```

Changed source release, artifact bytes/roles, owner, integrity contract, qualification linkage, or supersession creates a new authority identity. Evidence presentation metadata is non-semantic when referenced evidence identity is unchanged.

## 8. Qualification Records

`SourceIntegrityQualification` durably records qualification ID, exact source, integrity contract, covered artifact IDs/digests, `QUALIFIED | UNSUPPORTED | INVALID`, and evidence refs. Only `QUALIFIED` may support actionable authority.

`AdoptionCompatibilityResult` records result ID, candidate releaseSetId, semantic-contract ID, `ADOPTABLE | UNSUPPORTED | INVALID`, stable reason code, and evidence refs. Only `ADOPTABLE` may support actionable authority.

Runtime download success and Store presence are not qualification. Records are immutable history; later contradiction does not edit the old outcome.

## 9. Invalidation and Supersession State

AdoptionAuthority is immutable. Actionability derives from schema validity, valid qualification links, absence of effective invalidation, explicit supersession policy, and mode-appropriate current validation facts.

P12 freezes separate durable relation records for P13:

```yaml
AdoptionAuthorityInvalidation:
  invalidationId: <StableId>
  authorityId: <AuthorityId>
  reasonCode: <ClosedCode>
  evidenceRefs: [...]
  supersedesInvalidationId: <Id-or-null>

AdoptionAuthoritySupersession:
  predecessorAuthorityId: <AuthorityId>
  successorAuthorityId: <AuthorityId>
  reasonCode: <ClosedCode>
```

Invalidation never deletes or rewrites authority/qualification history. Supersession never means floating "follow latest." P13 owns operations, atomicity, conflict behavior, and effective ordering.

## 10. Validation Rules

A document is invalid unless:

1. schema discriminator matches exactly;
2. required fields exist and unknown non-extension root fields are rejected;
3. computed identities equal declared IDs;
4. at least one artifact exists;
5. role tuples and artifact IDs are unique;
6. every artifact has complete exact source plus SHA-256;
7. each artifact source provider/repository/release equals root source in v1;
8. no floating/environment-derived locator exists;
9. qualification links match the exact source, release set, contract, and qualifying outcomes;
10. owner is original source owner, never inferred from metadata host;
11. evidence refs are non-empty, unique after normalization, and secret-free;
12. supersedes does not self-reference;
13. credentials, tokens, Store/local paths, mirrors, network facts, or consumer activation are absent from canonical authority;
14. extensions cannot override core meaning.

Validation fails closed and cannot repair authority by choosing another repository, release, asset, digest, or owner.

## 11. Defaults and Optionality

| Field | Rule |
| --- | --- |
| `target`, `variant` | optional; absence means role is not qualified by that dimension |
| `sizeBytes` | optional; absence leaves digest as byte identity |
| `supersedes` | optional; absence means no predecessor declared |
| `extensions` | optional; defaults to empty map |
| all other authority/source/artifact fields | required; never context-defaulted |

## 12. Versioning and Compatibility

- `axbuild-adoption-authority-v1` is a closed semantic major version.
- Readers reject unknown major discriminators.
- Optional namespaced extensions may be added within v1.
- New core optional fields require explicit absence semantics and authority revision.
- Required-field changes, validation weakening, or changed existing-field meaning require a new major.
- `sdk-lock-v1` and `release-index-v1` remain unchanged.
- Existing same-authority publication/resolution remains unchanged.
- Lossless same-location projection to v1 is semantically permitted for later design/proof.
- Cross-location projection that erases artifact repository/release is forbidden.
- AdoptionAuthority is not a consumer lock and does not activate a consumer.
- Unknown root fields outside `extensions` are invalid.

## 13. Extensions

Keys use collision-resistant owner namespaces. Extensions cannot override core fields, add fallback authority, relax digest/locator rules, introduce floating selection, transfer ownership, compose another release under v1, encode credentials, activate consumers, or change actionability without recognized schema authority.

A core reader may ignore only explicitly non-critical extensions. Critical-extension negotiation belongs to later encoding/platform design.

## 14. Non-Canonical State

Credentials/tokens, document storage location, API responses/listing order, Store/archive/materialized paths, cache/mirror entries, network facts/timestamps, transient sessions, resolver requests/results, and consumer activation/build/CI state are non-canonical.

Runtime resolution never creates or revises AdoptionAuthority.

## 15. Reference Conformance

- Skia-like: multiple target/variant artifacts share one exact project-owned root release; each keeps exact asset/digest.
- Semantic-like: host tools and target runtimes share one releaseSetId; roles distinguish purpose and subset selection does not split identity.
- Separately hosted metadata: authority document may live in AxBuild or another approved location while root/artifact source continues to name the original project-owned release. Hosting location has no ownership or selection meaning.

## 16. Reserved for P13 and Later

P13 defines qualification commit, authority establishment/dedup, invalidation, supersession, conflicts, stale writes, replay, atomicity, and read-only versus mutating operations. It cannot change P12 meaning or restore co-location inheritance.

P14–P20 may choose architecture, modules, flows, platform/serialization contracts, bounded efficiency, and evidence. P30/P31 may later authorize implementation packages. None may treat P12 as implementation, consumer migration, release relocation, or binary republication authority.

## 17. P12 Exit Check

- canonical state and related durable records: **PASS**
- identity/change rules: **PASS**
- field meaning/defaults/validation/versioning/optionality/extensions: **PASS**
- qualification separated from runtime/Store: **PASS**
- immutable history and invalidation/supersession boundary: **PASS**
- co-location resolved: **PASS — not canonical**
- existing v1 preserved without reinterpretation: **PASS**
- minimum additive semantic contract bounded: **PASS**
- implementation, migration, relocation, republication excluded: **PASS**

## 18. Decision Record

```yaml
stage: P12
owner: aegis-modeling
status: READY
canonical_baseline: 580adc8e015413f6a77b1952321fa6e2caa43ae4
working_branch: phase3/existing-release-adoption-p02

co_location_is_canonical_invariant: false
artifact_source_locator_explicit_per_artifact: true
authority_document_host_is_binary_owner: false
new_semantic_contract: axbuild-adoption-authority-v1
sdk_lock_v2_authorized: false
release_index_v2_authorized: false
v1_reinterpretation_authorized: false
lossless_same_location_projection_permitted_for_later_design: true
lossy_cross_location_projection_forbidden: true

implementation_authorized: false
consumer_migration_authorized: false
release_relocation_authorized: false
binary_republication_authorized: false
next_stage: P13
```

## 19. Handoff

```yaml
type: stage_handoff
from_owner: aegis-modeling
from_stage: P12
to_owner: aegis-modeling
requested_stage: P13
repository: Mostorm-Labs/axbuild
canonical_baseline: 580adc8e015413f6a77b1952321fa6e2caa43ae4
working_branch: phase3/existing-release-adoption-p02
artifact: docs/modeling/AXBUILD-PHASE3A-EXISTING-RELEASE-ADOPTION-P12-v0.1.md
status: READY
semantic_contract: axbuild-adoption-authority-v1
constraints:
  - exact per-artifact provider/repository/release/asset/digest
  - original source ownership
  - immutable authority and qualification history
  - no v1 reinterpretation
  - no implementation authorization
  - no consumer migration
  - no release relocation or binary republication
```
