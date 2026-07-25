"""SMOKE TEST for the new JED_REPLAY_SAFE adaptive-sizing mode (gpt Metal replica).
Verifies the LOGIC end-to-end through the real SandboxEnv: fingerprint -> template
race -> replay-cost-bounded fill -> hard clamp, with candidates that actually fire.
Wall-time/N here is Mac-not-Kaggle (meaningless count); we only confirm the loop runs,
selects a firing template, and returns valid firing single-post candidates. Uses a
SHORT budget so search_time_left() stops the fill fast."""
import sys, os, contextlib, io, time
sys.path.insert(0, 'comp'); sys.path.insert(0, '.')
os.environ['JED_REPLAY_SAFE'] = '1'
os.environ['JED_RS_REPS'] = '2'          # fewer probes -> faster smoke
os.environ['JED_RS_MARGIN'] = '10'
from pathlib import Path
import types
import attack
from aicomp_sdk.agents.gpt_oss_agent import GPTOSSAgent, build_gpt_oss_backend_config
from aicomp_sdk.agents.hf_chat_template.backends.llama_cpp import LlamaCppChatTemplateBackend
from aicomp_sdk.core.env.sandbox import SandboxEnv
from aicomp_sdk.guardrails.optimal import Guardrail as Optimal
from aicomp_sdk.core.predicates import eval_predicates

GGUF = "models/gpt-oss-20b-Q4_K_M.gguf"; FIX = Path('comp') / 'aicomp_sdk' / 'fixtures'
print("loading gpt-oss-20b Q4 (Metal)...", flush=True)
cfg = build_gpt_oss_backend_config(model_path=GGUF)
with contextlib.redirect_stderr(io.StringIO()):
    be = LlamaCppChatTemplateBackend.from_model_path(model_path=GGUF, config=cfg, n_ctx=8192, n_gpu_layers=-1, verbose=False)
ag = GPTOSSAgent(backend=be)
env = SandboxEnv(seed=123, fixtures_dir=FIX, agent=ag, guardrail=Optimal())

alg = attack.AttackAlgorithm(config={})
conf = types.SimpleNamespace(time_budget_s=90.0, max_tool_hops=8)  # short budget

print("running _run_replay_safe (JED_REPLAY_SAFE=1, budget=90s)...", flush=True)
t0 = time.time()
with contextlib.redirect_stderr(io.StringIO()):
    cands = alg.run(env, conf)
dt = time.time() - t0
print(f"\nreturned {len(cands)} candidates in {dt:.0f}s", flush=True)

# inspect: distinct hosts (cells) + re-verify a few fire through the real path
msgs = []
for c in cands:
    m = getattr(c, 'user_messages', None) or []
    msgs.append(m[0] if m else "")
hosts = set()
for m in msgs:
    if 'http://' in m:
        hosts.add(m.split('http://', 1)[1].split()[0].split('<')[0])
print(f"distinct hosts (=> distinct cells): {len(hosts)}  sample: {sorted(hosts)[:5]}")
print(f"sample candidate[0]: {msgs[0][:120]!r}")

# independent re-fire check on 3 returned candidates
fired = 0
for m in msgs[:3]:
    env.reset()
    with contextlib.redirect_stderr(io.StringIO()):
        env.interact(m, max_tool_hops=8)
    if sum(1 for x in eval_predicates(env.export_trace_dict()) if x['predicate'] == 'EXFILTRATION') > 0:
        fired += 1
print(f"re-fire check: {fired}/3 returned candidates fire EXFIL")
print("SMOKE:", "PASS" if (len(cands) >= 3 and fired >= 2 and len(hosts) >= 3) else "FAIL", flush=True)
