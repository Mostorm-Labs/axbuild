import json

import pytest

from axbuild.contracts import load_release_index, load_sdk_lock, validate_namespace, validate_sha256
from axbuild.errors import ContractError


def write_json(tmp_path, name, value):
    path = tmp_path / name
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def valid_lock():
    return {
        "format": "axbuild-sdk-lock-v1",
        "family": "semantic",
        "repository": "Mostorm-Labs/axiom",
        "releaseTag": "semantic-sdk-v2-abc",
        "releaseSetId": "set-abc",
        "indexAsset": "semantic-sdk-index.json",
        "indexSha256": "A" * 64,
    }


def valid_index():
    return {
        "format": "axbuild-release-index-v1",
        "family": "semantic",
        "releaseSetId": "set-abc",
        "artifacts": [
            {
                "kind": "host-tools",
                "key": "linux-x86_64",
                "identity": "host-1",
                "asset": "host.zip",
                "sha256": "b" * 64,
                "size": 123,
                "metadata": {"executable": "bin/tool"},
            },
            {
                "kind": "runtime",
                "key": "windows-x64-msvc-static",
                "identity": "runtime-1",
                "asset": "runtime.zip",
                "sha256": "c" * 64,
                "metadata": {"abi": {"linkage": "static"}},
            },
        ],
    }


def test_lock_requires_exact_format(tmp_path):
    lock = valid_lock()
    lock["format"] = "wrong"
    with pytest.raises(ContractError, match="format"):
        load_sdk_lock(write_json(tmp_path, "bad.json", lock))


def test_valid_lock_normalizes_digest(tmp_path):
    ref = load_sdk_lock(write_json(tmp_path, "lock.json", valid_lock()))
    assert ref.family == "semantic"
    assert ref.identity == "set-abc"
    assert ref.sha256 == "a" * 64
    assert ref.repository == "Mostorm-Labs/axiom"


def test_namespace_rejects_unsafe_values():
    for value in ("", "../runtime", "runtime/child", "runtime\\child", ".", ".."):
        with pytest.raises(ContractError):
            validate_namespace(value)


def test_sha256_requires_64_hex_chars():
    with pytest.raises(ContractError):
        validate_sha256("xyz")


def test_valid_release_index_parses_artifacts(tmp_path):
    index = load_release_index(write_json(tmp_path, "index.json", valid_index()))
    assert index.family == "semantic"
    assert index.release_set_id == "set-abc"
    assert [(a.kind, a.key) for a in index.artifacts] == [
        ("host-tools", "linux-x86_64"),
        ("runtime", "windows-x64-msvc-static"),
    ]
    assert index.artifacts[0].size == 123


def test_release_index_rejects_duplicate_kind_key(tmp_path):
    index = valid_index()
    index["artifacts"].append(dict(index["artifacts"][0], identity="host-2", asset="host2.zip"))
    with pytest.raises(ContractError, match="duplicate"):
        load_release_index(write_json(tmp_path, "index.json", index))


def test_release_index_rejects_non_object_metadata(tmp_path):
    index = valid_index()
    index["artifacts"][0]["metadata"] = ["bad"]
    with pytest.raises(ContractError, match="metadata"):
        load_release_index(write_json(tmp_path, "index.json", index))


def test_release_index_rejects_unknown_top_level_fields(tmp_path):
    index = valid_index()
    index["latest"] = True
    with pytest.raises(ContractError, match="unknown"):
        load_release_index(write_json(tmp_path, "index.json", index))


def test_lock_rejects_release_tag_path_traversal(tmp_path):
    lock = valid_lock()
    lock["releaseTag"] = "../sdk-v1"
    with pytest.raises(ContractError, match="releaseTag"):
        load_sdk_lock(write_json(tmp_path, "bad-tag.json", lock))
