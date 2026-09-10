# AxBuild Dependency Inventory & Seed Release v0.1

**Status:** Phase 1.5 architecture / release-supply decision record  
**Date:** 2026-09-10  
**AxBuild baseline:** `Mostorm-Labs/axbuild@5f2df2310fc3e1b6b324ac82889585a22fca5cc5`  
**Inventory baselines:** `Mostorm-Labs/axiom@196f71ff600b633d6f017a928bc0e8205004223c`, `Mostorm-Labs/NearCast@f57e1c66efe7e641ef1acada9df44581ce8e9f5f`

## 1. Purpose

Phase 1.5 converts real dependency supply already present in Axiom and NearCast into an explicit AxBuild migration inventory before producer/classifier automation is designed.

The goal is not to upload every dependency to GitHub Releases. The goal is to decide which dependency families are worth long-lived binary reuse, which existing qualified release sets should be adopted, which new seed release must be created, and which dependencies must remain upstream/toolchain/source managed.

This document is the input to Phase 2 producer, change-classifier, and reusable-workflow design.

## 2. Decision taxonomy

| Decision | Meaning |
| --- | --- |
| `ADOPT EXISTING RELEASE` | Qualified binary release content already exists. Preserve its identity/bytes and integrate it into AxBuild without rebuilding merely for migration. |
| `CREATE SEED RELEASE` | A stable reusable dependency closure exists in practice but lacks a canonical immutable release-set contract. Create its first AxBuild-qualified release set. |
| `KEEP AS-IS` | Current source/package/submodule mechanism is appropriate; binary release supply would add more complexity than value now. |
| `DO NOT REHOST` | External SDK/toolchain/vendor distribution should remain sourced from its official distribution mechanism. Pin/version/hash where appropriate, but do not make AxBuild the binary distributor. |
| `DEFER` | Potential future family, but evidence does not yet justify a release boundary. |

## 3. System boundary

AxBuild standardizes **dependency identity, verified acquisition, storage, materialization and facts**. It does not require all dependency bytes to live in `Mostorm-Labs/axbuild`.

```text
Mostorm-Labs/axbuild
  -> resolver / Store / transport / schemas / workflows

Mostorm-Labs/axiom/releases
  -> Axiom-owned qualified Skia and Semantic SDK release sets

Mostorm-Labs/NearCast/releases
  -> NearCast-owned dependency release sets, beginning with nearcast-airplay

future shared dependency registry (only if justified)
  -> cross-project families with real reuse and independent ownership
```

Project-specific binary payloads stay with their project owner by default. A shared binary registry such as `Mostorm-Labs/axdeps` is explicitly deferred until at least two projects need the same independently versioned family.

## 4. Axiom inventory

Axiom already has a mature split between source/toolchain authority (`deps.lock.json`) and qualified binary SDK locks (`semantic-sdk.lock.json`, `r1-full-skia-sdk.lock.json`). Phase 1.5 must preserve this separation.

