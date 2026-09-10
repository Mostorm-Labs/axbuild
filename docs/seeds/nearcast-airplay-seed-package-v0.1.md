# AxBuild NearCast AirPlay Seed Package v0.1

Status: P30 Implementation Planning

Owner: axbuild

## Purpose

Define the first AxBuild-owned dependency seed package for the NearCast AirPlay dependency closure.

This package is intentionally owned by AxBuild. NearCast remains an integration consumer and qualification source, not the release authority for shared dependency artifacts.

## Boundary

Included:

- define artifact identity
- define release index
- define provenance contract
- define lock format usage
- validate consumption through AxBuild resolver

Excluded:

- NearCast consumer migration
- replacement of existing dependency restore path
- external redistribution
- changing NearCast runtime behavior

## Ownership

```text
NearCast
  - integration qualification
  - provider implementation
  - runtime compatibility validation

AxBuild
  - release authority
  - artifact identity
  - release index
  - lock authority
  - resolver/store consumption
```

## Artifact Family

```yaml
family: nearcast-airplay
kind: runtime
target: windows-x64
variant: release
```

## Migration Strategy

Current path remains valid:

```
NearCast
  -> existing URL + SHA256 dependency restore
```

Future optional path:

```
NearCast
  -> AxBuild lock
  -> AxBuild resolver
  -> qualified artifact
```

Migration is a separate future slice.

## Next Steps

1. Create P31 task package.
2. Freeze execution closure contract.
3. Implement AxBuild-owned seed producer.
4. Validate clean-store and offline replay.
5. Do not migrate consumers until separately approved.
