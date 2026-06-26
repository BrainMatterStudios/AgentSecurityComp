"""Reproduce the gateway's INVALID_SUBMISSION ('incorrect format') check locally.

For each profile we set its env knobs, run AttackAlgorithm.run() against a local
env, then validate EVERY returned candidate exactly as the gateway/inference
server do. A single failing candidate is what produces 'incorrect format'.
"""
from __future__ import annotations
import os
import sys
import time
import traceback
from pathlib import Path

COMP = Path(__file__).resolve().parents[1] / "comp"
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COMP))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "dev"))

from aicomp_sdk.core.env.sandbox import SandboxEnv
from aicomp_sdk.guardrails.optimal import Guardrail as Optimal
from aicomp_sdk.attacks import AttackRunConfig
from aicomp_sdk.evaluation.ops import MAX_REPLAY_FINDINGS, MAX_REPLAY_MESSAGES_PER_FINDING
from aicomp_sdk.core.env.api import MAX_USER_MESSAGE_CHARS
from compliant_agent import CompliantAgent

FIX = COMP / "aicomp_sdk" / "fixtures"

PROFILES = {
    "k1_640":            {"JED_K1_SHORT": "1", "JED_K1_PROMPT": "0", "JED_MAX_CANDIDATES": "640", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"},
    "k1_adaptive":       {"JED_K1_SHORT": "1", "JED_K1_ADAPTIVE": "1", "JED_MAX_CANDIDATES": "820", "JED_REPLAY_BUDGET_S": "28000", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1", "JED_N_MIN": "50", "JED_N_FALLBACK": "620"},
    "private_chain_400": {"JED_PRIVATE_CHAIN": "1", "JED_K1_ADAPTIVE": "1", "JED_MAX_CANDIDATES": "400", "JED_REPLAY_BUDGET_S": "28000", "JED_CHAIN_N_MIN": "60", "JED_CHAIN_N_FALLBACK": "240"},
    "multi8_130_CTL":    {"JED_PUBLIC_MULTI": "1", "JED_MULTI_TINY": "1", "JED_MULTI_POSTS": "8", "JED_MAX_CANDIDATES": "130", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"},
}

# Knobs that any profile might set — cleared between runs so they don't leak.
ALL_KNOBS = set()
for d in PROFILES.values():
    ALL_KNOBS |= set(d)
ALL_KNOBS |= {"JED_K1_SHORT","JED_K1_PROMPT","JED_K1_ADAPTIVE","JED_PRIVATE_CHAIN",
             "JED_PUBLIC_MULTI","JED_MULTI_TINY","JED_MULTI_POSTS","JED_MULTI_PROMPT",
             "JED_MAX_CANDIDATES","JED_MAX_PRIVATE_CHAINS","JED_SEARCH_FRACTION",
             "JED_REPLAY_BUDGET_S","JED_N_MIN","JED_N_FALLBACK","JED_CHAIN_N_MIN","JED_CHAIN_N_FALLBACK"}


def validate(messages, index):
    """Exactly the gateway/inference-server validation contract."""
    if isinstance(messages, (str, bytes)):
        return f"cand[{index}].user_messages is a str/bytes, not a sequence"
    try:
        msgs = tuple(messages)
    except TypeError:
        return f"cand[{index}].user_messages not iterable"
    if not msgs:
        return f"cand[{index}] has zero messages"
    if len(msgs) > MAX_REPLAY_MESSAGES_PER_FINDING:
        return f"cand[{index}] chain len {len(msgs)} > {MAX_REPLAY_MESSAGES_PER_FINDING}"
    for j, m in enumerate(msgs):
        if not isinstance(m, str):
            return f"cand[{index}].msg[{j}] not a str ({type(m).__name__})"
        if not m.strip():
            return f"cand[{index}].msg[{j}] empty/whitespace"
        if len(m) > MAX_USER_MESSAGE_CHARS:
            return f"cand[{index}].msg[{j}] len {len(m)} > {MAX_USER_MESSAGE_CHARS}"
    return None


def run_profile(name, knobs):
    for k in ALL_KNOBS:
        os.environ.pop(k, None)
    os.environ.update(knobs)
    # Re-import attack fresh each time (module-level reads of env are at call time,
    # but be safe and reload).
    for mod in list(sys.modules):
        if mod == "attack":
            del sys.modules[mod]
    import attack
    algo = attack.AttackAlgorithm()
    env = SandboxEnv(seed=123, fixtures_dir=FIX, agent=CompliantAgent(), guardrail=Optimal())
    cfg = AttackRunConfig(time_budget_s=1800.0, max_tool_hops=8)
    t0 = time.time()
    try:
        cands = algo.run(env, cfg)
    except Exception:
        print(f"\n### {name}: run() RAISED — this alone = incorrect format")
        traceback.print_exc()
        return
    dt = time.time() - t0
    n = len(cands) if cands is not None else 0
    print(f"\n### {name}: returned {n} candidates in {dt:.1f}s")
    if cands is None:
        print("  !! run() returned None -> gateway treats as no candidates")
        return
    if n > MAX_REPLAY_FINDINGS:
        print(f"  note: {n} > MAX_REPLAY_FINDINGS({MAX_REPLAY_FINDINGS}); only first {MAX_REPLAY_FINDINGS} replayed")
    bad = 0
    first_bad = None
    for i, c in enumerate(cands[:MAX_REPLAY_FINDINGS]):
        um = getattr(c, "user_messages", c)
        err = validate(um, i)
        if err:
            bad += 1
            if first_bad is None:
                first_bad = (i, err, um)
    if bad:
        print(f"  >>> {bad} INVALID candidate(s) -> gateway raises INVALID_SUBMISSION -> 'incorrect format'")
        i, err, um = first_bad
        print(f"      first bad: {err}")
        print(f"      payload: {repr(um)[:300]}")
    else:
        print(f"  OK: all {min(n,MAX_REPLAY_FINDINGS)} candidates pass validation (no format failure from candidates)")
        # show a sample + msg length stats
        lens = [len(m) for c in cands[:MAX_REPLAY_FINDINGS] for m in c.user_messages]
        print(f"      msg count/cand: {[len(c.user_messages) for c in cands[:3]]}...  max msg len={max(lens)}")
        print(f"      sample[0]: {repr(cands[0].user_messages)[:200]}")


if __name__ == "__main__":
    print(f"MAX_REPLAY_FINDINGS={MAX_REPLAY_FINDINGS} MAX_MSGS/find={MAX_REPLAY_MESSAGES_PER_FINDING} MAX_CHARS={MAX_USER_MESSAGE_CHARS}")
    for nm, kb in PROFILES.items():
        run_profile(nm, kb)
