from pathlib import Path

import pytest

from axbuild.errors import IntegrityError
from axbuild.model import ResolveRequest
from axbuild.provider import ProviderRegistry
from examples.providers.axiom_like import AxiomLikeProvider
from examples.providers.nearcast_like import NearCastLikeProvider
from tests.fixture_factory import create_axiom_like_fixture, create_nearcast_like_fixture


def test_axiom_like_provider_selects_host_tool_and_target_runtime(tmp_path):
    fixture = create_axiom_like_fixture(tmp_path)
    registry = ProviderRegistry()
    registry.register(AxiomLikeProvider(fixture.lock_path, host_key="linux-x86_64"))
    result = registry.resolve(
        "axiom-like",
        ResolveRequest(fixture.repo_root, "windows-x64-msvc-static", fixture.store_root, str(fixture.mirror_root)),
    )

    assert Path(result.environment["AXIOM_LIKE_HOST_ROOT"]).is_dir()
    assert Path(result.environment["AXIOM_LIKE_RUNTIME_ROOT"]).is_dir()
    assert [(a["kind"], a["key"]) for a in result.facts["artifacts"]] == [
        ("host-tools", "linux-x86_64"),
        ("runtime", "windows-x64-msvc-static"),
    ]


def test_axiom_like_second_resolution_is_store_only(tmp_path):
    fixture = create_axiom_like_fixture(tmp_path)
    registry = ProviderRegistry()
    registry.register(AxiomLikeProvider(fixture.lock_path, host_key="linux-x86_64"))
    online = ResolveRequest(fixture.repo_root, "windows-x64-msvc-static", fixture.store_root, str(fixture.mirror_root))
    registry.resolve("axiom-like", online)

    offline = ResolveRequest(fixture.repo_root, online.target, fixture.store_root, offline=True)
    second = registry.resolve("axiom-like", offline)

    assert second.facts["index"]["source"] == "store"
    assert all(item["source"] == "store" for item in second.facts["artifacts"])


def test_nearcast_like_provider_accepts_complete_prebuilt_closure(tmp_path):
    fixture = create_nearcast_like_fixture(tmp_path, complete=True)
    registry = ProviderRegistry()
    registry.register(NearCastLikeProvider(fixture.lock_path))

    result = registry.resolve(
        "nearcast-like",
        ResolveRequest(fixture.repo_root, "windows-x64", fixture.store_root, str(fixture.mirror_root)),
    )

    root = Path(result.environment["NEARCAST_LIKE_AIRPLAY_ROOT"])
    assert (root / "gstreamer/lib/pkgconfig/gstreamer-1.0.pc").is_file()
    assert (root / "dnssd/Include/dns_sd.h").is_file()
    assert result.facts["metadata"]["dependencyShape"] == "prebuilt-closure"


def test_nearcast_like_rejects_incomplete_prebuilt_closure(tmp_path):
    fixture = create_nearcast_like_fixture(tmp_path, complete=False)
    registry = ProviderRegistry()
    registry.register(NearCastLikeProvider(fixture.lock_path))

    with pytest.raises(IntegrityError, match="dnssd"):
        registry.resolve(
            "nearcast-like",
            ResolveRequest(fixture.repo_root, "windows-x64", fixture.store_root, str(fixture.mirror_root)),
        )
