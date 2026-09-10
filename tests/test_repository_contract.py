import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_ci_matrix_covers_supported_phase1_hosts():
    workflow = (ROOT / ".github/workflows/test.yml").read_text(encoding="utf-8")
    for runner in ("ubuntu-24.04", "windows-2025", "macos-15"):
        assert runner in workflow
    assert 'python-version: "3.11"' in workflow
    assert "pip install" in workflow
    assert "pytest" in workflow
    assert "axbuild --help" in workflow


def test_contract_schemas_are_published_and_identify_v1_formats():
    sdk = json.loads((ROOT / "schemas/sdk-lock-v1.schema.json").read_text(encoding="utf-8"))
    index = json.loads((ROOT / "schemas/release-index-v1.schema.json").read_text(encoding="utf-8"))
    artifact = json.loads((ROOT / "schemas/artifact-manifest-v1.schema.json").read_text(encoding="utf-8"))
    assert sdk["properties"]["format"]["const"] == "axbuild-sdk-lock-v1"
    assert index["properties"]["format"]["const"] == "axbuild-release-index-v1"
    assert artifact["properties"]["format"]["const"] == "axbuild-artifact-manifest-v1"
