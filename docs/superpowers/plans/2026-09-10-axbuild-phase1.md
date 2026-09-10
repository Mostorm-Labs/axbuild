# AxBuild Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify the Phase 1 AxBuild dependency-supply framework that resolves locked release artifacts into a persistent verified Store for both Axiom-like source SDKs and NearCast-like prebuilt dependency closures.

**Architecture:** The repository contains a small Python package under `src/axbuild`. Common modules model trusted release references, validate JSON contracts, transport exact release bytes, safely materialize archives into a content-addressed Store, and orchestrate explicit project-owned providers. Synthetic fixtures prove the same common resolver supports host-tool + target-runtime SDKs and monolithic prebuilt runtime closures without hard-coded project semantics.

**Tech Stack:** Python 3.11+, standard library only at runtime, pytest for tests, GitHub Actions for cross-platform validation.

**Spec:** `docs/superpowers/specs/2026-09-10-axbuild-phase1-design.md`

## Global Constraints

- Repository/product name is `AxBuild`; package namespace and CLI are `axbuild`.
- Source layout is `src/axbuild/`; do not introduce `awbuild` naming.
- Runtime code uses Python standard library only in Phase 1.
- Project/provider semantics stay outside common resolver/store/transport modules.
- Store, mirror, and cache are never dependency authority; lock + verified index determine identity.
- Invalid existing materialization is an integrity error, not a cache miss.
- Consumer resolution never silently source-builds a missing locked binary.
- Offline mode never uses network or mirror transport.
- Archive extraction rejects traversal/absolute/link entries.
- Tests are written first and observed failing before production code for each behavior.

---

## File Structure

- `pyproject.toml` — package metadata, `axbuild` console script, pytest configuration.
- `src/axbuild/__init__.py` — public version/export surface.
- `src/axbuild/errors.py` — typed AxBuild errors.
- `src/axbuild/model.py` — immutable references, requests, plans, materialized artifact records.
- `src/axbuild/contracts.py` — strict lock/index parsing and namespace/digest validation.
- `src/axbuild/archive.py` — SHA256 verification and safe ZIP extraction.
- `src/axbuild/store.py` — persistent Store paths, locking, materialization.
- `src/axbuild/transport.py` — file/HTTP(S)/GitHub Release byte acquisition.
- `src/axbuild/provider.py` — provider protocol and explicit registry.
- `src/axbuild/resolver.py` — family-neutral resolve orchestration and machine facts.
- `src/axbuild/cli.py` — validate/resolve entry points.
- `examples/providers/axiom_like.py` — synthetic host-tools + runtime provider.
- `examples/providers/nearcast_like.py` — synthetic prebuilt closure provider.
- `tests/fixtures/` — generated/small fixture archives and lock/index JSON created by tests.
- `tests/test_contracts.py` — lock/index validation tests.
- `tests/test_archive.py` — digest and traversal tests.
- `tests/test_store.py` — materialization/reuse/integrity tests.
- `tests/test_transport.py` — mirror/GitHub URL/auth/offline transport tests.
- `tests/test_resolver.py` — common resolver/provider orchestration tests.
- `tests/test_examples.py` — Axiom-like and NearCast-like end-to-end fixture tests.
- `.github/workflows/test.yml` — Linux/Windows/macOS test matrix.

---

### Task 1: Package skeleton and immutable model

**Files:**
- Create: `pyproject.toml`
- Create: `src/axbuild/__init__.py`
- Create: `src/axbuild/errors.py`
- Create: `src/axbuild/model.py`
- Test: `tests/test_model.py`

**Interfaces:**
- Produces: `ReleaseIndexRef`, `ArtifactRef`, `ResolveRequest`, `ProviderPlan`, `MaterializedArtifact` dataclasses and error hierarchy used by all later tasks.

- [ ] **Step 1: Write the failing model tests**

