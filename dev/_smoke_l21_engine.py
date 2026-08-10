"""Local smoke test: run the full _run_fast_emit multi-call calibrate path on gpt-oss.
Verifies candidate count/message shape and that calibration sizing lands safely."""
import os, sys, time, contextlib, io
sys.path.insert(0, 'comp'); sys.path.insert(0, '.')
from pathlib import Path
os.environ["JED_FAST_EMIT"] = "1"
os.environ["JED_EMIT_K"] = "8"
os.environ["JED_EMIT_CALIBRATE"] = "1"
os.environ["JED_EMIT_SAFETY"] = "0.5"
os.environ["JED_EMIT_CAP_N"] = "400"
import attack
from aicomp_sdk.agents.gpt_oss_agent import GPTOSSAgent, build_gpt_oss_backend_config
from aicomp_sdk.agents.hf_chat_template.backends.llama_cpp import LlamaCppChatTemplateBackend
from aicomp_sdk.core.env.sandbox import SandboxEnv
from aicomp_sdk.guardrails.optimal import Guardrail as Optimal
from aicomp_sdk.core.predicates import eval_predicates

GGUF = "models/gpt-oss-20b-Q4_K_M.gguf"
FIX = Path('comp') / 'aicomp_sdk' / 'fixtures'
cfg = build_gpt_oss_backend_config(model_path=GGUF)
with contextlib.redirect_stderr(io.StringIO()):
    be = LlamaCppChatTemplateBackend.from_model_path(
        model_path=GGUF, config=cfg, n_ctx=8192, n_gpu_layers=-1, verbose=False)
ag = GPTOSSAgent(backend=be)

class FakeEnv:
    def __init__(self):
        self._env = SandboxEnv(seed=123, fixtures_dir=FIX, agent=ag, guardrail=Optimal())
        self._env.reset()
    def reset(self):
        return self._env.reset()
    def interact(self, msg, **kw):
        return self._env.interact(msg, **kw)
    def export_trace_dict(self):
        return self._env.export_trace_dict()

att = attack.AttackAlgorithm()
env = FakeEnv()
config = attack.AttackRunConfig(time_budget_s=9000.0, max_tool_hops=8)
t0 = time.time()
cands = att.run(env, config)
print(f"\nengine returned {len(cands)} candidates in {time.time()-t0:.0f}s", flush=True)
m0 = cands[0].user_messages[0] if hasattr(cands[0], 'user_messages') else cands[0][0]
print(f"msg[0] len={len(m0)}: {m0[:120]}...", flush=True)

# Verify a candidate fires 8 posts through a fresh env (replay-style, no calibrate reuse).
env2 = SandboxEnv(seed=555, fixtures_dir=FIX, agent=ag, guardrail=Optimal())
env2.reset()
with contextlib.redirect_stderr(io.StringIO()):
    env2.interact(m0, max_tool_hops=8)
posts = sum(1 for x in eval_predicates(env2.export_trace_dict()) if x['predicate'] == 'EXFILTRATION')
print(f"candidate[0] posts (fresh env) = {posts}", flush=True)
print("done", flush=True)
