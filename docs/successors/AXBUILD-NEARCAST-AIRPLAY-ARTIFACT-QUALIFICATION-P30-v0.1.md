# AXBUILD-NEARCAST-AIRPLAY-ARTIFACT-QUALIFICATION-P30-v0.1

## Stage

- Owner: `aegis-implementation`
- Stage: `P30 Implementation Planning`
- Successor of: `AXBUILD-NEARCAST-AIRPLAY-RELEASE-PUBLISH-P30-v0.1`

## Purpose

Define the first AxBuild-owned artifact qualification slice for the NearCast AirPlay dependency family.

This slice exists before release publication. It converts a validated dependency closure into a qualified artifact candidate with complete identity, provenance, and reproducibility information.

Release publication is a separate successor slice.

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
  - future release input
```

## Scope

Included:

- deterministic artifact identity generation
- archive manifest generation
- SHA256 calculation
- provenance generation
- package schema validation
- qualification report generation

Excluded:

- GitHub Release creation
- release tag creation
- consumer migration
- redistribution approval
- NearCast runtime changes

## Artifact Family

```yaml
family: nearcast-airplay
kind: runtime
target: windows-x64
variant: release
```

## Required Qualification Output

```text
nearcast-airplay-runtime-windows-x64-release.zip
nearcast-airplay-artifact-manifest.json
nearcast-airplay-provenance.json
qualification-report.json
```

## Required Verification

- artifact identity is deterministic
- manifest matches archive contents
- provenance matches artifact identity
- schema validation succeeds
- qualified artifact can be consumed by AxBuild resolver in a local mirror

## Success Boundary

A successful qualification produces a release-ready candidate.

It does not create a release.

The following publication slice requires a separate package:

```text
qualified artifact candidate
        |
        v
AxBuild release publication
```