| Dependency | Source / version | Owner | Current acquisition | Build cost | Artifact size | Targets | ABI sensitivity | Redistribution posture | Current release | Recommended family | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Skia SDK | `google/skia`, `chrome/m152`, commit `b6d106297ff9ef2ff8094033695d045e87775581` | Axiom | Qualified `r1-full` SDK lock/release | High | Large; per target/variant sizes are already recorded in lock metadata | Windows, Web, Apple, Android; release/debug/ASAN where defined | High | Preserve upstream notices/license obligations already carried by Axiom packaging; no new redistribution conclusion is introduced here | `skia-sdk-r1-full-v1-54c1999dc79d094d` | `skia` | `ADOPT EXISTING RELEASE` |
| Semantic SDK | Protobuf `36.0` + Abseil `20250512.1` producer inputs | Axiom | `semantic-sdk.lock.json` -> release index -> host-tools/runtime assets | High | Per-asset sizes recorded by existing release | Linux/Windows/macOS host tools; desktop/mobile/web runtimes as published | High | Existing Axiom-owned qualified release; preserve component license notices | `semantic-sdk-v2-14e3d492c9b7f970` | `semantic` | `ADOPT EXISTING RELEASE` |
| Protobuf source + protoc upstream assets | Protobuf `36.0` with source and protoc SHA256 pins | Semantic SDK producer | Explicit upstream URLs + SHA256 in `deps.lock.json` | Medium/High as runtime producer input | Upstream assets | Host tools + runtime producer matrix | High for generated/runtime compatibility | Upstream source/asset terms apply | Consumed into Semantic SDK release | `semantic` producer input | `KEEP AS-IS` |
| Abseil source | `20250512.1`, pinned source SHA256 | Semantic SDK producer | Upstream source tarball | Medium as producer input | Source tarball | Semantic runtime targets | High when linked into runtime | Upstream terms apply | Consumed into Semantic SDK release | `semantic` producer input | `KEEP AS-IS` |
| Emscripten / LLVM | emsdk `6.0.6`, LLVM `22.1.8` | Toolchain | Official emsdk/toolchain provisioning | Toolchain | N/A for AxBuild release inventory | Web | High | Toolchain distribution boundary | No AxBuild release required | none | `DO NOT REHOST` |
| Windows LLVM | LLVM `22.1.8`, official installer + pinned SHA256 | Toolchain | Official LLVM release asset | Toolchain | External installer | Windows | High | Keep official publisher as distributor | No AxBuild release required | none | `DO NOT REHOST` |
| Node.js | `24.18.0` LTS, platform archives + SHA256 | Toolchain/runtime tooling | Official Node archives | Low/Medium bootstrap | External archives | macOS arm64/x64, Linux x64, Windows x64 | Medium | Keep official publisher as distributor | No AxBuild release required | none | `DO NOT REHOST` |
| Android NDK | `27.2.12479018` / r27c / API 26 | Toolchain | Android SDK/NDK provisioning | Toolchain | N/A | Android | High | Android toolchain distribution boundary | No AxBuild release required | none | `DO NOT REHOST` |
| GoogleTest | `1.18.0`, pinned commit | Axiom test/build | Source dependency | Low | Small relative to SDK families | Build hosts | Low/Medium | Upstream source dependency | None needed | none | `KEEP AS-IS` |
| nlohmann_json | `3.12.0`, pinned commit | Axiom | Source dependency | Low | Small/header-oriented | Cross-platform | Low | Upstream source dependency | None needed | none | `KEEP AS-IS` |
| xxHash | `0.8.3`, pinned commit | Axiom | Source dependency | Low | Small | Cross-platform | Low/Medium | Upstream source dependency | None needed | none | `KEEP AS-IS` |
| Roboto / Noto Sans CJK subset | Skia resource fonts with pinned SHA256 | Axiom/Skia packaging | Source/resource input | Low | Small relative to SDK | Rendering targets | Low | Preserve font license notices | Embedded/input to SDK build | `skia` input | `KEEP AS-IS` |
| Web npm dependencies | React `19.2.8`, React DOM `19.2.8`, Vite `8.2.1`, TypeScript `7.0.2`, Playwright `1.62.1` | Axiom web/tooling | Package-manager install | Low/Medium | Package-manager managed | Web/build host | Medium | Keep package-manager/upstream distribution | None needed | none | `KEEP AS-IS` |

### 4.1 Axiom decision

Do **not** rebuild Skia or Semantic SDK merely to satisfy AxBuild naming. Their existing qualified release content is the valuable asset.

However, AxBuild Phase 1 currently accepts only `axbuild-sdk-lock-v1` and `axbuild-release-index-v1`, and its verified artifact authority requires artifacts to resolve under the repository/tag selected by the lock. Therefore `ADOPT EXISTING RELEASE` currently has a compatibility gap.

The migration rule is:

1. old Axiom release tags remain immutable;
2. do not attach new metadata to old tags as a migration shortcut;
3. do not duplicate large binaries solely to change metadata format;
4. Phase 2 must define a **generic immutable existing-release adoption mechanism** before Axiom migration;
5. that mechanism must remain family-neutral and must not hard-code Axiom/Skia/Semantic formats into AxBuild core.

