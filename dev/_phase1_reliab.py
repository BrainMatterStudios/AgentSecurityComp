"""Reliability of idx13 preclose on gpt-oss across seeds + payload/URL variety.
A non-firing candidate only lowers score; only a time-overrun voids. So we need:
(a) fire rate ~100%, (b) stable low per-candidate time. Compare to natural single."""
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
T = attack.EXFIL_PAYLOAD
HOPS = 8
print("loading gpt-oss...", flush=True)
cfg = build_gpt_oss_backend_config(model_path=GGUF)
with contextlib.redirect_stderr(io.StringIO()):
    backend = LlamaCppChatTemplateBackend.from_model_path(model_path=GGUF, config=cfg, n_ctx=8192, n_gpu_layers=-1, verbose=False)
agent = GPTOSSAgent(backend=backend)
print("ready\n", flush=True)

def one(msg, seed):
    env = SandboxEnv(seed=seed, fixtures_dir=FIX, agent=agent, guardrail=Optimal())
    env.reset()
    t0 = time.time()
    with contextlib.redirect_stderr(io.StringIO()):
        env.interact(msg, max_tool_hops=HOPS)
    dt = time.time() - t0
    tr = env.export_trace_dict()
    exfil = sum(1 for x in eval_predicates(tr) if x['predicate'] == 'EXFILTRATION')
    return exfil, dt

for label, fn in [("natural", attack.K1_PROMPTS[0]), ("preclose13", attack.K1_PROMPTS[13])]:
    fires = 0; tsum = 0.0; n = 0
    for i in range(6):
        u = attack._k1_url(i) if hasattr(attack, "_k1_url") else f"http://a.co/{i+1}"
        try:
            e, dt = one(fn(T, u), 100 + i)
        except Exception as ex:
            print(f"[{label}] seed{100+i} ERROR {type(ex).__name__}: {ex}", flush=True); continue
        fires += (1 if e >= 1 else 0); tsum += dt; n += 1
        print(f"[{label}] seed{100+i} url={u} posts={e} {dt:4.1f}s", flush=True)
    if n:
        print(f"==> {label}: fire_rate={fires}/{n} avg={tsum/n:4.1f}s  raw/s(if fires)={18*fires/tsum:5.2f}\n", flush=True)
print("done", flush=True)