```python
from pathlib import Path
from axbuild.model import ArtifactRef, ResolveRequest


def test_artifact_ref_is_hashable_and_immutable():
    ref = ArtifactRef("demo", "runtime", "windows-x64", "id-1", "org/repo", "sdk-v1", "demo.zip", "a" * 64)
    assert {ref: "ok"}[ref] == "ok"


def test_resolve_request_normalizes_store_path(tmp_path: Path):
    request = ResolveRequest(repo_root=tmp_path, target="windows-x64", store_root=tmp_path / "store")
    assert request.store_root.is_absolute()
```

- [ ] **Step 2: Run tests and verify RED**

Run: `python -m pytest tests/test_model.py -q`
Expected: import failure because `axbuild` does not exist.

- [ ] **Step 3: Implement minimal package/model**

Implement frozen dataclasses and errors. `ResolveRequest` fields are `repo_root: Path`, `target: str`, `store_root: Path`, `mirror: str | None = None`, `offline: bool = False` and normalize paths in `__post_init__` via `object.__setattr__`.

- [ ] **Step 4: Run model tests and full suite**

Run: `python -m pytest tests/test_model.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml src/axbuild tests/test_model.py
git commit -m "feat: add AxBuild core model"
```

### Task 2: Strict lock and release-index contracts

**Files:**
- Create: `src/axbuild/contracts.py`
- Test: `tests/test_contracts.py`

**Interfaces:**
- Consumes: model dataclasses and `ContractError`.
- Produces: `load_sdk_lock(path: Path) -> ReleaseIndexRef`, `load_release_index(path: Path) -> ReleaseIndex`, `validate_namespace(value: str) -> str`, `validate_sha256(value: str) -> str`.

- [ ] **Step 1: Write failing contract tests**

```python
import json
import pytest
from axbuild.contracts import load_sdk_lock, validate_namespace
from axbuild.errors import ContractError


def test_lock_requires_exact_format(tmp_path):
    path = tmp_path / "demo.lock.json"
    path.write_text(json.dumps({"format": "wrong"}), encoding="utf-8")
    with pytest.raises(ContractError, match="format"):
        load_sdk_lock(path)


def test_namespace_rejects_traversal():
    with pytest.raises(ContractError):
        validate_namespace("../runtime")
```

Also test a valid lock and valid release index, duplicate `(kind,key)` rejection, family/releaseSet mismatch, malformed digest, unknown/missing required fields.

- [ ] **Step 2: Verify RED**

Run: `python -m pytest tests/test_contracts.py -q`
Expected: import failure for `axbuild.contracts`.

- [ ] **Step 3: Implement strict parsers**

Use explicit key/type checks rather than permissive dataclass unpacking. Normalize digests to lowercase. The parser may preserve arbitrary artifact `metadata` dictionaries but must reject non-object metadata.

- [ ] **Step 4: Verify GREEN**

Run: `python -m pytest tests/test_contracts.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/axbuild/contracts.py tests/test_contracts.py
git commit -m "feat: validate AxBuild release contracts"
```

### Task 3: Integrity verification and safe ZIP extraction

**Files:**
- Create: `src/axbuild/archive.py`
- Test: `tests/test_archive.py`

**Interfaces:**
- Produces: `file_sha256(path: Path) -> str`, `verify_sha256(path: Path, expected: str) -> None`, `extract_zip_safe(archive: Path, destination: Path) -> None`.

- [ ] **Step 1: Write failing archive tests**

```python
import zipfile
import pytest
from axbuild.archive import extract_zip_safe, verify_sha256
from axbuild.errors import IntegrityError


def test_verify_sha256_rejects_mismatch(tmp_path):
    path = tmp_path / "a.bin"
    path.write_bytes(b"payload")
    with pytest.raises(IntegrityError, match="SHA256"):
        verify_sha256(path, "0" * 64)


def test_zip_rejects_parent_traversal(tmp_path):
    archive = tmp_path / "bad.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr("../escape.txt", "bad")
    with pytest.raises(IntegrityError, match="unsafe"):
        extract_zip_safe(archive, tmp_path / "out")
```

