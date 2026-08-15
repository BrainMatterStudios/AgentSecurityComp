import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_builder():
    path = ROOT / "dev" / "_build_l30.py"
    spec = importlib.util.spec_from_file_location("build_l30", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_l30_rungs_cover_control_capacity_and_crown_attempts():
    build = load_builder()
    run_dirs = [r.directory for r in build.RUNGS]
    envs = [r.env for r in build.RUNGS]

    assert run_dirs == [
        "submission_kernel_l30_l27_control",
        "submission_kernel_l30_fixed1100",
        "submission_kernel_l30_fixed1530",
        "submission_kernel_l30_split_hop4",
        "submission_kernel_l30_fastemit_k8",
    ]

    assert build.RUNGS[0].source_kind == "d4"
    assert "REPLAY_SAFE_FRAC = 0.98" in build.D4_CONTROL_SOURCE
    assert envs[1]["JED_RS_FIXED_N"] == 1100
    assert envs[1]["JED_REPLAY_SAFE"] == 1
    assert "JED_RS_HOPPACK" not in envs[1]
    assert envs[2]["JED_RS_FIXED_N"] == 1530
    assert envs[2]["JED_REPLAY_SAFE"] == 1
    assert envs[3]["JED_RS_SPLIT"] == 1
    assert envs[3]["JED_RS_HOPPACK_GPT"] == 4
    assert envs[3]["JED_RS_HOPPACK_FORCE"] == 1
    assert envs[4]["JED_FAST_EMIT"] == 1
    assert envs[4]["JED_EMIT_K"] == 8
    assert envs[4]["JED_EMIT_CALIBRATE"] == 1
    assert envs[4]["JED_EMIT_SAFETY"] == "0.55"
    assert envs[4]["JED_EMIT_CAP_N"] == 2000


def test_l30_builder_writes_submission_notebooks_and_metadata(tmp_path, monkeypatch):
    build = load_builder()
    monkeypatch.setattr(build, "ROOT", tmp_path)
    monkeypatch.setattr(build, "ATTACK_B64", "YXR0YWNr")
    monkeypatch.setattr(build, "D4_B64", "ZDQ=")

    build.main()

    for rung in build.RUNGS:
        d = tmp_path / rung.directory
        nb = json.loads((d / "k.ipynb").read_text())
        meta = json.loads((d / "kernel-metadata.json").read_text())
        env_src = nb["cells"][1]["source"]
        write_src = nb["cells"][2]["source"]

        assert meta["id"] == rung.slug
        assert meta["title"] == rung.title
        assert meta["code_file"] == "k.ipynb"
        assert meta["enable_gpu"] is True
        assert meta["machine_shape"] == "NvidiaTeslaT4"
        assert meta["enable_internet"] is False
        assert meta["competition_sources"] == ["ai-agent-security-multi-step-tool-attacks"]
        assert "attack.py" in write_src
        for key, value in rung.env.items():
            assert f"os.environ[{key!r}]={str(value)!r}" in env_src
