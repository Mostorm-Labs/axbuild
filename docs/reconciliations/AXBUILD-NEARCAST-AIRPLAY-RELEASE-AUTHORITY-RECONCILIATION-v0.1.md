# AXBUILD NearCast AirPlay Release Authority Reconciliation v0.1

Status: P31 RECONCILIATION REQUIRED

## Reason

The previous release publication package reached P32 but correctly failed closed because the publication authority boundary was not executable.

## Findings

- AxBuild repository visibility is public.
- Previous package required an internal/private release boundary.
- Previous package did not bind release publication to a private artifact authority.
- Previous package depended on gate state without a durable Gate/Evidence reference.
- Publication input artifact references were not materialized as immutable qualified inputs.

## Required Corrections

Before reopening P31:

1. Define the release artifact authority location.
2. Separate artifact qualification from release publication.
3. Bind publication eligibility to exact Gate/Evidence references.
4. Provide immutable artifact inputs with digest.

## Revised Slices

### Slice C1 — Artifact Qualification

Owner: AxBuild

Output:

- qualified runtime archive
- artifact manifest
- provenance
- SHA256 digest

No release publication.

### Slice C2 — Release Publication

Depends on C1.

Output:

- immutable release
- release index
- SDK lock

No consumer migration.

## Non-goals

- NearCast consumer migration
- external redistribution
- replacing current dependency restore path
