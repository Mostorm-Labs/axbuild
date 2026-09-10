# AXBUILD-NEARCAST-AIRPLAY-RELEASE-PUBLISH-P30-v0.1

## Stage

- Owner: `aegis-implementation`
- Stage: `P30 Implementation Planning`
- Target: successor P31 Task Packaging

## Purpose

Define the first AxBuild-owned internal dependency release publication slice for the NearCast AirPlay seed package.

This slice promotes an already qualified candidate package into an immutable internal release artifact. It does not migrate NearCast consumers.

## Authority Boundary

```text
NearCast
  - integration qualification
  - compatibility validation

AxBuild
  - dependency release authority
  - artifact identity
  - release index
  - provenance
  - SDK lock authority
  - resolver/store consumption
```

## Depends On

```yaml
previous_slice:
  package: NC-AIRPLAY-SEED-PACKAGE-P31-01
  result_revision: 5de6af60d43107bf62b192fb84bb8dda137542d7
  gate: P34_PASS
```

## Included

- create internal/private release publication workflow
- publish immutable seed package assets
- validate release index and provenance before publication
- preserve artifact identity across publication
- verify AxBuild resolver consumption from published release

## Excluded

- NearCast consumer migration
- replacing existing dependency restore path
- external redistribution qualification
- modifying NearCast runtime behavior
- changing AxBuild core ownership model

## Release Contract

Family:

```yaml
family: nearcast-airplay
kind: runtime
target: windows-x64
variant: release
visibility: internal
```

Assets:

```text
nearcast-airplay-runtime-windows-x64-release.zip
nearcast-airplay-sdk-index.json
nearcast-airplay-provenance.json
nearcast-airplay-sdk.lock.json
```

## Terminal Success

All must hold:

- immutable internal release exists
- release index validates
- provenance validates
- SDK lock validates
- resolver consumes published artifact
- offline replay remains valid

## Terminal Blockers

- AUTHORITY_CONFLICT
- MISSING_REQUIRED_INPUT
- ENVIRONMENT_BLOCKER
- FROZEN_VERIFICATION_FAILURE
- NEW_HIGH_IMPACT_FAILURE_MODE

## Future Migration

Consumer migration is a separate successor slice and is not authorized here.
