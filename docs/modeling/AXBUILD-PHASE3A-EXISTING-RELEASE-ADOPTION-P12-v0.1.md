# AxBuild Phase 3A Generic Existing-Release Adoption — P12 Semantic Schema v0.1

## Stage

- Owner: `aegis-modeling`
- Stage: `P12 Semantic Schema`
- Phase: `Phase 3 — Platform Generalization`
- Capability: `Phase 3A — Generic Existing-Release Adoption`
- Status: `READY`

## Purpose

Freeze the canonical semantic meaning of Generic Existing-Release Adoption before schema encoding, API, or implementation decisions.

P12 defines semantic truth, not JSON fields, database layout, or wire format.

## Core Semantic Boundary

AxBuild distinguishes:

```
AdoptionAuthority
        !=
ExistingReleaseSource
```

`ExistingReleaseSource` represents the original project-owned release and remains owned by that project.

`AdoptionAuthority` represents AxBuild's explicit authorization to consume an exact existing release set. It does not transfer binary ownership.

## Canonical Objects

### AdoptionAuthority

Canonical aggregate representing an explicit adoption statement.

Semantic contents:

- adoption identity;
- source release reference;
- adopted release set reference;
- qualification linkage;
- provenance linkage;
- ownership descriptor;
- lifecycle state.

### ExistingReleaseSource

External resource reference representing the original release authority.

Contains the exact external source identity:

- provider;
- repository/namespace;
- release identity;
- tag/version;
- original owner.

### AdoptedReleaseSet

Represents a coherent set of adopted artifacts.

Supports:

- multi-target SDKs;
- multi-variant releases;
- host-tool/runtime combinations.

Artifacts from unrelated releases cannot form one adopted release set.

### AdoptedArtifactMapping

Maps:

```
ArtifactRole
        ->
Exact Source Asset
        +
Content Digest
```

Filename alone is never identity.

## Identity Rules

### AdoptionAuthority Identity

Authority identity represents a complete adoption statement, not only a source release.

It includes:

- source release identity;
- adopted release-set identity;
- artifact mapping semantics;
- adoption contract semantics.


### New Identity Required

A new authority identity is required when:

- source release changes;
- artifact bytes/digest changes;
- artifact role mapping changes;
- ownership boundary changes.

### Revision Allowed

Revision may represent non-semantic additions such as evidence attachment or diagnostic metadata without changing adopted bytes or authority meaning.

## Qualification Semantic

Qualification is a separate durable concept.

```
QualificationRecord
        !=
AdoptionAuthority
```

Qualification history must remain preserved.

An authority does not become qualified by a runtime download or Store entry.

## Lifecycle Semantic

Authority history is append/supersede based.

Old authority records are not deleted when replaced.

Conceptual relation:

```
Old Authority
      |
      | superseded by
      v
New Authority
```

## Compatibility Decision

Current `sdk-lock-v1` and `release-index-v1` semantics remain valid for existing same-authority publication flows.

Phase 3A does not immediately authorize `sdk-lock-v2` or `release-index-v2`.

A compatibility boundary may adapt AdoptionAuthority semantics into existing resolver inputs.

## Non-Canonical Data

The following are not semantic authority:

- credentials;
- tokens;
- Store paths;
- cache entries;
- mirrors;
- network observations;
- download timestamps;
- temporary inspection sessions.

## Deferred Decisions

Reserved for later stages:

- wire schema encoding;
- field naming;
- schema version strategy;
- API contracts;
- module implementation.

## Successor

`P13 Operation / Mutation Model`
