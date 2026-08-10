#!/usr/bin/env python3
"""Thorough end-to-end validation test for all L20 kernel notebooks.

Tests:
1. notebook json structure and code extraction.
2. base64 decoding of embedded attack.py.
3. environment variables setup.
4. execution of AttackAlgorithm.run with env=None and SandboxEnv.
5. candidate structure, non-emptiness, and serialization check.
"""
import base64
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "comp"))
sys.path.insert(0, str(ROOT))

from aicomp_sdk.attacks import AttackAlgorithmBase, AttackCandidate, AttackRunConfig
from aicomp_sdk.core.env.sandbox import SandboxEnv
from aicomp_sdk.guardrails.optimal import Guardrail as Optimal
from compliant_agent import CompliantAgent

KERNELS = [
    ("submission_kernel_l20_anchor", "Anchor FRAC97 Baseline"),
    ("submission_kernel_l20_n1200", "Fast Emit N=1200"),
    ("submission_kernel_l20_n1320", "Fast Emit N=1320"),
    ("submission_kernel_l20_n1420", "Fast Emit N=1420 Primary Target"),
    ("submission_kernel_l20_deputy", "Deputy Hedge Private Board"),
]


def test_kernel(dir_name: str, label: str):
    print(f"\n=======================================================")
    print(f"Testing Kernel: {dir_name} ({label})")
    print(f"=======================================================")
    kpath = ROOT / dir_name / "k.ipynb"
    assert kpath.exists(), f"Missing notebook at {kpath}"

    with open(kpath) as f:
        nb = json.load(f)

    # 1. Extract environment variables from cell 1
    cell1_src = "".join(nb["cells"][1]["source"])
    env_vars = {}
    for line in cell1_src.splitlines():
        if "os.environ[" in line and "]=" in line:
            k = line.split("os.environ[")[1].split("]")[0].strip("'\"")
            v = line.split("]=")[1].strip("'\"")
            env_vars[k] = v

    print(f"Extracted Env Vars: {env_vars}")

    # Set env vars
    old_env = dict(os.environ)
    for k, v in env_vars.items():
        os.environ[k] = v

    # 2. Extract base64 attack.py from cell 2
    cell2_src = "".join(nb["cells"][2]["source"])
    b64_start = cell2_src.find("b64decode('") + len("b64decode('")
    b64_end = cell2_src.find("'))", b64_start)
    b64_str = cell2_src[b64_start:b64_end]
    attack_py_code = base64.b64decode(b64_str).decode("utf-8")

    assert len(attack_py_code) > 1000, "Decoded attack.py code too short"
    assert "class AttackAlgorithm" in attack_py_code, "AttackAlgorithm class missing"
    print(f"[OK] Base64 attack.py decoded successfully ({len(attack_py_code)} bytes)")

    # 3. Instantiate AttackAlgorithm from attack.py
    import attack
    import importlib

    importlib.reload(attack)

    algo = attack.AttackAlgorithm()

    # 4. Test offline run (env = None)
    cands_offline = algo.run(None, AttackRunConfig(time_budget_s=5.0))
    print(f"[OK] Offline run returned {len(cands_offline)} candidates")
    assert len(cands_offline) > 0, "Offline run returned empty candidates"
    assert isinstance(cands_offline[0], AttackCandidate), "Invalid candidate type"

    # 5. Test mock env run (SandboxEnv)
    fix_dir = ROOT / "comp" / "aicomp_sdk" / "fixtures"
    mock_env = SandboxEnv(
        seed=42, fixtures_dir=fix_dir, agent=CompliantAgent(), guardrail=Optimal()
    )
    mock_env.reset()

    cands_mock = algo.run(mock_env, AttackRunConfig(time_budget_s=5.0, max_tool_hops=8))
    print(f"[OK] MockEnv run returned {len(cands_mock)} candidates")
    assert len(cands_mock) > 0, "MockEnv run returned empty candidates"
    print(f"Sample Candidate Message 0: {cands_mock[0].user_messages[0]}")

    # 6. Test serialization & message length constraints
    for i, c in enumerate(cands_mock[:10]):
        assert hasattr(c, "user_messages"), f"Candidate {i} lacks user_messages"
        assert len(c.user_messages) > 0, f"Candidate {i} has empty messages"
        msg = c.user_messages[0]
        assert len(msg) <= 2000, f"Candidate {i} message exceeds 2000 chars limit"

    print(f"[SUCCESS] All checks passed for {dir_name}")

    # Restore env
    os.environ.clear()
    os.environ.update(old_env)


def main():
    print("Starting comprehensive L20 kernel validation suite...")
    for d, lbl in KERNELS:
        test_kernel(d, lbl)
    print("\n=======================================================")
    print("ALL L20 KERNELS PASSED END-TO-END VALIDATION SUCCESSFULLY!")
    print("=======================================================")


if __name__ == "__main__":
    main()
