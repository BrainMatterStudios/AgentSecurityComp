import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_builder():
    path = ROOT / "dev" / "_build_l18.py"
    spec = importlib.util.spec_from_file_location("build_l18", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_l18_rungs_define_hybrid_reset_set():
    build = load_builder()
    run_dirs = [r[0] for r in build.RUNGS]
    slugs = [r[1] for r in build.RUNGS]
    envs = [r[3] for r in build.RUNGS]

    assert run_dirs == [
        "submission_kernel_l18_anchor_rs97",
        "submission_kernel_l18_aco8n60",
        "submission_kernel_l18_aco8n120",
        "submission_kernel_l18_split_safe",
        "submission_kernel_l18_aco8n230",
    ]
    assert slugs == [
        "ahmedmobasher86/jed-public-pt-safe",
        "ahmedmobasher86/jed-public-pt-probe",
        "ahmedmobasher86/jed-public-k1nx-1000",
        "ahmedmobasher86/jed-public-k1nx-1200",
        "ahmedmobasher86/jed-public-k1nx-800",
    ]
    assert envs[0]["JED_REPLAY_SAFE"] == 1
    assert envs[0]["JED_RS_TEMPLATES"] == "5,6"
    assert envs[0]["JED_RS_FRAC"] == 97
    for idx in (1, 2, 4):
        assert envs[idx]["JED_GEMMA_FORGE"] == 1
        assert envs[idx]["JED_GEMMA_FORGE_REPEAT_A_PATHS"] == 1
        assert envs[idx]["JED_GEMMA_FORGE_K"] == 8
        assert envs[idx]["JED_GEMMA_FORGE_MIN_POSTS"] >= 6
    assert envs[1]["JED_GEMMA_FORGE_N"] == 60
    assert envs[2]["JED_GEMMA_FORGE_N"] == 120
    assert envs[4]["JED_GEMMA_FORGE_N"] == 230
    assert envs[3]["JED_AGG_PROBE"] == 1
    assert envs[3]["JED_GPTOSS_MP_K"] == 4
    assert envs[3]["JED_GEMMA_N"] <= 560


def test_l18_builder_writes_cpu_save_notebooks_and_metadata(tmp_path, monkeypatch):
    build = load_builder()
    monkeypatch.setattr(build, "ROOT", tmp_path)
    monkeypatch.setattr(build, "ATTACK_B64", "ZmFrZQ==")

    build.main()

    for directory, slug, title, env, _note in build.RUNGS:
        d = tmp_path / directory
        nb = json.loads((d / "k.ipynb").read_text())
        meta = json.loads((d / "kernel-metadata.json").read_text())
        env_src = nb["cells"][1]["source"]

        assert meta["id"] == slug
        assert meta["title"] == title
        assert meta["code_file"] == "k.ipynb"
        assert meta["enable_gpu"] is False
        assert "machine_shape" not in meta
        assert meta["enable_internet"] is False
        assert meta["competition_sources"] == ["ai-agent-security-multi-step-tool-attacks"]
        for key, value in env.items():
            assert f"os.environ[{key!r}]={str(value)!r}" in env_src