Candidate mechanisms to evaluate in Phase 2 are an artifact-level immutable source locator in the AxBuild index, or a project-owned adapter that produces canonical AxBuild metadata before the common resolver boundary. The chosen mechanism must still pin repository, tag/asset identity and SHA256 and must not permit floating `latest` resolution.

## 5. NearCast inventory

NearCast currently has a different dependency shape. Windows CI caches `third_party/prebuilt/airplay`, restores it through `Restore-AirPlayDependencies.ps1`, and keys reuse by `NEARCAST_AIRPLAY_DEPS_SHA256`. The dependency URL and digest come from CI configuration rather than a checked-in release-set lock.

The current AirPlay closure validation expects GStreamer, a vcpkg x64-windows closure, DNS-SD headers, Bonjour, WebView2 headers, and the required GStreamer `aacparse` feature. NearCast also consumes first-party Axent and a UxPlay fork through git submodules.

| Dependency | Source / version | Owner | Current acquisition | Build/bootstrap cost | Artifact size | Targets | ABI sensitivity | Redistribution posture | Current release | Recommended family | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AirPlay dependency closure | GStreamer MSVC x86_64 + vcpkg closure + DNS-SD + Bonjour + WebView2 materialization | NearCast | CI variable URL + required SHA256 -> PowerShell restore -> `third_party/prebuilt/airplay` | High bootstrap weight; exact producer cost `MEASURE` | `MEASURE` from current archive | Windows x64 | High | **Redistribution review required before canonical seed publication**; component licenses/vendor terms differ | No checked-in canonical AxBuild release-set reference | `nearcast-airplay` | `CREATE SEED RELEASE` |
| GStreamer inside AirPlay closure | Official GStreamer MSVC x86_64 SDK; plugin set selected by runtime need | NearCast AirPlay | Included in current closure | High if repeatedly provisioned | `MEASURE` | Windows x64 now | High: plugins/runtime/CRT/toolchain matter | Core LGPL; plugin licenses vary; preserve notices and inventory selected plugins | Part of closure only | `nearcast-airplay` component | `CREATE SEED RELEASE` as closure component, not separate family in v0.1 |
| OpenSSL / libplist / vcpkg-resolved libraries | Versions currently determined by closure producer inputs | NearCast AirPlay | vcpkg/CMake-derived closure | Medium | `MEASURE` | Windows x64 | High for linked/runtime compatibility | Component licenses must be captured in manifest/notices | Part of closure only | `nearcast-airplay` component | `CREATE SEED RELEASE` as closure component |
| Bonjour / DNS-SD | Bonjour SDK / `Bonjour64.msi`; current restore validates installer version >= 3.0.0.0 | NearCast AirPlay | Included/provisioned by current closure | Medium bootstrap | `MEASURE` | Windows x64 | Medium | Apple Bonjour SDK/license terms require explicit redistribution check; if not permitted for chosen packaging, provision externally instead of embedding | Part of closure only | `nearcast-airplay` component | `CREATE SEED RELEASE` **only if redistribution gate passes** |
| WebView2 development dependency | WebView2 headers currently expected in closure | NearCast AirPlay | Included in current closure | Low/Medium | `MEASURE` | Windows x64 | Medium | Microsoft distribution terms apply; keep only what redistribution permits | Part of closure only | `nearcast-airplay` component | `CREATE SEED RELEASE` **only if redistribution gate passes** |
| UxPlay fork | Gitee `auditoryworks_hamedal/UxPlay`, branch `codex-develop`; exact commit pinned by gitlink in consuming tree | NearCast product source | Git submodule; CI falls back to `Mostorm-Labs/NearCast-UxPlay` mirror | Source build | Source tree | Windows AirPlay path | High at source/API boundary | GPLv3; repo notices also identify a mongoose GPL-2.0-only/commercial compatibility issue that must be resolved for distribution | Source dependency, not binary seed family | none | `KEEP AS-IS` |
| Axent | `Mostorm-Labs/Axent`, main branch, exact gitlink pinned by consuming tree | First-party Axent | Git submodule | Source build | Source tree | NearCast supported hosts | High at internal API/ABI boundary | First-party ownership; transitive licenses remain Axent-owned | No seed release required now | none | `KEEP AS-IS` |
| AXTP runtime / hidapi / IXWebSocket under Axent | Versions owned by Axent integration | Axent | Transitive source dependency | Low/Medium relative to media closure | Source/build outputs | NearCast supported hosts | Medium/High | Keep dependency ownership with Axent | No independent NearCast seed release | none | `KEEP AS-IS` |
| MSVC / Windows SDK | Runner/toolchain provisioned | Toolchain | GitHub runner / developer environment | Toolchain | N/A | Windows | High | Vendor SDK/toolchain boundary | No AxBuild release | none | `DO NOT REHOST` |
| Microsoft VC++ Redistributable | Current NearCast notices record bundled `14.44.35211.0` for product runtime | Product packaging | Official Microsoft redistributable, packaged separately | Low bootstrap | External installer | Windows x64 | High runtime compatibility | Microsoft redistribution terms apply; product runtime packaging is distinct from AxBuild build-dependency supply | Product package concern | none | `DO NOT REHOST` as AxBuild dependency |

