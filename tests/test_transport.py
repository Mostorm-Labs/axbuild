from pathlib import Path

import pytest

from axbuild.archive import file_sha256
from axbuild.errors import IntegrityError, OfflineError, TransportError
from axbuild.model import ArtifactRef
from axbuild.transport import ensure_release_file, redirect_is_safe, release_url


def make_ref(payload: bytes = b"payload"):
    import hashlib

    return ArtifactRef(
        family="demo",
        kind="runtime",
        key="windows-x64",
        identity="runtime-1",
        repository="org/repo",
        release_tag="sdk v1",
        asset="a b.zip",
        sha256=hashlib.sha256(payload).hexdigest(),
    )


def test_release_url_quotes_tag_and_asset():
    ref = make_ref()
    assert release_url(ref) == "https://github.com/org/repo/releases/download/sdk%20v1/a%20b.zip"


def test_file_mirror_copies_and_verifies_exact_asset(tmp_path):
    payload = b"fixture bytes"
    ref = make_ref(payload)
    mirror = tmp_path / "mirror"
    source = mirror / ref.release_tag / ref.asset
    source.parent.mkdir(parents=True)
    source.write_bytes(payload)
    destination = tmp_path / "store" / ref.asset

    result = ensure_release_file(ref, destination, mirror=str(mirror))

    assert result.path == destination
    assert result.source == "mirror"
    assert result.network_used is False
    assert destination.read_bytes() == payload
    assert file_sha256(destination) == ref.sha256


def test_existing_verified_destination_is_reused(tmp_path):
    payload = b"fixture bytes"
    ref = make_ref(payload)
    destination = tmp_path / ref.asset
    destination.write_bytes(payload)

    result = ensure_release_file(ref, destination, offline=True)

    assert result.source == "store"
    assert result.network_used is False


def test_offline_missing_destination_fails_without_transport(tmp_path):
    ref = make_ref()
    with pytest.raises(OfflineError, match="offline"):
        ensure_release_file(ref, tmp_path / ref.asset, mirror=str(tmp_path / "mirror"), offline=True)


def test_corrupt_mirror_is_integrity_failure_not_fallback(tmp_path):
    ref = make_ref(b"expected")
    mirror = tmp_path / "mirror"
    source = mirror / ref.release_tag / ref.asset
    source.parent.mkdir(parents=True)
    source.write_bytes(b"corrupt")

    with pytest.raises(IntegrityError, match="SHA256"):
        ensure_release_file(ref, tmp_path / "out" / ref.asset, mirror=str(mirror))


def test_missing_file_mirror_reports_clean_miss_when_github_fails(tmp_path, monkeypatch):
    ref = make_ref()

    def fail_github(ref, destination):
        raise TransportError("github unavailable")

    monkeypatch.setattr("axbuild.transport._github_download", fail_github)
    with pytest.raises(TransportError, match="github unavailable"):
        ensure_release_file(ref, tmp_path / "out" / ref.asset, mirror=str(tmp_path / "mirror"))


def test_redirect_policy_blocks_https_downgrade_and_allows_https_cross_origin():
    assert redirect_is_safe("https://github.com/a", "https://objects.githubusercontent.com/b") is True
    assert redirect_is_safe("https://github.com/a", "http://example.com/b") is False
    assert redirect_is_safe("http://example.com/a", "https://example.com/b") is True
    assert redirect_is_safe("https://github.com/a", "file:///tmp/a") is False
