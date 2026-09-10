# AxBuild Phase 1 Design

## Status

Approved design baseline for Phase 1 implementation.

## Goal

Build a reusable dependency-supply framework for Mostorm-Labs projects that avoids rebuilding stable, expensive third-party repositories on ordinary CI runs while preserving reproducibility, integrity, offline recovery, and project-specific flexibility.

## Reference implementations

Phase 1 intentionally learns from two different dependency shapes:

1. **Axiom**: source-built SDK release sets such as Skia and Semantic SDK, with target/variant/toolchain identities, verified release indexes, provider-driven resolution, and a persistent content-addressed store.
2. **NearCast**: prebuilt dependency closure for Windows AirPlay integration, currently restoring GStreamer plus supporting dependencies from a versioned archive with SHA256 validation and runtime layout checks.

AxBuild must model both without hard-coding Axiom, Skia, NearCast, GStreamer, AirPlay, Protobuf, or UxPlay semantics into the common layer.

## Repository and naming

- Repository: `Mostorm-Labs/axbuild`.
- Intended visibility: public.
- Product-specific or proprietary dependency assets may remain in private project repositories or private release registries.
- Python package namespace: `axbuild`.
- Source layout: `src/axbuild/`.
- Public command: `axbuild`.
- Do not introduce the previous `awbuild` name.

## Phase 1 scope

Phase 1 implements:

- immutable identity models for release sets and artifacts;
- strict JSON lock and release-index parsing;
- SHA256 verification;
- verified transport from local mirror, HTTP(S) mirror, and GitHub Release Assets;
- GitHub private release support using `GITHUB_TOKEN` or `GH_TOKEN` without persisting credentials;
- persistent content-addressed archive and materialized-package store;
- lock-safe materialization with staging and validation before publication;
- explicit offline mode;
- project-owned provider protocol;
- provider registry and family-neutral resolver;
- machine-readable resolution facts;
- two fixture providers demonstrating Axiom-like source-SDK and NearCast-like prebuilt-bundle consumption;
- reusable consumer CI validation across Linux, Windows, and macOS;
- contract tests for security/integrity boundaries.

Phase 1 does **not** migrate Axiom or NearCast, publish real GStreamer/Skia packages, implement a general producer matrix, or implement an update bot.

## Architecture

```text
Project SDK lock
      |
      v
Provider Registry
      |
      v
Family-neutral Resolver
      |
      +---- verified release index
      |
      +---- artifact selection
      |
      v
Transport ------------------- optional mirror
      |                              |
      +--------- GitHub Release -----+
      |
      v
Content-addressed Store
      |
      v
Provider install + validate
      |
      v
Resolved environment + facts
```

### Authority rule

The repository lock determines the requested release-set identity and digest. Store contents, mirrors, network endpoints, and caches never become dependency authority and cannot change the identity or digest being resolved.

## Data model

### SDK lock

A lock contains:

- `format`: `axbuild-sdk-lock-v1`;
- `family`;
- `repository` in `owner/repo` form;
- `releaseTag`;
- `releaseSetId`;
- `indexAsset`;
- `indexSha256`.

### Release index

A release index contains:

- `format`: `axbuild-release-index-v1`;
- `family`;
- `releaseSetId`;
- `artifacts`: array of artifact records.

Each artifact record contains:

- `kind`;
- `key`;
- `identity`;
- `asset`;
- `sha256`;
- optional `size`;
- `metadata` object for ABI/toolchain/capability facts.

Identity strings are opaque to the common resolver. Project providers define which artifacts are needed and what metadata they require.

## Provider contract

A provider is repository-trusted Python code registered explicitly by the consumer. It owns family semantics and exposes:

```python
class Provider(Protocol):
    family: str
    def index_ref(self, request: ResolveRequest) -> ReleaseIndexRef: ...
    def plan(self, request: ResolveRequest, index: ReleaseIndex) -> ProviderPlan: ...
    def install(self, ref: ArtifactRef, archive: Path, staging_root: Path) -> None: ...
    def validate(self, ref: ArtifactRef, materialized_root: Path) -> None: ...
    def environment(self, plan: ProviderPlan, materialized: tuple[MaterializedArtifact, ...]) -> dict[str, str]: ...
```

Downloaded code must never be treated as a provider plugin.

## Store layout

```text
<store>/
  archives/sha256/<digest>/<asset>
  release-sets/<family>/<releaseSetId>/<indexAsset>
  packages/<family>/<kind>/<identity>/
  locks/<digest>.lock
```

Materialized packages are validated before reuse. A present but invalid package is an integrity failure, not a cache miss.

## Transport behavior

Resolution order:

1. verified local Store;
2. configured mirror;
3. GitHub Release Asset from the exact repository/tag/asset encoded by the trusted reference.

Offline mode permits only already materialized and valid Store content.

Redirects may not downgrade HTTPS to HTTP. Authorization and cookies must be stripped on cross-origin redirects. Downloaded bytes must verify against SHA256 before publication into the Store.

## Fixture reference cases

### Axiom-like fixture

Demonstrates a release index with separate `host-tools` and `runtime` artifacts, where the provider selects one host tool and one target runtime and emits environment variables for both.

### NearCast-like fixture

Demonstrates one prebuilt `runtime` closure containing a fake GStreamer-style layout plus supporting directories. Its provider validates required files/features in the extracted package before materialization succeeds.

The fixture is intentionally synthetic: no third-party binary is copied into AxBuild.

## CI

Phase 1 CI runs package/unit/contract tests on:

- Ubuntu;
- Windows;
- macOS.

Tests must use local fixture assets and a local file mirror where possible. Network-dependent GitHub transport logic is unit-tested around URL/auth/integrity behavior rather than requiring publication of real release assets.

## Security and failure behavior

- malformed lock/index data fails closed;
- path namespace components reject separators, traversal, and empty values;
- SHA256 is always lowercase 64-hex internally;
- archive extraction rejects absolute paths and traversal entries;
- package publication uses staging then atomic rename where supported;
- invalid existing materialization is reported, not silently replaced;
- offline miss raises a distinct offline error;
- credentials are never written to resolution facts;
- provider registration is explicit and duplicate families are rejected.

## Phase 1 completion criteria

Phase 1 is complete when:

1. `pip install -e .` exposes an `axbuild` command;
2. all unit tests pass on the current environment;
3. resolver can consume both Axiom-like and NearCast-like local fixture releases without project-specific code in the common modules;
4. a second resolution uses the persistent Store and does not re-fetch fixture bytes;
5. offline resolution succeeds after materialization and fails clearly before materialization;
6. integrity mismatch and unsafe archive paths fail closed;
7. CI matrix definition covers Ubuntu, Windows, and macOS;
8. README documents how future Axiom/NearCast adapters will integrate without claiming they are already migrated.
