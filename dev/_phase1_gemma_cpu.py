"""FAITHFUL gemma measurement on CPU (Metal has the llama_decode -3 bug; CPU decodes
fine). llama.cpp + exact Kaggle GGUF via the SDK Gemma4Agent+SandboxEnv at hops=8.
Firing + posts-per-candidate transfer regardless of CPU/CUDA (wall-time does not).
Goal: does idx4(stop)/idx12(toolonly) cut the wasted final response while FIRING
reliably (no degrade-to-prose misfire), and does multipost(idx11) reach 8 hops?"""
import sys, time, contextlib, io
sys.path.insert(0, 'comp'); sys.path.insert(0, '.')
from pathlib import Path
import attack
from aicomp_sdk.agents.gemma4_agent import Gemma4Agent, build_gemma4_backend_config
from aicomp_sdk.agents.hf_chat_template.backends.llama_cpp import LlamaCppChatTemplateBackend
from aicomp_sdk.core.env.sandbox import SandboxEnv
from aicomp_sdk.guardrails.optimal import Guardrail as Optimal
from aicomp_sdk.core.predicates import eval_predicates

GGUF = "models/gemma-4-26B-A4B-it-UD-Q4_K_M.gguf"
FIX = Path('comp') / 'aicomp_sdk' / 'fixtures'
T = attack.EXFIL_PAYLOAD
HOPS = 8

print("loading gemma on CPU (n_gpu_layers=0)...", flush=True)
cfg = build_gemma4_backend_config(model_path=GGUF)
with contextlib.redirect_stderr(io.StringIO()):
    be = LlamaCppChatTemplateBackend.from_model_path(
        model_path=GGUF, config=cfg, n_ctx=4096, n_gpu_layers=0, verbose=False,
        supports_tools=True, llama_kwargs={"swa_full": True})
agent = Gemma4Agent(backend=be)
print("ready\n", flush=True)

def measure(name, msg, seed=123):
    env = SandboxEnv(seed=seed, fixtures_dir=FIX, agent=agent, guardrail=Optimal())
    env.reset()
    t0 = time.time()
    with contextlib.redirect_stderr(io.StringIO()):
        res = env.interact(msg, max_tool_hops=HOPS)
    dt = time.time() - t0
    tr = env.export_trace_dict()
    ev = tr.get("tool_events", [])
    exfil = sum(1 for x in eval_predicates(tr) if x['predicate'] == 'EXFILTRATION')
    seq = ",".join(f"{e.get('name','?')}{'+' if e.get('ok') else 'x'}" for e in ev) or "-none-"
    print(f"[{name:14}] posts={exfil} tool_calls={res.successful_tool_calls} turns={res.agent_turns} "
          f"{dt:5.1f}s seq={seq}", flush=True)

u = "http://a.co/1"
tests = {
 "natural":   attack.K1_PROMPTS[0](T, u),   # idx0 baseline (~87 tok/post, boundary ~560)
 "stop":      attack.K1_PROMPTS[4](T, u),    # idx4: keep proven gen1, collapse gen2 (low misfire risk)
 "toolonly":  attack.K1_PROMPTS[12](T, u),   # idx12: rewrite gen1 (misfire risk)
 "multipost": attack.K1_PROMPTS[11](T, u),   # idx11: 16-URL list, does gemma reach 8 hops?
}
print(f"=== gemma @ hops={HOPS} (CPU, faithful) — want: fires 100%, fewer turns/post ===", flush=True)
for n, m in tests.items():
    try:
        measure(n, m)
    except Exception as e:
        print(f"[{n:14}] ERROR {type(e).__name__}: {e}", flush=True)
print("done", flush=True)
