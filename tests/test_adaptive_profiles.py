import ast
import importlib
import os
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def load_attack_module(monkeypatch, **env):
    for key in list(os.environ):
        if key.startswith("JED_"):
            monkeypatch.delenv(key, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, str(value))
    sys.modules.pop("attack", None)
    import attack

    return importlib.reload(attack)


def load_profiles():
    tree = ast.parse((ROOT / "dev" / "build_notebook.py").read_text())
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "PROFILES":
                return ast.literal_eval(node.value)
    raise AssertionError("PROFILES assignment not found")


class FastEnv:
    def __init__(self, delay_s=0.001):
        self.delay_s = delay_s

    def reset(self):
        return None

    def interact(self, *_args, **_kwargs):
        time.sleep(self.delay_s)


class FailingEnv:
    def reset(self):
        raise RuntimeError("calibration failed")

    def interact(self, *_args, **_kwargs):
        raise RuntimeError("calibration failed")


def test_adaptive_n_never_exceeds_max_candidates(monkeypatch):
    attack = load_attack_module(
        monkeypatch,
        JED_MAX_CANDIDATES=400,
        JED_N_MIN=560,
        JED_CAL_SAMPLES=1,
        JED_REPLAY_PASSES=4,
        JED_REPLAY_BUDGET_S=28000,
        JED_N_SAFETY_PCT=118,
    )
    alg = attack.AttackAlgorithm()
    n = alg._adaptive_n(FastEnv(), 1800.0, 8, lambda _token, _url: "probe")
    assert n == 400


def test_adaptive_n_uses_safe_fallback_on_calibration_failure(monkeypatch):
    attack = load_attack_module(
        monkeypatch,
        JED_MAX_CANDIDATES=820,
        JED_N_FALLBACK=620,
        JED_CAL_SAMPLES=1,
    )
    alg = attack.AttackAlgorithm()
    n = alg._adaptive_n(FailingEnv(), 1800.0, 8, lambda _token, _url: "probe")
    assert n == 620


def test_private_chain_fast_path_can_fill_its_configured_max(monkeypatch):
    attack = load_attack_module(
        monkeypatch,
        JED_PRIVATE_CHAIN=1,
        JED_K1_ADAPTIVE=1,
        JED_MAX_CANDIDATES=400,
        JED_REPLAY_BUDGET_S=28000,
        JED_CAL_SAMPLES=1,
        JED_REPLAY_PASSES=4,
        JED_N_SAFETY_PCT=118,
        JED_CHAIN_N_MIN=60,
        JED_CHAIN_N_FALLBACK=240,
    )
    alg = attack.AttackAlgorithm()
    cands = alg.run(FastEnv(), attack.AttackRunConfig(time_budget_s=1800.0, max_tool_hops=8))
    assert len(cands) == 400
    assert all(len(candidate.user_messages) == 2 for candidate in cands[:5])


def test_adaptive_profiles_define_explicit_safe_fallbacks():
    profiles = load_profiles()
    assert profiles["k1_adaptive"]["env"]["JED_N_FALLBACK"] == "620"
    assert profiles["private_chain_400"]["env"]["JED_CHAIN_N_FALLBACK"] == "240"