Also test absolute paths and symlink entries are rejected, and a normal archive extracts successfully.

- [ ] **Step 2: Verify RED**

Run: `python -m pytest tests/test_archive.py -q`
Expected: import failure for `axbuild.archive`.

- [ ] **Step 3: Implement safe archive helpers**

Use `zipfile.ZipFile.infolist()`, reject absolute/POSIX/Windows-drive/traversal paths and Unix symlink mode entries before extracting anything. Resolve each destination and prove it remains under the requested root.

- [ ] **Step 4: Verify GREEN**

Run: `python -m pytest tests/test_archive.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/axbuild/archive.py tests/test_archive.py
git commit -m "feat: add verified safe archive handling"
```

### Task 4: Persistent content-addressed Store

**Files:**
- Create: `src/axbuild/store.py`
- Test: `tests/test_store.py`

**Interfaces:**
- Consumes: `ArtifactRef`, `ReleaseIndexRef`, archive verification, `IntegrityError`/`AxBuildError`.
- Produces: `SdkStore.archive_path`, `release_index_path`, `package_path`, `lock`, `materialize_package`.

- [ ] **Step 1: Write failing Store tests**

```python
from pathlib import Path
import zipfile
from axbuild.model import ArtifactRef
from axbuild.store import SdkStore


def test_store_paths_are_content_and_family_namespaced(tmp_path):
    ref = ArtifactRef("demo", "runtime", "win", "id-1", "org/repo", "v1", "demo.zip", "a" * 64)
    store = SdkStore(tmp_path)
    assert store.archive_path(ref) == tmp_path / "archives" / "sha256" / ("a" * 64) / "demo.zip"
    assert store.package_path(ref) == tmp_path / "packages" / "demo" / "runtime" / "id-1"
```

Add tests that valid installed package is reused, invalid installed package raises `IntegrityError` without invoking installer, and failed staging never replaces a valid destination.

- [ ] **Step 2: Verify RED**

Run: `python -m pytest tests/test_store.py -q`
Expected: import failure for `axbuild.store`.

- [ ] **Step 3: Implement Store**

Use cross-process file locking: `fcntl.flock` on POSIX and `msvcrt.locking` on Windows. Staging lives beside destination and publishes by rename only after provider validation. Never auto-repair a present invalid package in consumer flow.

- [ ] **Step 4: Verify GREEN**

Run: `python -m pytest tests/test_store.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/axbuild/store.py tests/test_store.py
git commit -m "feat: add persistent SDK store"
```

### Task 5: Verified release transport

**Files:**
- Create: `src/axbuild/transport.py`
- Test: `tests/test_transport.py`

**Interfaces:**
- Consumes: release/artifact refs and `verify_sha256`.
- Produces: `release_url(ref) -> str`, `ensure_release_file(ref, destination, mirror=None, offline=False) -> ReleaseFile`.

- [ ] **Step 1: Write failing transport tests**

```python
from axbuild.model import ArtifactRef
from axbuild.transport import release_url


def test_release_url_quotes_tag_and_asset():
    ref = ArtifactRef("demo", "runtime", "win", "id", "org/repo", "sdk v1", "a b.zip", "a" * 64)
    assert release_url(ref) == "https://github.com/org/repo/releases/download/sdk%20v1/a%20b.zip"
```

Add tests for local directory mirror copy + digest verification, offline miss, existing verified destination reuse, mirror corruption failure, and redirect policy helpers. Mock only `urllib` boundary for authenticated GitHub metadata/asset selection; assert credentials are not exposed in returned facts.

- [ ] **Step 2: Verify RED**

Run: `python -m pytest tests/test_transport.py -q`
Expected: import failure for `axbuild.transport`.

- [ ] **Step 3: Implement transport**

Support file-system mirrors and HTTP(S) mirrors. GitHub private assets resolve exact release metadata by tag and exact asset name when a token exists, then download the asset endpoint. Enforce a 2 GiB maximum download and safe redirect behavior modeled on the proven Axiom transport boundary.

