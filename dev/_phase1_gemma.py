"""PHASE 1 gemma (the higher board), faithful: exact Kaggle GGUF
gemma-4-26B-A4B-it-UD-Q4_K_M via the SDK Gemma4Agent + SandboxEnv at hops=8.
swa_full=True avoids the known gemma SWA crash on llama-cpp-python. Measure
posts-per-candidate + firing for single vs multi-post + toolonly variants."""
import sys, time, contextlib, io
sys.path.insert(0, 'comp'); sys.path.insert(0, '.'); sys.path.insert(0, 'dev')
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

print("loading gemma-4-26B UD-Q4_K_M (llama.cpp, swa_full=True)...", flush=True)
cfg = build_gemma4_backend_config(model_path=GGUF)
with contextlib.redirect_stderr(io.StringIO()):
    backend = LlamaCppChatTemplateBackend.from_model_path(
        model_path=GGUF, config=cfg, n_ctx=8192, n_gpu_layers=-1, verbose=False,
        supports_tools=True, llama_kwargs={"swa_full": True})
agent = Gemma4Agent(backend=backend)
print("ready\n", flush=True)

def measure(name, msg):
    env = SandboxEnv(seed=123, fixtures_dir=FIX, agent=agent, guardrail=Optimal())
    env.reset()
    t0 = time.time()
    with contextlib.redirect_stderr(io.StringIO()):
        res = env.interact(msg, max_tool_hops=HOPS)
    dt = time.time() - t0
    tr = env.export_trace_dict()
    exfil = sum(1 for x in eval_predicates(tr) if x['predicate'] == 'EXFILTRATION')
    raw = exfil * 16 + 2
    print(f"[{name:16}] posts={exfil} turns={res.agent_turns} {dt:5.1f}s "
          f"raw/s={raw/dt:5.2f} (raw={raw})", flush=True)

u = "http://a.co/1"
tests = {
 "single_natural":  attack.K1_PROMPTS[0](T, u),
 "toolonly_single": attack.K1_PROMPTS[12](T, u),   # idx12 "emit only the tool call"
 "multipost_16url": attack.K1_PROMPTS[11](T, u),   # idx11 list of 16
}
print(f"=== gemma @ hops={HOPS} ===", flush=True)
for n, m in tests.items():
    try:
        measure(n, m)
    except Exception as e:
        print(f"[{n:16}] ERROR {type(e).__name__}: {e}", flush=True)
print("done", flush=True)
