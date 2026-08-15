import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_builder():
    path = ROOT / "dev" / "_build_l29.py"
    spec = importlib.util.spec_from_file_location("build_l29", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_l29_rungs_target_own_research_hypotheses():
    build = load_builder()
    run_dirs = [r[0] for r in build.RUNGS]
    envs = [r[3] for r in build.RUNGS]

    assert run_dirs == [
        "submission_kernel_l29_control",
        "submission_kernel_l29_split_hop8",
        "submission_kernel_l29_gpt_hop8_n260",
        "submission_kernel_l29_gemma_frac999",
        "submission_kernel_l29_deputy_hedge",
    ]

    assert envs[0] == build.BASE
    assert envs[1]["JED_RS_SPLIT"] == 1
    assert envs[1]["JED_RS_HOPPACK_GPT"] == 8
    assert envs[1]["JED_RS_HOPPACK_FORCE"] == 1
    assert envs[2]["JED_RS_ONLY"] == "gpt"
    assert envs[2]["JED_RS_FIXED_N"] == 260
    assert envs[2]["JED_RS_HOPPACK"] == 8
    assert envs[2]["JED_RS_HOPPACK_FORCE"] == 1
    assert envs[3]["JED_RS_ONLY"] == "gemma"
    assert envs[3]["JED_RS_FRAC_GEMMA"] == 999
    assert envs[4]["JED_RS_CHANNEL"] == "deputy"
    assert "JED_RS_HOPPACK" not in envs[4]


def test_l29_builder_writes_gpu_notebooks_and_metadata(tmp_path, monkeypatch):
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
        assert meta["enable_gpu"] is True
        assert meta["machine_shape"] == "NvidiaTeslaT4"
        assert meta["enable_internet"] is False
        assert meta["competition_sources"] == ["ai-agent-security-multi-step-tool-attacks"]
        for key, value in env.items():
            assert f"os.environ[{key!r}]={str(value)!r}" in env_src
