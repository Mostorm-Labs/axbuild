import stat
import zipfile

import pytest

from axbuild.archive import extract_zip_safe, file_sha256, verify_sha256
from axbuild.errors import IntegrityError


def test_verify_sha256_rejects_mismatch(tmp_path):
    path = tmp_path / "a.bin"
    path.write_bytes(b"payload")
    with pytest.raises(IntegrityError, match="SHA256"):
        verify_sha256(path, "0" * 64)


def test_file_sha256_is_stable(tmp_path):
    path = tmp_path / "a.bin"
    path.write_bytes(b"payload")
    assert file_sha256(path) == "239f59ed55e737c77147cf55ad0c1b030b6d7ee748a7426952f9b852d5a935e5"


def test_zip_rejects_parent_traversal(tmp_path):
    archive = tmp_path / "bad.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr("../escape.txt", "bad")
    with pytest.raises(IntegrityError, match="unsafe"):
        extract_zip_safe(archive, tmp_path / "out")
    assert not (tmp_path / "escape.txt").exists()


def test_zip_rejects_absolute_and_drive_paths(tmp_path):
    for name in ("/absolute.txt", "C:/drive.txt"):
        archive = tmp_path / (name.replace("/", "_").replace(":", "_") + ".zip")
        with zipfile.ZipFile(archive, "w") as zf:
            zf.writestr(name, "bad")
        with pytest.raises(IntegrityError, match="unsafe"):
            extract_zip_safe(archive, tmp_path / "out")


def test_zip_rejects_symlink_entries(tmp_path):
    archive = tmp_path / "link.zip"
    info = zipfile.ZipInfo("link")
    info.create_system = 3
    info.external_attr = (stat.S_IFLNK | 0o777) << 16
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr(info, "target")
    with pytest.raises(IntegrityError, match="symlink"):
        extract_zip_safe(archive, tmp_path / "out")


def test_zip_extracts_normal_tree(tmp_path):
    archive = tmp_path / "ok.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr("sdk/include/a.h", "header")
        zf.writestr("sdk/lib/a.lib", "library")
    destination = tmp_path / "out"
    extract_zip_safe(archive, destination)
    assert (destination / "sdk/include/a.h").read_text() == "header"
    assert (destination / "sdk/lib/a.lib").read_text() == "library"
