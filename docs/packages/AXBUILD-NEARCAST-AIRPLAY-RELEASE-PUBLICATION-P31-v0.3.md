# AXBUILD-NEARCAST-AIRPLAY-RELEASE-PUBLICATION-P31-v0.3

## Stage

- Owner: `aegis-implementation`
- Stage: `P31 Task Packaging`
- Target: `P32 Implementation`
- Package ID: `AXBUILD-NEARCAST-AIRPLAY-RELEASE-PUBLICATION-P31-03`
- Supersedes: `AXBUILD-NEARCAST-AIRPLAY-RELEASE-PUBLICATION-P31-02`

## Purpose

Publish the exact C1.5-qualified NearCast AirPlay artifact instance into the private AxBuild dependency release authority in `Mostorm-Labs/axdeps`, then prove that AxBuild can resolve the published immutable release.

This package reconciles the previous C2 package after the earlier `MISSING_REQUIRED_INPUT` / evidence-binding failure. It binds the real qualified artifact instance, its digest, reviewer-accessible artifact, and durable P34 Gate result.

It does not authorize NearCast consumer migration or public redistribution.

## Authority Boundary

```text
Mostorm-Labs/axbuild
  - publication tooling / resolver / schemas / validation
  - C2 implementation repository

Mostorm-Labs/axdeps
  - private immutable dependency release authority
  - release tag and release assets

Mostorm-Labs/NearCast
  - source of the already-qualified dependency closure only
  - no changes authorized by this package
```

## Exact C1.5 Qualified Input

```yaml
qualification:
  repository: Mostorm-Labs/axbuild
  result_revision: f2f1dd6161f39110c5022743212f882186080440
  materialized_ref: github:Mostorm-Labs/axbuild:pull/5/head@f2f1dd6161f39110c5022743212f882186080440
  accepted_tooling_revision: c121c2a380209d4472a785f1746b9aa4d853008c

  source:
    repository: Mostorm-Labs/NearCast
    release_tag: airplay-deps-windows-x64-20260814-162942
    asset: nearcast-airplay-deps-windows-x64-20260814-162942.zip
    sha256: 0768c47f3df888bddbca7531299f11776188d2ee029332294a1af08bb2f1575c

  qualified_artifact:
    artifact_identity: nearcast-airplay-runtime-windows-x64-release-26bdd0c07de1c6db
    archive_asset: nearcast-airplay-runtime-windows-x64-release.zip
    archive_sha256: 0a085cdb439e4d3dbe517d83e40898d6a124ea689ec24cd987b49d7ccf74c44e
    file_count: 3821
    redistribution_status: review-required

  reviewer_artifact:
    provider: github-actions
    run_id: 34686774827
    job_id: 103535012902
    artifact_id: 10295767679
    artifact_name: nearcast-airplay-qualification-d6338ff3bf63822fec8e1c1bbbdb4218224f70e7
    artifact_zip_sha256: e3b3071fe0d3c8af240756766fac19178526fd8a711b260fa5f34f4f2859c290
    expires_at: 2026-09-26T09:48:22Z

  gate:
    stage: P34
    result: PASS
    durable_ref: github:Mostorm-Labs/axbuild:pull/5#issuecomment-5645236338
```

The executor MUST resolve this exact reviewer artifact before publication. A missing, expired, mismatched, or differently hashed input is terminal `MISSING_REQUIRED_INPUT`; it must not be reconstructed from an unpinned source.

## Release Authority Preflight

```yaml
release_authority:
  repository: Mostorm-Labs/axdeps
  visibility: private
  default_branch: main
  required_access: release-write
```

P32 must fail closed as `BLOCKED_EXECUTION_AUTHORITY` if it cannot create a private GitHub Release and upload assets to `Mostorm-Labs/axdeps`.

## Frozen Release Identity

```yaml
family: nearcast-airplay
kind: runtime
target: windows-x64
variant: release

repository: Mostorm-Labs/axdeps
release_tag: nearcast-airplay-runtime-windows-x64-release-26bdd0c07de1c6db
release_set_id: nearcast-airplay-set-26bdd0c07de1c6db

index_asset: nearcast-airplay-sdk-index.json
provenance_asset: nearcast-airplay-provenance.json
lock_asset: nearcast-airplay-sdk.lock.json
runtime_asset: nearcast-airplay-runtime-windows-x64-release.zip
```

The release tag and release set ID above are exact. The executor must not invent a version, use `latest`, replace an existing tag, or rename the assets.

Before creating anything, P32 must verify that the frozen release tag does not already exist. If it exists with any mismatching asset or digest, return `IMMUTABILITY_CONFLICT` and stop. If an exact already-published release is discovered, return the exact release/evidence refs for control reconciliation rather than overwriting it.

## Required Changes

```yaml
implementation:
  required_changes:
    - resolve and verify the exact C1.5 reviewer artifact
    - verify qualified runtime archive SHA256 before publication
    - generate an AxBuild release index for the frozen release_set_id
    - carry forward the qualified provenance without relaxing redistribution.status
    - generate an AxBuild SDK lock bound to Mostorm-Labs/axdeps and the frozen release tag
    - create the immutable private GitHub Release in Mostorm-Labs/axdeps
    - upload exactly the frozen runtime/index/provenance/lock assets
    - verify every published asset by downloaded bytes and digest
    - validate release index and SDK lock using AxBuild contracts
    - validate online resolver consumption from an empty store using the private release
    - validate offline replay from the populated store without network fallback
    - verify the release cannot be silently overwritten

  forbidden_changes:
    - modify Mostorm-Labs/NearCast
    - migrate any NearCast consumer
    - replace NEARCAST_AIRPLAY_DEPS_URL
    - create or modify a consumer lock in NearCast
    - publish the dependency bytes publicly
    - change redistribution.status from review-required
    - store third-party binary release assets in the axbuild git tree
    - use latest/floating release references
    - overwrite or mutate an existing release/tag/asset
```

