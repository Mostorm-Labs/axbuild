# AXBUILD-NEARCAST-AIRPLAY-RELEASE-AUTHORITY-RESOLUTION-P31-v0.1

## Stage

- Owner: `aegis-implementation`
- Purpose: resolve release authority before C2 publication
- Predecessor: C1 Artifact Qualification PASS

## Authority Decision

The release authority is separated from the public AxBuild tooling repository.

```text
Mostorm-Labs/axbuild
  - resolver
  - schemas
  - tooling
  - provider contracts

Mostorm-Labs/axdeps
  - dependency release assets
  - internal/private artifact publication
  - release lifecycle authority
```

## Rationale

AxBuild is public source infrastructure. Binary dependency release assets with `redistribution.status: review-required` must not be published through the public tooling repository.

`axdeps` becomes the release authority location for qualified dependency artifacts.

## C2 Preconditions

Before release publication:

- artifact qualification must PASS;
- artifact digest must be immutable;
- release index authority must point to axdeps;
- provenance must preserve redistribution status;
- publication eligibility must reference exact qualification evidence.

## C2 Scope

Included:

- publish qualified artifact to axdeps;
- generate immutable release metadata;
- validate AxBuild resolver consumption.

Excluded:

- NearCast consumer migration;
- changing current dependency restore path;
- external redistribution approval;
- product runtime changes.

## Next Step

Create the C2 P31 execution package against axdeps-backed release authority.
