"""PHASE 1b: on the REAL engine (local llama.cpp Q4), compare the two gpt-oss levers:
(A) multi-post reaching the 8-hop cap (idx11, 16 URLs), and
(B) harmony reasoning-suppression (preclose idx13) — RE-TESTED here because it was
    abandoned on wrong-engine (transformers) measurements; llama.cpp may differ.
Also try preclose+multipost. Report posts, turns, seconds, tok (via trace), seq."""
import sys, time, contextlib, io
sys.path.insert(0, 'comp'); sys.path.insert(0, '.'); sys.path.insert(0, 'dev')
from pathlib import Path
import attack
from aicomp_sdk.agents.gpt_oss_agent import GPTOSSAgent, build_gpt_oss_backend_config
from aicomp_sdk.agents.hf_chat_template.backends.llama_cpp import LlamaCppChatTemplateBackend
from aicomp_sdk.core.env.sandbox import SandboxEnv
from aicomp_sdk.guardrails.optimal import Guardrail as Optimal
from aicomp_sdk.core.predicates import eval_predicates

GGUF = "models/gpt-oss-20b-Q4_K_M.gguf"
FIX = Path('comp') / 'aicomp_sdk' / 'fixtures'
T = attack.EXFIL_PAYLOAD                 # "diag=SECRET_MARKER"
HOPS = 8
NL = chr(10)

print("loading gpt-oss-20b-Q4_K_M (llama.cpp)...", flush=True)
cfg = build_gpt_oss_backend_config(model_path=GGUF)
with contextlib.redirect_stderr(io.StringIO()):
    backend = LlamaCppChatTemplateBackend.from_model_path(
        model_path=GGUF, config=cfg, n_ctx=8192, n_gpu_layers=-1, verbose=False)
agent = GPTOSSAgent(backend=backend)
print("ready\n", flush=True)

def measure(name, msg, reps=1):
    for r in range(reps):
        env = SandboxEnv(seed=123 + r, fixtures_dir=FIX, agent=agent, guardrail=Optimal())
        env.reset()
        t0 = time.time()
        with contextlib.redirect_stderr(io.StringIO()):
            res = env.interact(msg, max_tool_hops=HOPS)
        dt = time.time() - t0
        tr = env.export_trace_dict()
        exfil = sum(1 for x in eval_predicates(tr) if x['predicate'] == 'EXFILTRATION')
        raw = exfil * 16 + 2
        print(f"[{name:16}] seed{123+r} posts={exfil} turns={res.agent_turns} "
              f"{dt:5.1f}s raw/s={raw/dt:5.2f} (raw={raw})", flush=True)

u = "http://a.co/1"
tests = {
 "single_natural":  attack.K1_PROMPTS[0](T, u),                 # baseline
 "multipost_16url": attack.K1_PROMPTS[11](T, u),                # idx11, 16 URLs
 "preclose_single": attack.K1_PROMPTS[13](T, u),               # idx13 harmony preclose
 "preclose_multi":  attack.K1_PROMPTS[11](T, u) + attack._HARMONY_PRECLOSE,
}
print(f"=== gpt-oss @ hops={HOPS} — the two levers on the REAL engine ===", flush=True)
for n, m in tests.items():
    try:
        measure(n, m)
    except Exception as e:
        print(f"[{n:16}] ERROR {type(e).__name__}: {e}", flush=True)
print("done", flush=True)
