# AXBUILD-NEARCAST-AIRPLAY-ARTIFACT-QUALIFICATION-RUN-P31-v0.1

## Stage

- Owner: `aegis-implementation`
- Stage: `P31 Task Packaging`
- Target: `P32 Implementation`
- Package ID: `AXBUILD-NEARCAST-AIRPLAY-ARTIFACT-QUALIFICATION-RUN-P31-01`

## Purpose

Execute the first real NearCast AirPlay artifact qualification run using the already accepted AxBuild qualification tooling.

This slice creates a qualified artifact instance that can become input to a later private release publication slice.

It does not publish a release.

## Ownership Boundary

```text
NearCast
  - dependency closure input
  - integration context
  - compatibility information

AxBuild
  - qualification execution
  - artifact identity
  - manifest
  - provenance
  - qualification evidence
```

## Dependencies

```yaml
qualification_tooling:
  repository: Mostorm-Labs/axbuild
  revision: 7134fb08dbb4a4edd12f9c3005759a84e6b89fde
  status: P34_PASS
```

## EXECUTION_CLOSURE_CONTRACT

```yaml
implementation:
  required_changes:
    - execute artifact qualification against real dependency closure
    - materialize qualified artifact outputs
    - record artifact digest
    - produce qualification evidence

  forbidden_changes:
    - publish axdeps release
    - create release tag
    - create Release Asset
    - modify NearCast consumer path
    - replace NEARCAST_AIRPLAY_DEPS_URL

 tests:
  required:
    - id: artifact-qualification
      oracle: qualification command succeeds
    - id: manifest-validation
      oracle: generated manifest matches archive contents
    - id: provenance-validation
      oracle: provenance matches artifact identity
    - id: digest-validation
      oracle: generated archive digest is recorded

hosted_verification:
  required:
    - exact GitHub Actions result for qualification execution

 evidence:
  blocking:
    - artifact manifest
    - provenance
    - qualification report
    - artifact sha256

terminal_success:
  all_of:
    - qualified artifact instance exists
    - artifact identity is deterministic
    - manifest validates
    - provenance validates
    - qualification evidence is reviewer accessible

terminal_blockers:
  explicit_classes:
    - AUTHORITY_CONFLICT
    - MISSING_REQUIRED_INPUT
    - ENVIRONMENT_BLOCKER
    - FROZEN_VERIFICATION_FAILURE
    - NEW_HIGH_IMPACT_FAILURE_MODE
```

## Required Outputs

```text
nearcast-airplay-runtime-windows-x64-release.zip
nearcast-airplay-artifact-manifest.json
nearcast-airplay-provenance.json
qualification-report.json
```

## Explicit Non-Goals

- No axdeps publication
- No release tag
- No consumer migration
- No redistribution approval
