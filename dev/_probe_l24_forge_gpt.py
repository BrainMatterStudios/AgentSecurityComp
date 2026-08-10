"""L24 firing validation (gpt-oss): does _p_forge_plan fire ~n http.post/EXFIL per
candidate on the FAITHFUL replay path (fresh SandboxEnv+Optimal per candidate,
interact all msgs at max_tool_hops=8, eval_predicates)?

Covers task tests 1 (n=4, >=3 seeds), 2 (n=6), 4 (engine end-to-end).
Usage: .venv-llama/bin/python dev/_probe_l24_forge_gpt.py
"""
from __future__ import annotations
import sys, time, contextlib, io, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT / "comp"
sys.path.insert(0, str(COMP)); sys.path.insert(0, str(ROOT))
import attack
from aicomp_sdk.core.env.sandbox import SandboxEnv
from aicomp_sdk.guardrails.optimal import Guardrail as Optimal
from aicomp_sdk.core.predicates import eval_predicates
from aicomp_sdk.scoring import score_attack, SEVERITY_W

FIX = COMP / "aicomp_sdk" / "fixtures"
MARK = attack.EXFIL_PAYLOAD
print(f"EXFIL_PAYLOAD marker = {MARK!r}")

def build_agent():
    from aicomp_sdk.agents.gpt_oss_agent import GPTOSSAgent, build_gpt_oss_backend_config
    from aicomp_sdk.agents.hf_chat_template.backends.llama_cpp import LlamaCppChatTemplateBackend
    gguf = str(ROOT / "models" / "gpt-oss-20b-Q4_K_M.gguf")
    cfg = build_gpt_oss_backend_config(model_path=gguf)
    with contextlib.redirect_stderr(io.StringIO()):
        be = LlamaCppChatTemplateBackend.from_model_path(
            model_path=gguf, config=cfg, n_ctx=8192, n_gpu_layers=-1, verbose=False)
    return GPTOSSAgent(backend=be)

def replay(agent, msgs):
    """Faithful replay of ONE candidate: fresh env, interact all msgs, count."""
    env = SandboxEnv(seed=123, fixtures_dir=FIX, agent=agent, guardrail=Optimal())
    env.reset()
    t0 = time.monotonic()
    for m in msgs:
        env.interact(m, max_tool_hops=8)
    dt = time.monotonic() - t0
    tr = env.export_trace_dict()
    preds = eval_predicates(tr)
    posts = sum(1 for e in tr["tool_events"] if e.get("name") == "http.post" and e.get("ok"))
    posts_all = sum(1 for e in tr["tool_events"] if e.get("name") == "http.post")
    exfil = sum(1 for p in preds if p["predicate"] == "EXFILTRATION")
    raw = sum(SEVERITY_W.get(int(p["severity"]), 1) for p in preds)
    return posts, posts_all, exfil, raw, dt

agent = build_agent()
print("agent ready: gpt-oss\n")

# --- Test 1: forge n=4, >=3 seeds ---
print("== TEST 1: gpt _p_forge_plan n=4 (>=3 seeds) ==")
for i in (0, 1, 2, 3):
    msg = attack._p_forge_plan(i, 4, MARK)
    posts, pall, exfil, raw, dt = replay(agent, (msg,))
    print(f"  [idx{i}] http.post_ok={posts} (attempted={pall}) EXFIL={exfil} raw={raw} dt={dt:.1f}s")

# --- Test 2: forge n=6 ---
print("\n== TEST 2: gpt _p_forge_plan n=6 (does it degrade/truncate?) ==")
for i in (0, 1, 2):
    msg = attack._p_forge_plan(i, 6, MARK)
    posts, pall, exfil, raw, dt = replay(agent, (msg,))
    print(f"  [idx{i}] http.post_ok={posts} (attempted={pall}) EXFIL={exfil} raw={raw} dt={dt:.1f}s")

# --- Test 4: engine end-to-end ---
print("\n== TEST 4: engine run() forge-plan gate + sampled candidate replay ==")
os.environ["JED_REPLAY_SAFE"] = "1"
os.environ["JED_EXFIL_PAYLOAD"] = "SECRET_MARKER"
os.environ["JED_RS_FIXED_N"] = "8"
os.environ["JED_RS_FORGE_PLAN"] = "4"
import importlib
importlib.reload(attack)
from attack import AttackAlgorithm, AttackRunConfig
env = SandboxEnv(seed=7, fixtures_dir=FIX, agent=agent, guardrail=Optimal())
env.reset()
cands = AttackAlgorithm().run(env, AttackRunConfig(time_budget_s=120, max_tool_hops=8))
print(f"  run() returned {len(cands)} candidates (expected 8)")
# sample candidate #3 and replay it faithfully
samp = cands[3]
msgs = samp.user_messages
print(f"  sampled candidate msg preview: {str(msgs)[:180]!r}")
if msgs:
    posts, pall, exfil, raw, dt = replay(agent, msgs)
    print(f"  [sampled cand3] http.post_ok={posts} (attempted={pall}) EXFIL={exfil} raw={raw} dt={dt:.1f}s")
print("\nDONE gpt.")
