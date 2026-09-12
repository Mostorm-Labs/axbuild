# AXBUILD-NEARCAST-AIRPLAY-RELEASE-PUBLICATION-P31-v0.4

## Stage

- Owner: `aegis-implementation`
- Stage: `P31 Task Packaging`
- Target: `P32 Implementation`
- Package ID: `AXBUILD-NEARCAST-AIRPLAY-RELEASE-PUBLICATION-P31-04`
- Supersedes: `AXBUILD-NEARCAST-AIRPLAY-RELEASE-PUBLICATION-P31-03`
- Reconciles terminal blocker: `IMMUTABILITY_CONFLICT`

## Purpose

Complete C2 private release publication without deleting, mutating, or reusing the non-immutable release created by the previous P32 attempt.

The previous implementation and publication outputs are preserved as evidence. The old release is not dependency authority. This package authorizes one new superseding release identity created after repository-level immutable releases were enabled in `Mostorm-Labs/axdeps`.

No NearCast consumer migration or public redistribution is authorized.

## Defect Classification

```yaml
previous_stage: P32
previous_status: IMMUTABILITY_CONFLICT
root_cause: TASK_PACKAGE_DEFECT
owning_layer: P31
reason: >-
  P31-03 froze an immutable-release success criterion but did not freeze the
  required temporal precondition that repository-level release immutability
  must already be enabled before creating the release. GitHub does not apply
  immutable-release protection retroactively.
```

## Preserved Valid Work

```yaml
implementation_result:
  repository: Mostorm-Labs/axbuild
  revision: 61982044b8f1974a0dddfaa4cd32b4e9236107fb
  materialized_ref: github:Mostorm-Labs/axbuild:pull/5/head@61982044b8f1974a0dddfaa4cd32b4e9236107fb

validated:
  qualification-input-integrity: pass
  release-index-validation: pass
  provenance-validation: pass
  lock-validation: pass
  published-asset-integrity: pass
  resolver-online-validation-local: pass
  resolver-offline-validation-local: pass
  local_tests: 67 passed

hosted:
  axbuild_ci:
    run_id: 34692302948
    conclusion: success
  failed_release_verification:
    repository: Mostorm-Labs/axdeps
    run_id: 34692527126
    job_id: 103550208788
    conclusion: failure
    reason: published release must have GitHub immutability enabled
    evidence_artifact_id: 10298195735
```

The executor MUST preserve valid implementation work and must not replay or redesign completed functionality unless necessary to bind the new frozen release identity.

## Exact Qualified Artifact Input

```yaml
artifact_identity: nearcast-airplay-runtime-windows-x64-release-26bdd0c07de1c6db
runtime_asset: nearcast-airplay-runtime-windows-x64-release.zip
runtime_sha256: 0a085cdb439e4d3dbe517d83e40898d6a124ea689ec24cd987b49d7ccf74c44e
redistribution_status: review-required

qualification_evidence:
  run_id: 34686774827
  job_id: 103535012902
  artifact_id: 10295767679
  artifact_zip_sha256: e3b3071fe0d3c8af240756766fac19178526fd8a711b260fa5f34f4f2859c290
  gate_ref: github:Mostorm-Labs/axbuild:pull/5#issuecomment-5645236338
```

## Superseded Failed Publication

The following release MUST be preserved unchanged and MUST NOT be used as dependency authority:

```yaml
repository: Mostorm-Labs/axdeps
release_id: 387538376
release_tag: nearcast-airplay-runtime-windows-x64-release-26bdd0c07de1c6db
release_url: https://github.com/Mostorm-Labs/axdeps/releases/tag/nearcast-airplay-runtime-windows-x64-release-26bdd0c07de1c6db
immutable: false
classification: superseded_failed_publication

assets:
  runtime:
    id: 559090110
    sha256: 0a085cdb439e4d3dbe517d83e40898d6a124ea689ec24cd987b49d7ccf74c44e
  index:
    id: 559090109
    sha256: 24c85e5d1884898dee5b50589dd31b9d539733d48bd1e5f3720f37613817c0b5
  provenance:
    id: 559090116
    sha256: 12cd347c8c589deff501b3b4526f8671d9dbf86cc94ab326b306f8b832e4fb7e
  lock:
    id: 559090111
    sha256: 61c077732d48fe359ebdc7b41c1ec70f018a277991cc99dc8d845bf4fa552f6b
```

