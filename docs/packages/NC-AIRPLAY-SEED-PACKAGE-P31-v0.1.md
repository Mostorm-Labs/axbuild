# NC-AIRPLAY-SEED-PACKAGE-P31-v0.1

## Stage

- Owner: `aegis-implementation`
- Stage: `P31 Task Packaging`
- Package ID: `NC-AIRPLAY-SEED-PACKAGE-P31-01`
- Target: `P32 Implementation`

## Purpose

Create the first AxBuild dependency seed package for the NearCast AirPlay dependency family.

This package establishes AxBuild as the dependency release authority. NearCast remains an integration consumer and validation source only.

## Ownership Boundary

```text
NearCast
  - existing dependency closure
  - provider integration
  - compatibility validation

AxBuild
  - artifact identity
  - release index
  - provenance
  - SDK lock
  - resolver/store validation
```

## Repository Identity

```yaml
repository:
  provider: github
  full_name: Mostorm-Labs/axbuild

execution_branch:
  codex/nearcast-airplay-seed-package-v0.1
```

## Dependencies

```yaml
depends_on:
  nearcast_validation:
    repository: Mostorm-Labs/NearCast
    reference: PR-139
    purpose: integration qualification only
```

## Required Changes

```yaml
implementation:
  required_changes:
    - define nearcast-airplay seed package schema
    - define artifact identity generation
    - define release index generation
    - define provenance metadata format
    - validate package through AxBuild resolver

  forbidden_changes:
    - modify NearCast consumer path
    - migrate NEARCAST_AIRPLAY_DEPS_URL usage
    - publish external redistribution artifact
    - modify AXTP/Axent contracts
    - place product-specific release authority in AxBuild core
```

## Package Model

```yaml
family: nearcast-airplay
kind: runtime
target: windows-x64
variant: release
```

## Required Outputs

```text
nearcast-airplay-runtime-windows-x64-release.zip
nearcast-airplay-sdk-index.json
nearcast-airplay-provenance.json
nearcast-airplay-sdk.lock.json
```

## Required Validation

```yaml
tests:
  required:
    - id: index-validation
      oracle: axbuild validate-index succeeds

    - id: lock-validation
      oracle: axbuild validate-lock succeeds

    - id: clean-store-resolution
      oracle: empty store resolves artifact successfully

    - id: offline-replay
      oracle: materialized store resolves without network
```

## Hosted Verification

Required:

```yaml
- GitHub Actions validation against exact result revision
```

## Evidence

Blocking:

```yaml
- release index validation result
- lock validation result
- resolver online/offline validation result
```

Corroborative:

```yaml
- package provenance metadata
- integration notes from NearCast
```

## Terminal Success

All of:

```text
AxBuild package identity is deterministic

AND

Release index validates

AND

SDK lock validates

AND

Resolver consumes package

AND

Offline replay succeeds
```

## Terminal Blockers

```yaml
- AUTHORITY_CONFLICT
- MISSING_REQUIRED_INPUT
- ENVIRONMENT_BLOCKER
- FROZEN_VERIFICATION_FAILURE
- NEW_HIGH_IMPACT_FAILURE_MODE
```

## Explicit Non-Goal

This package does not authorize consumer migration. A future migration slice must separately promote the SDK lock into NearCast consumption.