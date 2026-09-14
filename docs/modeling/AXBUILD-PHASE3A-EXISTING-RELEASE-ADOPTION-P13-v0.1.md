# AxBuild Phase 3A Generic Existing-Release Adoption — P13 Operation / Mutation Model v0.1

## Stage

- Owner: `aegis-modeling`
- Stage: `P13 Operation / Mutation Model`
- Phase: `Phase 3 — Platform Generalization`
- Capability: `Phase 3A — Generic Existing-Release Adoption`
- Status: `READY`

## Role

Define canonical mutation boundaries and lifecycle operations after P10 Product Object Model, P11 Interaction / Behavior, and P12 Semantic Schema.

P13 defines semantic operations, atomicity, idempotency, replay, ordering, compatibility, and failure behavior. It does not define API, CLI, database, or implementation classes.

## Operation Classes

### Read Operations

Do not mutate canonical truth.

Examples:

- `InspectExistingRelease`
- `ValidateAdoptionAuthority`
- `ResolveAdoptedRelease`

Runtime facts and diagnostics are derived outputs only.

### Qualification Operations

Produce durable evidence but do not establish authority.

Primary operation:

- `QualifyExistingRelease`

Output:

- `SourceIntegrityQualification`
- `AdoptionCompatibilityResult`
- `AdoptionQualificationResult`

Qualification does not create `AdoptionAuthority`.

### Canonical Mutations

Only explicit mutations may change canonical adoption truth:

- `EstablishAdoptionAuthority`
- `InvalidateAdoptionAuthority`
- `SupersedeAdoptionAuthority`

## Core Operations

## QualifyExistingRelease

Purpose:

Determine whether an existing project-owned release satisfies the adoption contract.

Inputs:

- ExistingReleaseSource
- inspection result
- integrity contract
- artifact mapping candidate

Checks:

- exact source identity
- artifact mapping
- digest integrity
- ownership preservation
- release-set coherence
- family-neutral representability

Outcomes:

- `ADOPTABLE`
- `UNSUPPORTED`
- `INVALID`

## EstablishAdoptionAuthority

Creates canonical adoption truth.

Preconditions:

- qualification outcome is ADOPTABLE
- source identity is exact
- artifact mappings are complete
- ownership is preserved

Atomic commit:

- AdoptionAuthority
- AdoptedReleaseSet
- Artifact mappings
- qualification linkage

Partial authority is invalid canonical state.

## ValidateAdoptionAuthority

Read-only validation.

Must not update authority when source reality changes.

Contradictions produce failure; durable invalidation requires explicit mutation.

## InvalidateAdoptionAuthority

Records that an authority is no longer actionable.

Does not delete historical authority or qualification records.

## SupersedeAdoptionAuthority

Creates a successor authority and links lineage.

Old authority remains historical.

In-place overwrite is forbidden.

## Idempotency

Identical establishment input must resolve to the same semantic authority identity.

Changes to source release, artifact digest, mapping, ownership, or contract require new identity or explicit supersession.

Duplicate conflicting authorities are forbidden.

## Replay

Qualification replay with identical inputs must be deterministic.

Authority establishment replay must not create duplicate canonical truth.

Runtime resolve replay cannot mutate authority.

## Ordering Rules

Valid lifecycle:

Inspect → Qualify → Establish → Validate → Invalidate/Supersede

Forbidden:

- Establish before qualification
- Resolve creating authority
- Validation silently changing authority
- Retry selecting another release

## Failure Rules

All authority-sensitive operations fail closed.

Forbidden fallbacks:

- latest release selection
- digest weakening
- source rebuild
- republish
- ownership transfer
- overwrite conflicting authority

## Compatibility Boundary

Existing authority remains readable after semantic evolution.

Changed source identity, artifact bytes, or ownership requires explicit new identity or supersession relation.

## Successor

Next stage: `P14 System Architecture`