### 5.1 NearCast seed-release decision

The first genuinely new seed release should be **one monolithic `nearcast-airplay` family for Windows x64**, matching the already-working closure boundary.

Do not split GStreamer, Bonjour, OpenSSL, libplist or WebView2 into independent AxBuild families in v0.1. Splitting is justified only when an independent upgrade cadence, independent consumer, or measurable reuse benefit appears.

Initial target shape:

```text
family: nearcast-airplay
kind: runtime
key: windows-x64-release
target: windows-x64
variant: release
owner repository: Mostorm-Labs/NearCast
```

Proposed release layout after redistribution qualification:

```text
tag: nearcast-airplay-sdk-v1-<releaseSetId-prefix>

assets:
  nearcast-airplay-windows-x64-release-<artifactIdentity>.zip
  nearcast-airplay-index.json
  nearcast-airplay-third-party-notices.txt   # or notices embedded in package + manifest reference
```

NearCast then checks in an AxBuild lock such as:

```json
{
  "format": "axbuild-sdk-lock-v1",
  "family": "nearcast-airplay",
  "repository": "Mostorm-Labs/NearCast",
  "releaseTag": "nearcast-airplay-sdk-v1-<releaseSetId-prefix>",
  "releaseSetId": "<releaseSetId>",
  "indexAsset": "nearcast-airplay-index.json",
  "indexSha256": "<sha256>"
}
```

The existing CI variables `NEARCAST_AIRPLAY_DEPS_URL` and `NEARCAST_AIRPLAY_DEPS_SHA256` then become migration inputs, not long-term dependency authority.

## 6. Seed-release qualification gates

A new release set is not qualified merely because a ZIP can be downloaded. Before `nearcast-airplay` is published as the canonical seed release, all of the following must be evidenced:

1. **Provenance** — record exact source/version/origin for every included component.
2. **Redistribution** — review GStreamer plugin licenses and vendor terms for Bonjour/WebView2/other bundled vendor files. If a component cannot be redistributed in the selected form, exclude it and provision it through its official mechanism.
3. **Manifest** — package contains or is accompanied by a machine-readable component manifest and preserved notices.
4. **Artifact identity** — identity derives from dependency sources, build/profile inputs, target/variant, ABI/toolchain contract and package-contract version; it is not simply the NearCast repository commit.
5. **SHA256** — index and every release asset have immutable digests.
6. **Layout validation** — current functional checks survive migration, including GStreamer discovery/scanner/plugin layout and required features such as `aacparse`.
7. **Clean-Store consumer test** — AxBuild resolves the lock from an empty Store, materializes the package, configures NearCast and completes the relevant Windows build/test path.
8. **Offline consumer test** — after Store population, the same consumer succeeds with AxBuild offline mode and no release/mirror network access.
9. **No hidden source fallback** — missing locked bytes cause a fail-closed consumer error rather than an implicit dependency rebuild.

