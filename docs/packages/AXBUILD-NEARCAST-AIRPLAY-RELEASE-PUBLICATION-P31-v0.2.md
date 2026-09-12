# AXBUILD-NEARCAST-AIRPLAY-RELEASE-PUBLICATION-P31-v0.2

## Stage

- Owner: `aegis-implementation`
- Stage: `P31 Task Packaging`
- Target: `P32 Implementation`
- Package ID: `AXBUILD-NEARCAST-AIRPLAY-RELEASE-PUBLICATION-P31-02`

## Purpose

Publish the already qualified NearCast AirPlay artifact candidate into the AxBuild private dependency release authority.

This slice begins only after C1 Artifact Qualification has passed.

## Authority

```text
Mostorm-Labs/axbuild
  - resolver
  - schemas
  - tooling

Mostorm-Labs/axdeps
  - internal dependency release assets
  - release lifecycle authority
```

## Dependencies

```yaml
artifact_qualification:
  repository: Mostorm-Labs/axbuild
  revision: 7134fb08dbb4a4edd12f9c3005759a84e6b89fde
  status: P34_PASS
```

## Required Changes

```yaml
implementation:
  required:
    - publish qualified artifact to axdeps
    - create immutable release identity
    - publish release index
    - publish provenance metadata
    - publish SDK lock metadata
    - validate AxBuild resolver consumption

  forbidden:
    - modify NearCast
    - migrate NearCast consumer
    - replace NEARCAST_AIRPLAY_DEPS_URL
    - publish external redistribution artifact
    - store binary release assets in axbuild source repository
    - overwrite immutable release assets
```

## Release Contract

```yaml
family: nearcast-airplay
kind: runtime
target: windows-x64
variant: release
visibility: private
repository: Mostorm-Labs/axdeps
```

## Required Outputs

```text
nearcast-airplay-runtime-windows-x64-release.zip
nearcast-airplay-sdk-index.json
nearcast-airplay-provenance.json
nearcast-airplay-sdk.lock.json
```

## EXECUTION_CLOSURE_CONTRACT

```yaml
implementation:
  required_changes:
    - private release publication
    - immutable artifact registration
    - release metadata validation

  forbidden_changes:
    - consumer migration
    - external redistribution
    - product repository changes

tests:
  required:
    - id: release-index-validation
      oracle: published index matches qualified artifact
    - id: provenance-validation
      oracle: provenance matches published artifact identity
    - id: lock-validation
      oracle: SDK lock resolves published release
    - id: resolver-validation
      oracle: AxBuild resolver consumes private release
    - id: immutability-check
      oracle: existing release assets cannot be overwritten

hosted_verification:
  required:
    - exact GitHub Actions result for publication revision

evidence:
  blocking:
    - qualification reference
    - release index digest
    - published artifact digest
    - resolver validation result

  corroborative:
    - publication log

terminal_success:
  all_of:
    - private release exists
    - assets match index
    - provenance matches artifact
    - resolver consumes release
    - immutable release rule validated

terminal_blockers:
  - AUTHORITY_CONFLICT
  - MISSING_REQUIRED_INPUT
  - ENVIRONMENT_BLOCKER
  - FROZEN_VERIFICATION_FAILURE
  - NEW_HIGH_IMPACT_FAILURE_MODE
```

## Non Goals

This package does not authorize:

- NearCast consumer migration
- public redistribution
- changing existing dependency restore paths