- [ ] **Step 4: Verify GREEN**

Run: `python -m pytest tests/test_transport.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/axbuild/transport.py tests/test_transport.py
git commit -m "feat: add verified release transport"
```

### Task 6: Provider registry and family-neutral resolver

**Files:**
- Create: `src/axbuild/provider.py`
- Create: `src/axbuild/resolver.py`
- Test: `tests/test_resolver.py`

**Interfaces:**
- Consumes: contracts, Store, transport, provider protocol.
- Produces: `ProviderRegistry.register(provider)`, `ProviderRegistry.resolve(family, request) -> ResolutionResult`, `resolve_provider(provider, request) -> ResolutionResult`.

- [ ] **Step 1: Write failing resolver tests**

```python
import pytest
from axbuild.provider import ProviderRegistry
from axbuild.errors import AxBuildError


def test_registry_rejects_duplicate_family(fake_provider):
    registry = ProviderRegistry()
    registry.register(fake_provider)
    with pytest.raises(AxBuildError, match="already registered"):
        registry.register(fake_provider)
```

Add an in-test provider showing: verified index is fetched first; plan artifacts are family-consistent and unique; existing Store packages avoid transport; offline miss raises `OfflineError`; result facts report source/networkUsed but never credentials.

- [ ] **Step 2: Verify RED**

Run: `python -m pytest tests/test_resolver.py -q`
Expected: import failure for provider/resolver modules.

- [ ] **Step 3: Implement registry and resolver**

Resolver order is: provider index ref → verified index bytes → parsed index → provider plan → each artifact archive → materialize + validate → environment. No source-build fallback exists in consumer resolver.

- [ ] **Step 4: Verify GREEN**

Run: `python -m pytest tests/test_resolver.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/axbuild/provider.py src/axbuild/resolver.py tests/test_resolver.py
git commit -m "feat: resolve provider release artifacts"
```

### Task 7: Axiom-like and NearCast-like fixture providers

**Files:**
- Create: `examples/__init__.py`
- Create: `examples/providers/__init__.py`
- Create: `examples/providers/axiom_like.py`
- Create: `examples/providers/nearcast_like.py`
- Create: `tests/fixture_factory.py`
- Test: `tests/test_examples.py`

**Interfaces:**
- Axiom-like provider selects one `host-tools` artifact and one target `runtime` artifact.
- NearCast-like provider selects one prebuilt runtime closure and validates required fake paths such as `gstreamer/lib/pkgconfig/gstreamer-1.0.pc`, `gstreamer/bin/gst-inspect-1.0.exe`, `bonjour/Bonjour64.msi`, and `dnssd/Include/dns_sd.h`.

- [ ] **Step 1: Write failing end-to-end fixture tests**

```python
def test_axiom_like_second_resolution_is_store_only(axiom_fixture):
    first = axiom_fixture.resolve()
    second = axiom_fixture.resolve(offline=True)
    assert first.facts["networkUsed"] is False
    assert all(a["source"] == "store" for a in second.facts["artifacts"])


def test_nearcast_like_rejects_incomplete_prebuilt_closure(nearcast_fixture):
    nearcast_fixture.remove("dnssd/Include/dns_sd.h")
    with pytest.raises(IntegrityError):
        nearcast_fixture.resolve()
```

- [ ] **Step 2: Verify RED**

Run: `python -m pytest tests/test_examples.py -q`
Expected: import/fixture failures.

- [ ] **Step 3: Implement synthetic fixtures/providers**

Create tiny ZIPs during tests; do not commit or download real Skia/GStreamer/AirPlay binaries. Both providers must use the exact same common resolver/store/transport stack.

- [ ] **Step 4: Verify GREEN**

Run: `python -m pytest tests/test_examples.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add examples tests/fixture_factory.py tests/test_examples.py
git commit -m "test: prove Axiom and NearCast dependency shapes"
```

### Task 8: CLI and build-environment facts