Forbidden operations on this release:

- delete the release;
- delete or move the tag;
- replace or overwrite an asset;
- mutate metadata in order to make it appear authoritative;
- resolve consumer dependencies from this tag.

## Release Authority Preconditions

```yaml
repository: Mostorm-Labs/axdeps
visibility: private
repository_release_immutability:
  required_before_creation: true
  observed_state_expected: enabled
```

P32 must fail closed before creating the new release if repository-level immutable releases are not enabled.

## Frozen Superseding Release Identity

```yaml
family: nearcast-airplay
kind: runtime
target: windows-x64
variant: release

repository: Mostorm-Labs/axdeps
release_tag: nearcast-airplay-runtime-windows-x64-release-26bdd0c07de1c6db-r2
release_set_id: nearcast-airplay-set-26bdd0c07de1c6db-r2

runtime_asset: nearcast-airplay-runtime-windows-x64-release.zip
index_asset: nearcast-airplay-sdk-index.json
provenance_asset: nearcast-airplay-provenance.json
lock_asset: nearcast-airplay-sdk.lock.json
```

Artifact identity remains `nearcast-airplay-runtime-windows-x64-release-26bdd0c07de1c6db`; only publication/release-set identity changes.

The executor MUST NOT invent another tag, use `latest`, reuse the old tag, or delete/recreate the old tag.

## Required Changes

```yaml
implementation:
  required_changes:
    - reconcile existing P32 implementation at revision 61982044b8f1974a0dddfaa4cd32b4e9236107fb
    - verify repository-level immutable releases are enabled before new release creation
    - regenerate release index and SDK lock for the frozen r2 release_tag/release_set_id
    - preserve exact qualified runtime bytes and artifact identity
    - preserve provenance and redistribution.status=review-required
    - create the new private release at the exact r2 tag
    - upload exactly runtime/index/provenance/lock assets
    - verify GitHub reports immutable=true for the new release after publication
    - verify published asset digests by downloading the new release assets
    - validate release index and SDK lock
    - validate resolver online consumption from an empty store using only the r2 tag
    - validate resolver offline replay from the populated store
    - verify old non-immutable tag is never selected by the new lock/resolver test

  forbidden_changes:
    - delete or mutate the previous non-immutable release/tag/assets
    - modify Mostorm-Labs/NearCast
    - migrate NearCast consumer configuration
    - replace NEARCAST_AIRPLAY_DEPS_URL
    - public redistribution
    - change redistribution.status
    - change qualified runtime bytes
    - use a floating/latest release selector
```

## EXECUTION_CLOSURE_CONTRACT

