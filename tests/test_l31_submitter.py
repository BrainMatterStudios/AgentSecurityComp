import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, rel: str):
    path = ROOT / rel
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_l31_submitter_uses_five_ordered_slots_and_reset_margin():
    submit = load_module("submit_l31", "dev/_submit_l31_after_reset.py")

    labels = [item["label"] for item in submit.DEFAULT_MANIFEST["submissions"]]
    assert labels == [
        "chainpack-2x8",
        "chainpack-3x8",
        "chainpack-4x8",
        "chainpack-4x4",
        "fastemit-k8",
    ]
    assert submit.DEFAULT_MARGIN_MINUTES == 7
    assert submit.COMPETITION == "ai-agent-security-multi-step-tool-attacks"


def test_l31_arm_script_copies_all_kernel_directories():
    arm = load_module("arm_l31", "dev/_arm_l31_launchd.py")
    build = load_module("build_l31", "dev/_build_l31.py")

    assert [item["directory"] for item in arm.manifest()["submissions"]] == [
        rung.directory for rung in build.RUNGS
    ]
    assert arm.LAUNCHD_LABEL == "com.ahmed.agentsecuritycomp.l31-submit"