## 7. Do-not-rehost boundary

Phase 1.5 explicitly rejects turning AxBuild into a general mirror for vendor toolchains.

Do not create AxBuild-managed binary releases for:

- Windows SDK / WDK;
- MSVC toolchain;
- Xcode / macOS / iOS SDKs;
- Android NDK;
- Emscripten SDK / LLVM toolchain distribution;
- Node.js official runtime archives merely for convenience;
- Microsoft VC++ Redistributable as a build-dependency family.

These may be version-pinned, hash-verified, provisioned by official installers/package managers, or cached ephemerally, but their official publisher remains the distribution authority.

## 8. Measurements still required

The inventory intentionally does not invent measurements that are not present in repository authority.

Before producer optimization targets are frozen, measure:

| Measurement | Why |
| --- | --- |
| Current NearCast AirPlay archive byte size | Establish release/storage/download budget |
| NearCast dependency bootstrap p50/p95 | Quantify value of Store/Release reuse |
| NearCast clean-run vs Store-hit build time | Demonstrate actual CI savings |
| GStreamer/plugin component inventory and versions | Provenance + redistribution + reproducibility |
| vcpkg closure package/version set | ABI/provenance identity |
| Existing Axiom Skia/Semantic Store-hit and release-fetch timing | Baseline migration without rebuilding |
| Release/mirror failure behavior | Verify fail-closed and recovery paths |

These are `MEASURE` inputs to P18/Phase 2 engineering decisions, not blockers to completing the inventory itself except where a qualification gate explicitly requires them.

## 9. Phase 1.5 execution order

```text
A. Preserve/adopt Axiom existing qualified release content
   -> identify generic AxBuild compatibility gap
   -> no source rebuild, no mutation of historical tags

B. Capture NearCast current AirPlay closure provenance
   -> archive digest + byte size
   -> exact GStreamer/plugin/vcpkg/vendor component inventory
   -> redistribution review

C. Produce NearCast nearcast-airplay seed candidate
   -> package + manifest + notices
   -> axbuild-release-index-v1
   -> qualification tests

D. Publish immutable NearCast seed release
   -> new release tag / releaseSetId
   -> exact assets + SHA256
   -> promote checked-in axbuild-sdk-lock-v1 only after qualification

E. Prove real AxBuild consumers
   -> clean Store
   -> Store hit
   -> offline
   -> corrupt/missing artifact failure

F. Only then design Phase 2 producer/classifier/reusable workflow
```

## 10. Frozen invariants for the next phase

1. A Release asset is **not authority by itself**; checked-in lock + verified release index select the exact release set.
2. No consumer resolves floating `latest`.
3. Published qualified release-set identity is immutable. Historical release tags are not edited to retrofit AxBuild metadata.
4. Every AxBuild-managed artifact is digest-verified before materialization.
5. Store, cache and mirror may provide bytes but may not choose another dependency identity.
6. Project-specific dependency assets remain in the project owner's release namespace by default.
7. Vendor SDK/toolchain binaries are not rehosted by default.
8. Ordinary consumer resolution never silently falls back to source-building a missing locked binary.
9. Provider/project semantics remain outside family-neutral AxBuild resolver/Store/transport code.
10. Family splitting requires evidence of independent ownership, upgrade cadence, consumer reuse or measurable supply-chain benefit.

## 11. Phase 1.5 outcome

The immediate release actions are therefore:

- **Axiom Skia:** `ADOPT EXISTING RELEASE`; no rebuild.
- **Axiom Semantic SDK:** `ADOPT EXISTING RELEASE`; no rebuild.
- **NearCast AirPlay/GStreamer closure:** `CREATE SEED RELEASE`, gated by provenance and redistribution qualification.
- **Toolchains/vendor SDKs:** `DO NOT REHOST`.
- **Small/source/product dependencies:** `KEEP AS-IS` unless later measurements justify promotion into a binary family.

Phase 2 must be designed against these real families, not against hypothetical dependency examples.