**Files:**
- Create: `src/axbuild/cli.py`
- Create: `src/axbuild/__main__.py`
- Test: `tests/test_cli.py`

**Interfaces:**
- Produces commands: `axbuild validate-lock LOCK`, `axbuild validate-index INDEX`.
- Phase 1 common CLI does not dynamically import project providers from downloaded content.

- [ ] **Step 1: Write failing CLI tests**

```python
import subprocess, sys


def test_validate_lock_command(valid_lock_path):
    result = subprocess.run([sys.executable, "-m", "axbuild", "validate-lock", str(valid_lock_path)], text=True, capture_output=True)
    assert result.returncode == 0
    assert '"format":"axbuild-sdk-lock-v1"' in result.stdout.replace(" ", "")
```

Also assert malformed input returns non-zero and diagnostics go to stderr.

- [ ] **Step 2: Verify RED**

Run: `python -m pytest tests/test_cli.py -q`
Expected: command failure because `axbuild.__main__` is absent.

- [ ] **Step 3: Implement CLI**

Use `argparse`; stdout is machine-readable JSON, stderr is human diagnostics/errors. Keep provider execution as Python API in Phase 1 rather than unsafe dynamic plugin loading.

- [ ] **Step 4: Verify GREEN**

Run: `python -m pytest tests/test_cli.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/axbuild/cli.py src/axbuild/__main__.py tests/test_cli.py pyproject.toml
git commit -m "feat: add AxBuild contract CLI"
```

### Task 9: Cross-platform CI and consumer documentation

**Files:**
- Create: `.github/workflows/test.yml`
- Modify: `README.md`
- Test: full test suite plus package build/install smoke.

**Interfaces:**
- Produces a public repository validation workflow suitable for later reusable consumer workflow extraction.

- [ ] **Step 1: Add CI contract test first**

Add `tests/test_repository_contract.py` that parses `.github/workflows/test.yml` as text and asserts it contains `ubuntu-24.04`, `windows-2025`, `macos-15`, Python 3.11, install, and pytest steps.

- [ ] **Step 2: Verify RED**

Run: `python -m pytest tests/test_repository_contract.py -q`
Expected: FAIL because workflow file is absent.

- [ ] **Step 3: Add workflow and README integration guide**

Document future adapters:

```text
Axiom provider -> source-built SDK release index -> AxBuild resolver
NearCast provider -> prebuilt AirPlay/GStreamer closure index -> AxBuild resolver
Virtual AV provider -> media/common/native dependency families -> AxBuild resolver
```

Do not claim those repositories are migrated in Phase 1.

- [ ] **Step 4: Run final verification**

Run:

```bash
python -m pytest -q
python -m pip install -e .
axbuild --help
python -m build --wheel --no-isolation || true
```

The first three commands are blocking. The optional wheel build may be skipped if the `build` frontend is not installed; `pip install -e .` is the Phase 1 packaging requirement.

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/test.yml README.md tests/test_repository_contract.py
git commit -m "ci: validate AxBuild phase 1 across platforms"
```

### Task 10: Phase 1 integration verification

**Files:**
- Modify only if verification reveals a defect.

**Interfaces:**
- Produces the exact candidate branch ready for remote publication/review.

- [ ] **Step 1: Run clean full suite**

Run: `python -m pytest -q`
Expected: all tests PASS with no warnings caused by AxBuild code.

- [ ] **Step 2: Run repository hygiene checks**

Run:

```bash
git diff --check
git status --short
```

Expected: no whitespace errors; only intentional untracked/generated local files, ideally none.

- [ ] **Step 3: Inspect commit history**

Run: `git log --oneline --decorate -12`
Expected: small reviewable commits corresponding to Tasks 1-9.

- [ ] **Step 4: Record remote publication blocker**

Confirm whether `Mostorm-Labs/axbuild` exists and whether the connected GitHub tool exposes repository creation. If it still does not, do not fabricate publication; report the local candidate path and exact one-time remote creation requirement.
