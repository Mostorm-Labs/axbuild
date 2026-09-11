from pathlib import Path


WORKFLOW = Path(".github/workflows/nearcast-airplay-qualification.yml")
TOOLING_REVISION = "7134fb08dbb4a4edd12f9c3005759a84e6b89fde"
SOURCE_SHA = "0768c47f3df888bddbca7531299f11776188d2ee029332294a1af08bb2f1575c"


def test_real_qualification_workflow_pins_all_external_inputs():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert TOOLING_REVISION in workflow
    assert "Mostorm-Labs/NearCast" in workflow
    assert SOURCE_SHA in workflow
    assert "qualify-nearcast-airplay-artifact" in workflow
    assert "actions/upload-artifact@v4" in workflow
    assert "if-no-files-found: error" in workflow


def test_real_qualification_workflow_checks_all_required_outputs():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    for name in (
        "nearcast-airplay-runtime-windows-x64-release.zip",
        "nearcast-airplay-artifact-manifest.json",
        "nearcast-airplay-provenance.json",
        "qualification-report.json",
    ):
        assert name in workflow
