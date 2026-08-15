import importlib
import importlib.util
import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "comp"))


class _Cfg:
    time_budget_s = 30.0
    max_tool_hops = 8


class _UnusedEnv:
    def reset(self):
        raise AssertionError("fixed-N chainpack should not probe the env")


def _fresh_attack(monkeypatch):
    for key in tuple(os.environ):
        if key.startswith("JED_"):
            monkeypatch.delenv(key, raising=False)
    import attack

    return importlib.reload(attack)


def test_fixed_n_hoppack_can_chain_multiple_hop_messages_per_candidate(monkeypatch):
    attack = _fresh_attack(monkeypatch)
    monkeypatch.setenv("JED_REPLAY_SAFE", "1")
    monkeypatch.setenv("JED_RS_FIXED_N", "2")
    monkeypatch.setenv("JED_RS_HOPPACK", "8")
    monkeypatch.setenv("JED_RS_CHAINPACK", "4")
    monkeypatch.setenv("JED_RS_MAX_CAND", "20")

    candidates = attack.AttackAlgorithm().run(_UnusedEnv(), _Cfg())

    assert len(candidates) == 2
    assert all(len(c.user_messages) == 4 for c in candidates)
    assert all("Make 8 http.post calls" in msg for c in candidates for msg in c.user_messages)
    joined = "\n".join(msg for c in candidates for msg in c.user_messages)
    for host_idx in range(64):
        assert attack._rs_url(20000 + host_idx) in joined


def test_l31_builder_defines_chainpack_ladder_and_metadata(tmp_path, monkeypatch):
    path = ROOT / "dev" / "_build_l31.py"
    spec = importlib.util.spec_from_file_location("build_l31", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    run_dirs = [r.directory for r in module.RUNGS]
    envs = [r.env for r in module.RUNGS]

    assert run_dirs == [
        "submission_kernel_l31_chainpack_2x8",
        "submission_kernel_l31_chainpack_3x8",
        "submission_kernel_l31_chainpack_4x8",
        "submission_kernel_l31_chainpack_4x4",
        "submission_kernel_l31_fastemit_k8",
    ]
    assert envs[0]["JED_RS_HOPPACK"] == 8
    assert envs[0]["JED_RS_CHAINPACK"] == 2
    assert envs[1]["JED_RS_CHAINPACK"] == 3
    assert envs[2]["JED_RS_CHAINPACK"] == 4
    assert envs[3]["JED_RS_HOPPACK"] == 4
    assert envs[3]["JED_RS_CHAINPACK"] == 4
    assert envs[4]["JED_FAST_EMIT"] == 1

    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "ATTACK_B64", "YXR0YWNr")
    module.main()

    for rung in module.RUNGS:
        d = tmp_path / rung.directory
        nb = json.loads((d / "k.ipynb").read_text())
        meta = json.loads((d / "kernel-metadata.json").read_text())
        env_src = nb["cells"][1]["source"]

        assert meta["id"] == rung.slug
        assert meta["title"] == rung.title
        assert meta["enable_gpu"] is True
        assert meta["machine_shape"] == "NvidiaTeslaT4"
        assert meta["competition_sources"] == ["ai-agent-security-multi-step-tool-attacks"]
        for key, value in rung.env.items():
            assert f"os.environ[{key!r}]={str(value)!r}" in env_src