## Required Published Outputs

The private `Mostorm-Labs/axdeps` release must contain exactly the required publication outputs:

```text
nearcast-airplay-runtime-windows-x64-release.zip
nearcast-airplay-sdk-index.json
nearcast-airplay-provenance.json
nearcast-airplay-sdk.lock.json
```

Additional diagnostic files are not blocking outputs and must not become dependency authority.

## EXECUTION_CLOSURE_CONTRACT

```yaml
continue_until_terminal_state: true

package_binding_preflight:
  required:
    - exact package_ref resolves in Mostorm-Labs/axbuild
    - task_anchor ancestry is valid
    - reviewer artifact 10295767679 is accessible and unexpired
    - reviewer artifact zip digest equals e3b3071fe0d3c8af240756766fac19178526fd8a711b260fa5f34f4f2859c290
    - runtime archive digest equals 0a085cdb439e4d3dbe517d83e40898d6a124ea689ec24cd987b49d7ccf74c44e
    - durable P34 Gate ref 5645236338 is resolvable
    - Mostorm-Labs/axdeps is private and writable by the execution credential
    - frozen release tag is absent or exactly reconcilable without mutation

implementation:
  required_changes:
    - private immutable release publication
    - release index generation and validation
    - provenance publication and validation
    - SDK lock generation and validation
    - online resolver consumption validation
    - offline replay validation
    - immutable-release protection validation

  forbidden_changes:
    - consumer migration
    - external/public redistribution
    - NearCast repository changes
    - product runtime changes
    - floating dependency selection
    - immutable release overwrite

tests:
  required:
    - id: qualification-input-integrity
      oracle: reviewer artifact and runtime archive match all frozen digests and identity

    - id: release-index-validation
      oracle: index validates against axbuild-release-index-v1 and selects the exact qualified artifact identity/digest

    - id: provenance-validation
      oracle: published provenance matches the exact artifact identity and keeps redistribution.status=review-required

    - id: lock-validation
      oracle: SDK lock validates against axbuild-sdk-lock-v1 and binds repository/releaseTag/releaseSetId/indexAsset/indexSha256 exactly

    - id: published-asset-integrity
      oracle: assets downloaded from the private axdeps release hash to the values referenced by release metadata

    - id: resolver-online-validation
      oracle: from an empty AxBuild store, resolution succeeds through the private axdeps release and materializes the exact artifact

    - id: resolver-offline-validation
      oracle: after the online resolve populates the store, offline resolution succeeds without network/source-build fallback

    - id: immutability-check
      oracle: publication logic refuses an existing mismatching tag or asset and never overwrites it

hosted_verification:
  required:
    - exact GitHub Actions result bound to the P32 result revision
    - publication/resolution verification must be reviewer-accessible

  optional:
    - additional local reproduction

evidence:
  blocking:
    - exact C1.5 qualification refs and P34 durable Gate ref
    - exact axdeps release URL/tag
    - exact published runtime archive SHA256
    - exact release index SHA256
    - exact provenance ref and validation result
    - exact SDK lock ref and validation result
    - exact online resolver validation result
    - exact offline replay validation result
    - exact hosted provider run/job refs

  corroborative:
    - publication log
    - local reproduction output

terminal_success:
  all_of:
    - exact C1.5 qualified artifact is published to the frozen private axdeps release
    - release assets are immutable and match their referenced digests
    - release index validates and points to the exact artifact
    - provenance validates and remains review-required
    - SDK lock validates and points only to the frozen axdeps release/index
    - online resolver consumes the private release from an empty store
    - offline replay consumes the populated store without network fallback
    - reviewer-accessible hosted evidence is materialized

terminal_blockers:
  explicit_classes:
    - BLOCKED_REPOSITORY_IDENTITY
    - BLOCKED_EXECUTION_AUTHORITY
    - AUTHORITY_CONFLICT
    - MISSING_REQUIRED_INPUT
    - IMMUTABILITY_CONFLICT
    - ENVIRONMENT_BLOCKER
    - FROZEN_VERIFICATION_FAILURE
    - NEW_HIGH_IMPACT_FAILURE_MODE
```

## Return Contract

P32 returns to `CONTROL_REVIEW` with exact identities, not prose-only claims:

```yaml
stage: P32
status: READY_FOR_CONTROL_REVIEW | <explicit terminal blocker>
result_revision: <exact axbuild commit>
materialized_ref: <exact reviewer-accessible axbuild PR/head ref>

release_refs:
  repository: Mostorm-Labs/axdeps
  release_tag: nearcast-airplay-runtime-windows-x64-release-26bdd0c07de1c6db
  release_url: <exact URL>
  assets:
    runtime: <exact asset ref>
    index: <exact asset ref>
    provenance: <exact asset ref>
    lock: <exact asset ref>

digests:
  runtime_sha256: 0a085cdb439e4d3dbe517d83e40898d6a124ea689ec24cd987b49d7ccf74c44e
  index_sha256: <exact sha256>

provider_run_refs:
  - provider: github-actions
    workflow: <exact workflow>
    run_id: <exact run>
    job_id: <exact job>

evidence_input_refs:
  - qualification-input-integrity
  - release-index-validation
  - provenance-validation
  - lock-validation
  - published-asset-integrity
  - resolver-online-validation
  - resolver-offline-validation
  - immutability-check

notes:
  - no NearCast migration
  - no public redistribution
  - no P34 PASS claim
```

P32 must not claim or imply P34 PASS.