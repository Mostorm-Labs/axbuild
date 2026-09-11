# AxBuild

AxBuild is a reusable dependency-supply framework for Mostorm-Labs projects. It is designed for repositories whose ordinary CI should consume already-qualified dependency artifacts instead of repeatedly rebuilding large third-party source trees.

Phase 1 provides a family-neutral resolver, strict lock/index contracts, SHA256-verified transport, a persistent content-addressed Store, explicit project-owned providers, offline operation, and synthetic integration examples for two real dependency shapes already used inside Mostorm-Labs.

## Reference implementations

AxBuild is intentionally informed by two different existing patterns:

- **Axiom-like source SDKs**: expensive source-built SDKs with separate host tools and target runtimes, target/ABI/toolchain identities, release indexes, and long-lived binary reuse.
- **NearCast-like prebuilt closures**: a prebuilt runtime bundle such as the current Windows AirPlay dependency closure containing GStreamer and supporting dependencies, restored by exact asset identity plus SHA256 and validated for required runtime layout.

The examples in this repository are synthetic. AxBuild does not contain or redistribute Skia, GStreamer, AirPlay, UxPlay, Bonjour, WebView2, or other third-party binaries.

## NearCast AirPlay artifact qualification

An explicit local NearCast AirPlay closure archive can be qualified into a
release-ready candidate without publishing it:

```bash
axbuild qualify-nearcast-airplay-artifact path/to/closure.zip path/to/candidate
```

The command emits the deterministic runtime archive, artifact manifest,
provenance metadata, and qualification report. Identity is based on the
canonical archive file inventory, target/variant, package contract, and
ABI/toolchain inputs. Provenance always records `redistribution.status` as
`review-required`; this tooling does not create a GitHub Release, release tag,
consumer lock, or redistribution approval.

The executable contract is implemented by `axbuild.qualification` and the
machine-readable manifest/report contracts are under `schemas/`.

## Core model

```text
Project SDK lock
      |
      v
Project-owned Provider
      |
      v
Family-neutral Resolver
      |
      +---- verified Release Index
      |
      +---- selected Artifact Refs
      |
      v
Verified Transport ---- optional mirror
      |                       |
      +---- GitHub Release ---+
      |
      v
Content-addressed Store
      |
      v
Provider install + validate
      |
      v
Environment + machine-readable facts
```

The repository lock and its verified release index are dependency authority. The Store, mirror, GitHub transport, and CI caches may provide bytes but never choose a different release identity.

## Install for development

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
axbuild --help
```

AxBuild requires Python 3.11 or newer. Runtime modules use only the Python standard library in Phase 1.

## CLI

Validate a repository SDK lock:

```bash
axbuild validate-lock path/to/family-sdk.lock.json
```

Validate a release index:

```bash
axbuild validate-index path/to/family-index.json
```

Successful commands write compact machine-readable JSON to stdout. Contract failures use stderr and a non-zero exit code.

## SDK lock

A project checks in a small lock that identifies an exact qualified release set:

```json
{
  "format": "axbuild-sdk-lock-v1",
  "family": "media-common",
  "repository": "Mostorm-Labs/example-project",
  "releaseTag": "media-common-sdk-v4",
  "releaseSetId": "media-common-set-4",
  "indexAsset": "media-common-index.json",
  "indexSha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
}
```

The consumer never resolves a floating `latest` release.

## Provider boundary

Common AxBuild code does not know what a dependency means. A project registers trusted provider code that selects artifacts from a verified index and defines package-specific installation, validation, and exported build environment.

```python
class Provider:
    family: str

    def index_ref(self, request): ...
    def plan(self, request, index): ...
    def install(self, ref, archive, staging_root): ...
    def validate(self, ref, materialized_root): ...
    def environment(self, plan, materialized): ...
```

Provider code must come from the consuming repository or another explicitly trusted code dependency. AxBuild never downloads executable provider plugins from a release.

## Persistent Store

The default application-level location will be selected by integrating projects in a later phase. The Phase 1 API accepts an explicit Store root and uses this layout:

```text
store/
  archives/sha256/<digest>/<asset>
  release-sets/<family>/<releaseSetId>/<indexAsset>
  packages/<family>/<kind>/<identity>/
  locks/<digest>.lock
```

A package already present in `packages/` must still pass provider validation. If it fails validation, AxBuild reports an integrity failure instead of silently deleting or replacing it.

## Mirror and offline behavior

`ResolveRequest` supports an optional mirror and an offline flag. A mirror may be a local directory, `file://` URL, or HTTP(S) base URL with the same `<releaseTag>/<asset>` layout as the upstream release source.

Resolution order for missing bytes is:

```text
verified Store
    -> configured mirror
    -> exact GitHub Release asset
```

Offline mode permits only already materialized and valid Store content. Consumer resolution does not fall back to rebuilding source.

## Private release assets

For private GitHub repositories, transport can use `GH_TOKEN` or `GITHUB_TOKEN`. The token is used only for GitHub API requests and is not stored in locks, Store paths, or resolution facts. Cross-origin redirects strip authorization and cookies.

## Examples

`examples/providers/axiom_like.py` demonstrates a provider selecting one host-tool artifact and one target-runtime artifact from the same release set.

`examples/providers/nearcast_like.py` demonstrates a provider selecting one prebuilt Windows runtime closure and validating a synthetic GStreamer/AirPlay-style directory shape.

These examples prove dependency shapes, not project migrations.

## Planned project integrations

Future project work can adopt AxBuild incrementally:

```text
Axiom
  current source-built SDK release sets
        -> Axiom provider
        -> AxBuild resolver/store/transport

NearCast
  current AirPlay/GStreamer dependency archive
        -> NearCast provider
        -> AxBuild resolver/store/transport

Virtual Audio/Video Companion
  future media/common/native dependency families
        -> project providers
        -> AxBuild resolver/store/transport
```

Phase 1 deliberately does not modify Axiom or NearCast. Producer matrix abstraction, change classification, reusable producer workflows, and migration of existing projects are Phase 2 work.

## Contracts

Machine-readable v1 schema documents are published under `schemas/`:

- `sdk-lock-v1.schema.json`
- `release-index-v1.schema.json`
- `artifact-manifest-v1.schema.json`

The Python parser is the Phase 1 executable contract and fails closed on unknown top-level fields, unsafe namespace values, malformed digests, duplicate artifact keys, and inconsistent release authority.

## CI

`.github/workflows/test.yml` runs the complete test suite on Ubuntu 24.04, Windows 2025, and macOS 15 using Python 3.11, then checks the installed `axbuild` CLI.

## Repository status

This repository currently contains the Phase 1 framework candidate. It is not yet an authority replacement for dependency logic in Axiom or NearCast until each project completes an explicit migration and verification cycle.
