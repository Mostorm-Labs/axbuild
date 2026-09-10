# AXBUILD-NEARCAST-AIRPLAY-RELEASE-PUBLISH-P31-v0.1

## Stage

- Owner: `aegis-implementation`
- Stage: `P31 Task Packaging`
- Target: `P32 Implementation`
- Package ID: `AXBUILD-NEARCAST-AIRPLAY-RELEASE-PUBLISH-P31-01`

## Purpose

Publish the first AxBuild-owned internal dependency release from the qualified NearCast AirPlay seed package.

This slice publishes dependency artifacts only. It does not migrate any consumer.

## Authority Boundary

```text
NearCast
  - integration qualification
  - compatibility validation

AxBuild
  - release authority
  - artifact identity
  - release index
  - provenance
  - SDK lock
  - resolver/store consumption
```

## Dependencies

```yaml
seed_package:
  repository: Mostorm-Labs/axbuild
  revision: 5de6af60d43107bf62b192fb84bb8dda137542d7
  gate: P34_PASS
```

## EXECUTION_CLOSURE_CONTRACT

```yaml
implementation:
  required_changes:
    - create internal immutable release workflow
    - publish runtime archive asset
    - publish release index asset
    - publish provenance asset
    - publish SDK lock asset
    - verify published release through resolver

  forbidden_changes:
    - modify NearCast consumer path
    - promote NearCast lock
    - external redistribution claim
    - replace existing release tags
    - add product-specific logic into AxBuild core

tests:
  required:
    - id: release-index-validation
      command_or_oracle: axbuild validate-index
      expected_result: success
      blocking_reason: release metadata integrity

    - id: sdk-lock-validation
      command_or_oracle: axbuild validate-lock
      expected_result: success
      blocking_reason: consumer resolution integrity

    - id: published-artifact-resolution
      command_or_oracle: resolve published package from clean store
      expected_result: success
      blocking_reason: release usability

    - id: offline-replay
      command_or_oracle: resolve from materialized store without network
      expected_result: success
      blocking_reason: reproducibility

hosted_verification:
  required:
    - GitHub Actions validation at exact result revision

evidence:
  blocking:
    - release index validation
    - lock validation
    - resolver validation
    - offline replay result
  corroborative:
    - provenance metadata

terminal_success:
  all_of:
    - immutable internal release exists
    - assets match release index
    - provenance matches artifact identity
    - resolver consumes published release
    - offline replay succeeds

terminal_blockers:
  explicit_classes:
    - AUTHORITY_CONFLICT
    - MISSING_REQUIRED_INPUT
    - ENVIRONMENT_BLOCKER
    - FROZEN_VERIFICATION_FAILURE
    - NEW_HIGH_IMPACT_FAILURE_MODE

return_policy:
  continue_until_terminal_state: true
```

## Explicit Non-Goals

- No NearCast consumer migration.
- No replacement of existing dependency restore path.
- No public redistribution qualification.
- No deletion of legacy dependency archive.
