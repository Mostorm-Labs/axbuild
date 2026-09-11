from __future__ import annotations

import json
from pathlib import Path
import zipfile

import pytest

from axbuild.archive import extract_zip_safe, file_sha256, verify_sha256
from axbuild.errors import ContractError, IntegrityError
from axbuild.qualification import (
    qualify_nearcast_airplay_artifact,
    load_artifact_manifest,
    load_qualification_report,
    load_provenance,
)


FILES = {
    "gstreamer/lib/pkgconfig/gstreamer-1.0.pc": "gstreamer",
    "gstreamer/bin/gst-inspect-1.0.exe": "inspect",
    "dnssd/Include/dns_sd.h": "dns",
    "bonjour/Bonjour64.msi": "bonjour",
    "webview2/build/native/include/WebView2.h": "webview",
    "vcpkg/installed/x64-windows/.axbuild-present": "vcpkg",
}


def write_archive(path: Path, *, reverse: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    items = list(FILES.items())
    if reverse:
        items.reverse()
    with zipfile.ZipFile(path, "w") as archive:
        for name, content in items:
            info = zipfile.ZipInfo(name)
            info.date_time = (2025, 1, 1, 0, 0, 0) if reverse else (2024, 1, 1, 0, 0, 0)
            archive.writestr(info, content)


def test_qualification_writes_manifest_provenance_and_report(tmp_path):
    source = tmp_path / "source.zip"
    write_archive(source)
    result = qualify_nearcast_airplay_artifact(source, tmp_path / "candidate")

    assert result.archive_path.name == "nearcast-airplay-runtime-windows-x64-release.zip"
    assert result.manifest_path.name == "nearcast-airplay-artifact-manifest.json"
    assert result.provenance_path.name == "nearcast-airplay-provenance.json"
    assert result.report_path.name == "qualification-report.json"
    manifest = load_artifact_manifest(result.manifest_path)
    provenance = load_provenance(result.provenance_path)
    report = load_qualification_report(result.report_path)
    assert manifest["family"] == "nearcast-airplay"
    assert manifest["target"] == "windows-x64"
    assert manifest["variant"] == "release"
    assert manifest["artifactIdentity"] == result.artifact_identity
    assert provenance["artifactIdentity"] == manifest["artifactIdentity"]
    assert provenance["sourceArchive"]["sha256"] == file_sha256(source)
    assert provenance["redistribution"]["status"] == "review-required"
    assert report["artifactIdentity"] == manifest["artifactIdentity"]
    assert all(item["status"] == "pass" for item in report["validationResults"].values())


def test_identity_is_stable_for_same_archive_inventory(tmp_path):
    first = tmp_path / "first.zip"
    second = tmp_path / "second.zip"
    write_archive(first)
    write_archive(second, reverse=True)
    one = qualify_nearcast_airplay_artifact(first, tmp_path / "one")
    two = qualify_nearcast_airplay_artifact(second, tmp_path / "two")
    assert one.artifact_identity == two.artifact_identity
    assert file_sha256(one.archive_path) == file_sha256(two.archive_path)


def test_identity_canonicalizes_file_inventory_order():
    entries = [
        {"path": "b.txt", "size": 1, "sha256": "b" * 64},
        {"path": "a.txt", "size": 1, "sha256": "a" * 64},
    ]
    from axbuild.qualification import artifact_identity

    assert artifact_identity(entries) == artifact_identity(list(reversed(entries)))


def test_manifest_files_match_candidate_archive(tmp_path):
    source = tmp_path / "source.zip"
    write_archive(source)
    result = qualify_nearcast_airplay_artifact(source, tmp_path / "candidate")
    manifest = load_artifact_manifest(result.manifest_path)
    with zipfile.ZipFile(result.archive_path) as archive:
        assert [item.filename for item in archive.infolist()] == [item["path"] for item in manifest["files"]]
        for item in manifest["files"]:
            assert file_sha256_from_zip(archive, item["path"]) == item["sha256"]


def file_sha256_from_zip(archive: zipfile.ZipFile, name: str) -> str:
    import hashlib

    return hashlib.sha256(archive.read(name)).hexdigest()


def test_archive_integrity_and_missing_closure_fail_closed(tmp_path):
    source = tmp_path / "source.zip"
    write_archive(source)
    result = qualify_nearcast_airplay_artifact(source, tmp_path / "candidate")
    verify_sha256(result.archive_path, result.archive_sha256)
    result.archive_path.write_bytes(b"tampered")
    with pytest.raises(IntegrityError):
        verify_sha256(result.archive_path, result.archive_sha256)

    incomplete = tmp_path / "incomplete.zip"
    with zipfile.ZipFile(incomplete, "w") as archive:
        archive.writestr("gstreamer/bin/gst-inspect-1.0.exe", "only one")
    with pytest.raises(IntegrityError, match="required"):
        qualify_nearcast_airplay_artifact(incomplete, tmp_path / "bad")


@pytest.mark.filterwarnings("ignore:Duplicate name:UserWarning")
def test_duplicate_archive_entries_fail_closed(tmp_path):
    source = tmp_path / "duplicate.zip"
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr("gstreamer/lib/pkgconfig/gstreamer-1.0.pc", "one")
        archive.writestr("gstreamer/lib/pkgconfig/gstreamer-1.0.pc", "two")
    with pytest.raises(IntegrityError, match="duplicate"):
        qualify_nearcast_airplay_artifact(source, tmp_path / "bad")


def test_extract_zip_accepts_windows_directory_entries(tmp_path):
    source = tmp_path / "windows-paths.zip"
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr("dnssd\\Lib\\", "")
        archive.writestr("dnssd\\Lib\\x64\\dnssd.lib", "library")

    destination = tmp_path / "extracted"
    extract_zip_safe(source, destination)

    assert (destination / "dnssd/Lib/x64/dnssd.lib").read_text(encoding="utf-8") == "library"


def test_manifest_rejects_unknown_fields(tmp_path):
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps({
        "format": "axbuild-nearcast-airplay-artifact-manifest-v1",
        "family": "nearcast-airplay",
        "target": "windows-x64",
        "variant": "release",
        "artifactIdentity": "candidate-1",
        "files": [{"path": "a.txt", "size": 1, "sha256": "a" * 64}],
        "unexpected": True,
    }), encoding="utf-8")
    with pytest.raises(ContractError, match="unknown"):
        load_artifact_manifest(path)


def test_qualification_schemas_are_valid_json():
    for name in (
        "nearcast-airplay-artifact-manifest-v1.schema.json",
        "nearcast-airplay-qualification-report-v1.schema.json",
    ):
        value = json.loads((Path("schemas") / name).read_text(encoding="utf-8"))
        assert value["type"] == "object"
