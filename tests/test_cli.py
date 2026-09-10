import json
import subprocess
import sys


def write_lock(tmp_path):
    path = tmp_path / "demo.lock.json"
    path.write_text(
        json.dumps(
            {
                "format": "axbuild-sdk-lock-v1",
                "family": "demo",
                "repository": "Mostorm-Labs/demo",
                "releaseTag": "demo-sdk-v1",
                "releaseSetId": "demo-set-1",
                "indexAsset": "demo-index.json",
                "indexSha256": "a" * 64,
            }
        ),
        encoding="utf-8",
    )
    return path


def write_index(tmp_path):
    path = tmp_path / "demo-index.json"
    path.write_text(
        json.dumps(
            {
                "format": "axbuild-release-index-v1",
                "family": "demo",
                "releaseSetId": "demo-set-1",
                "artifacts": [
                    {
                        "kind": "runtime",
                        "key": "windows-x64",
                        "identity": "runtime-1",
                        "asset": "runtime.zip",
                        "sha256": "b" * 64,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "axbuild", *args],
        text=True,
        capture_output=True,
        check=False,
    )


def test_validate_lock_command_emits_machine_readable_json(tmp_path):
    result = run_cli("validate-lock", str(write_lock(tmp_path)))
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["format"] == "axbuild-sdk-lock-v1"
    assert payload["family"] == "demo"
    assert payload["releaseSetId"] == "demo-set-1"
    assert result.stderr == ""


def test_validate_index_command_emits_artifact_count(tmp_path):
    result = run_cli("validate-index", str(write_index(tmp_path)))
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload == {
        "artifactCount": 1,
        "family": "demo",
        "format": "axbuild-release-index-v1",
        "releaseSetId": "demo-set-1",
    }


def test_malformed_contract_exits_nonzero_and_uses_stderr(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{}", encoding="utf-8")
    result = run_cli("validate-lock", str(path))
    assert result.returncode == 2
    assert result.stdout == ""
    assert "missing required field" in result.stderr


def test_module_help_works():
    result = run_cli("--help")
    assert result.returncode == 0
    assert "validate-lock" in result.stdout
    assert "validate-index" in result.stdout
