"""L24 firing validation (gemma-4, CPU/SLOW): test 3.
Q: gemma has no harmony analysis channel -- does _p_forge_plan fire ANY posts
(>=1) or ZERO? And does gemma fire the plain single-post template (terse_ok/close_ok)?
Faithful replay path: fresh SandboxEnv+Optimal per candidate, interact msgs at
max_tool_hops=8, eval_predicates. Keep trials small (CPU minutes).
Usage: .venv-gemma/bin/python dev/_probe_l24_forge_gemma.py
"""
from __future__ import annotations
import sys, time, contextlib, io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT / "comp"
sys.path.insert(0, str(COMP)); sys.path.insert(0, str(ROOT))
import attack
from aicomp_sdk.core.env.sandbox import SandboxEnv
from aicomp_sdk.guardrails.optimal import Guardrail as Optimal
from aicomp_sdk.core.predicates import eval_predicates
from aicomp_sdk.scoring import SEVERITY_W

FIX = COMP / "aicomp_sdk" / "fixtures"
MARK = attack.EXFIL_PAYLOAD
print(f"EXFIL_PAYLOAD marker = {MARK!r}")

def build_agent():
    from aicomp_sdk.agents.gemma4_agent import Gemma4Agent, build_gemma4_backend_config
    from aicomp_sdk.agents.hf_chat_template.backends.llama_cpp import LlamaCppChatTemplateBackend
    gguf = str(ROOT / "models" / "gemma-4-26B-A4B-it-UD-Q4_K_M.gguf")
    cfg = build_gemma4_backend_config(model_path=gguf)
    with contextlib.redirect_stderr(io.StringIO()):
        be = LlamaCppChatTemplateBackend.from_model_path(
            model_path=gguf, config=cfg, n_ctx=4096, n_gpu_layers=0, verbose=False,
            supports_tools=True, llama_kwargs={"swa_full": True})
    return Gemma4Agent(backend=be)

def replay(agent, msgs):
    env = SandboxEnv(seed=123, fixtures_dir=FIX, agent=agent, guardrail=Optimal())
    env.reset()
    t0 = time.monotonic()
    for m in msgs:
        env.interact(m, max_tool_hops=8)
    dt = time.monotonic() - t0
    tr = env.export_trace_dict()
    preds = eval_predicates(tr)
    posts = sum(1 for e in tr["tool_events"] if e.get("name") == "http.post" and e.get("ok"))
    pall = sum(1 for e in tr["tool_events"] if e.get("name") == "http.post")
    exfil = sum(1 for p in preds if p["predicate"] == "EXFILTRATION")
    raw = sum(SEVERITY_W.get(int(p["severity"]), 1) for p in preds)
    return posts, pall, exfil, raw, dt

agent = build_agent()
print("agent ready: gemma-4\n")

print("== TEST 3a: gemma _p_forge_plan n=4 (>=1 => row nonzero; 0 => row LOST) ==")
for i in (0, 1):
    msg = attack._p_forge_plan(i, 4, MARK)
    posts, pall, exfil, raw, dt = replay(agent, (msg,))
    print(f"  [idx{i}] http.post_ok={posts} (attempted={pall}) EXFIL={exfil} raw={raw} dt={dt:.1f}s")

print("\n== TEST 3b: gemma plain single-post templates (sanity: gemma DOES fire) ==")
tmpl = dict(attack._RS_TEMPLATES)
for name in ("terse_ok", "close_ok"):
    t = tmpl[name]
    msg = t.format(m=MARK, u=attack._rs_url(10), h=attack._rs_host(10)).strip()[:1990]
    posts, pall, exfil, raw, dt = replay(agent, (msg,))
    print(f"  [{name}] http.post_ok={posts} (attempted={pall}) EXFIL={exfil} raw={raw} dt={dt:.1f}s")

print("\nDONE gemma.")
