# AXBUILD-NEARCAST-AIRPLAY-ARTIFACT-QUALIFICATION-P31-v0.1

## Stage

- Owner: `aegis-implementation`
- Stage: `P31 Task Packaging`
- Target: `P32 Implementation`
- Package ID: `AXBUILD-NEARCAST-AIRPLAY-ARTIFACT-QUALIFICATION-P31-01`

## Purpose

Create the first qualified AxBuild artifact candidate for the NearCast AirPlay dependency family.

This slice produces a verified artifact candidate. It does not publish a release and does not migrate any consumer.

## Ownership Boundary

```text
NearCast
  - integration validation
  - dependency closure source
  - compatibility evidence

AxBuild
  - artifact identity
  - package contract
  - provenance
  - qualification result
```

## Required Changes

```yaml
implementation:
  required:
    - generate deterministic artifact manifest
    - generate artifact identity
    - generate provenance metadata
    - validate package schema
    - generate qualification report

  forbidden:
    - publish GitHub Release
    - create release tag
    - modify NearCast consumer path
    - replace NEARCAST_AIRPLAY_DEPS_URL
    - claim external redistribution approval
```

## Qualification Outputs

```text
nearcast-airplay-runtime-windows-x64-release.zip
nearcast-airplay-artifact-manifest.json
nearcast-airplay-provenance.json
qualification-report.json
```

## EXECUTION_CLOSURE_CONTRACT

```yaml
implementation:
  required_changes:
    - artifact qualification tooling
    - deterministic manifest generation
    - provenance generation
  forbidden_changes:
    - release publication
    - consumer migration

tests:
  required:
    - id: manifest-validation
      oracle: artifact manifest validates against schema
    - id: identity-determinism
      oracle: identical inputs produce identical identity
    - id: provenance-validation
      oracle: provenance matches artifact manifest
    - id: archive-integrity
      oracle: archive hash remains stable

hosted_verification:
  required:
    - exact GitHub Actions result on implementation revision

evidence:
  blocking:
    - manifest validation result
    - provenance validation result
    - artifact hash result
  corroborative:
    - qualification report

terminal_success:
  all_of:
    - deterministic artifact identity exists
    - manifest validates
    - provenance validates
    - qualification report generated

terminal_blockers:
  explicit_classes:
    - AUTHORITY_CONFLICT
    - MISSING_REQUIRED_INPUT
    - ENVIRONMENT_BLOCKER
    - FROZEN_VERIFICATION_FAILURE
    - NEW_HIGH_IMPACT_FAILURE_MODE
```

## Next Boundary

A successful C1 qualification may become input to a later release publication slice.
It does not authorize publication or consumer migration.