```yaml
continue_until_terminal_state: true

package_binding_preflight:
  required:
    - exact package_ref resolves in Mostorm-Labs/axbuild
    - task_anchor ancestry is valid
    - previous P32 result revision 61982044b8f1974a0dddfaa4cd32b4e9236107fb is resolvable
    - old release 387538376 still exists with immutable=false and exact preserved asset digests
    - repository-level immutable releases are enabled before r2 creation
    - r2 release tag does not already exist, unless an exact immutable release can be reconciled without mutation
    - exact qualification artifact/evidence remains resolvable

implementation:
  required_changes:
    - superseding immutable private release publication
    - r2 release index generation and validation
    - r2 SDK lock generation and validation
    - published asset integrity validation
    - online resolver validation against r2 only
    - offline resolver replay
    - immutable release verification

  forbidden_changes:
    - old release deletion or mutation
    - consumer migration
    - public redistribution
    - NearCast repository changes
    - qualified artifact mutation

tests:
  required:
    - id: old-release-preservation
      oracle: release 387538376 remains unchanged and immutable=false

    - id: precreation-immutability-precondition
      oracle: repository immutable-release policy is enabled before r2 release creation

    - id: r2-release-immutability
      oracle: GitHub reports immutable=true for the published r2 release

    - id: qualification-input-integrity
      oracle: r2 runtime asset SHA256 equals 0a085cdb439e4d3dbe517d83e40898d6a124ea689ec24cd987b49d7ccf74c44e

    - id: release-index-validation
      oracle: r2 index validates and selects the exact qualified artifact identity/digest

    - id: provenance-validation
      oracle: provenance matches the artifact identity and remains review-required

    - id: lock-validation
      oracle: SDK lock binds exactly to Mostorm-Labs/axdeps, the r2 release tag, r2 release_set_id, index asset and index digest

    - id: published-asset-integrity
      oracle: all four downloaded r2 assets match their expected/referenced digests

    - id: resolver-online-validation
      oracle: an empty store resolves through the r2 private release and never selects the old tag

    - id: resolver-offline-validation
      oracle: populated-store offline resolution succeeds without network/source-build fallback

hosted_verification:
  required:
    - exact GitHub Actions result bound to the P32 result revision
    - exact axdeps verification run proving r2 immutable=true and resolver/integrity checks

  optional:
    - local reproduction

evidence:
  blocking:
    - exact r2 release URL/tag/id with immutable=true
    - exact runtime SHA256
    - exact r2 index SHA256
    - exact provenance and lock refs
    - exact hosted run/job refs
    - online resolver result against r2
    - offline replay result
    - proof old release remained unchanged and is not selected

  corroborative:
    - local test output
    - publication log

terminal_success:
  all_of:
    - old non-immutable publication remains preserved and non-authoritative
    - r2 private release exists and GitHub reports immutable=true
    - r2 runtime bytes equal the qualified artifact bytes
    - r2 index/provenance/lock validate
    - r2 lock and resolver never select the old release
    - online resolver succeeds against r2 from an empty store
    - offline replay succeeds from the populated store
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

```yaml
stage: P32
status: READY_FOR_CONTROL_REVIEW | <explicit terminal blocker>
result_revision: <exact axbuild commit>
materialized_ref: <exact reviewer-accessible axbuild PR/head ref>

release_refs:
  repository: Mostorm-Labs/axdeps
  superseded_release:
    id: 387538376
    tag: nearcast-airplay-runtime-windows-x64-release-26bdd0c07de1c6db
    immutable: false
    unchanged: true
  authoritative_release:
    id: <exact r2 release id>
    tag: nearcast-airplay-runtime-windows-x64-release-26bdd0c07de1c6db-r2
    url: <exact r2 release URL>
    immutable: true

digests:
  runtime_sha256: 0a085cdb439e4d3dbe517d83e40898d6a124ea689ec24cd987b49d7ccf74c44e
  index_sha256: <exact r2 index sha256>
  provenance_sha256: <exact sha256>
  lock_sha256: <exact sha256>

provider_run_refs:
  - provider: github-actions
    repository: Mostorm-Labs/axbuild
    run_id: <exact run>
    job_id: <exact job(s)>
  - provider: github-actions
    repository: Mostorm-Labs/axdeps
    run_id: <exact verification run>
    job_id: <exact job>

evidence_input_refs:
  - old-release-preservation
  - precreation-immutability-precondition
  - r2-release-immutability
  - qualification-input-integrity
  - release-index-validation
  - provenance-validation
  - lock-validation
  - published-asset-integrity
  - resolver-online-validation
  - resolver-offline-validation

notes:
  - no NearCast migration
  - no public redistribution
  - no P34 PASS claim
```

P32 must not claim or imply P34 PASS.
