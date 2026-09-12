# AXBUILD-NEARCAST-AIRPLAY-RELEASE-PUBLICATION-P30-v0.2

## Stage

- Owner: `aegis-implementation`
- Stage: `P30 Successor Planning`
- Successor of: `AXBUILD-NEARCAST-AIRPLAY-ARTIFACT-QUALIFICATION-P30-v0.1`

## Purpose

Promote a qualified AxBuild NearCast AirPlay artifact candidate into an immutable dependency release.

This slice starts only after artifact qualification has passed. It does not combine qualification, publication, and consumer migration.

## Previous Boundary

Completed:

```
NearCast dependency closure
        |
        v
AxBuild qualified artifact candidate
```

Current successor:

```
qualified artifact candidate
        |
        v
AxBuild dependency release
```

## Required Authority Decisions Before P31

### 1. Release Authority Location

A valid publication target must be selected:

- private dependency registry/repository, or
- explicitly approved public redistribution channel.

The executor must not infer this choice.

### 2. Visibility Contract

Release visibility must match redistribution policy.

Current qualification state remains:

```
redistribution.status = review-required
```

Therefore default assumption is not public redistribution.

### 3. Evidence Binding

Publication eligibility must reference exact:

- qualification result revision
- artifact digest
- validation results
- approval boundary

Floating references such as latest gate or latest CI run are invalid.

## Scope

Included after authority resolution:

- immutable release creation
- release index publication
- provenance publication
- release asset validation
- resolver consumption validation

Excluded:

- NearCast consumer migration
- replacing current dependency restore path
- external redistribution without approval
- modifying NearCast runtime

## Revised Lifecycle

```
C1 Artifact Qualification
        |
        v
P34 Gate
        |
        v
C2 Release Publication
        |
        v
Optional Consumer Migration
```

## Next Action

Do not enter P31 until release authority location and publication evidence boundary are explicitly frozen.
