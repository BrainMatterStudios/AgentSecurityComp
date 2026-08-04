"""TRACK 2, step 1 — RIGOROUS per-candidate cost decomposition on the faithful engine
(gpt-oss Q4 via llama.cpp). Question: where does per-candidate replay time go, and does
multi-message PACKING (amortize the ~9MB env-build across K idx13 posts in ONE candidate)
beat single-post? The "packing is dead" verdict was transformers-measured; re-check here.

CONTROLS: warmup discarded, N replications per config, report mean+/-std. This is a LOCAL
measurement -> a HYPOTHESIS. Wall-time does NOT transfer to Kaggle; only the RATIO
(packing raw/s vs single raw/s) is suggestive, and any winner must be Kaggle-validated.
"""
import sys, time, contextlib, io, statistics as st
sys.path.insert(0, 'comp'); sys.path.insert(0, '.')
from pathlib import Path
import attack
from aicomp_sdk.agents.gpt_oss_agent import GPTOSSAgent, build_gpt_oss_backend_config
from aicomp_sdk.agents.hf_chat_template.backends.llama_cpp import LlamaCppChatTemplateBackend
from aicomp_sdk.core.env.sandbox import SandboxEnv
from aicomp_sdk.guardrails.optimal import Guardrail as Optimal
from aicomp_sdk.core.predicates import eval_predicates

GGUF = "models/gpt-oss-20b-Q4_K_M.gguf"; FIX = Path('comp')/'aicomp_sdk'/'fixtures'
T = attack.EXFIL_PAYLOAD; HOPS = 8
idx13 = attack.K1_PROMPTS[13]
alg = attack.AttackAlgorithm(config={})

print("loading gpt-oss (llama.cpp/Metal)...", flush=True)
cfg = build_gpt_oss_backend_config(model_path=GGUF)
with contextlib.redirect_stderr(io.StringIO()):
    be = LlamaCppChatTemplateBackend.from_model_path(model_path=GGUF, config=cfg, n_ctx=8192, n_gpu_layers=-1, verbose=False)
ag = GPTOSSAgent(backend=be)

def envbuild_only():
    """time to build+reset a fresh env (the ~9MB fixture parse), no interact."""
    t0 = time.time()
    env = SandboxEnv(seed=123, fixtures_dir=FIX, agent=ag, guardrail=Optimal()); env.reset()
    return time.time() - t0

def candidate(msgs):
    """one candidate = 1 env-build + interact per user-message; return (time, posts)."""
    env = SandboxEnv(seed=123, fixtures_dir=FIX, agent=ag, guardrail=Optimal()); env.reset()
    t0 = time.time()
    with contextlib.redirect_stderr(io.StringIO()):
        for m in msgs:
            env.interact(m, max_tool_hops=HOPS)
    dt = time.time() - t0
    posts = sum(1 for x in eval_predicates(env.export_trace_dict()) if x['predicate'] == 'EXFILTRATION')
    return dt, posts

def stat(xs): return f"{st.mean(xs):.2f}+/-{(st.pstdev(xs) if len(xs)>1 else 0):.2f}"

# warmup (discard) — 2 throwaway candidates so KV/schema prefix + caches are hot
print("warming up...", flush=True)
for _ in range(2): candidate([idx13(T, alg._k1_url(999))])

REPS = 4
print(f"\n=== cost decomposition (gpt-oss idx13, hops={HOPS}, {REPS} reps warm) ===", flush=True)
eb = [envbuild_only() for _ in range(REPS)]
print(f"env-build+reset ALONE (9MB parse): {stat(eb)} s", flush=True)

# packing sweep: K idx13 posts in ONE candidate (K unique urls) vs single-post baseline
base = 0
for K in (1, 2, 4, 8, 16):
    dts, pss = [], []
    for r in range(REPS):
        msgs = [idx13(T, alg._k1_url(1000 + r*100 + i)) for i in range(K)]
        dt, posts = candidate(msgs); dts.append(dt); pss.append(posts)
    raw = 16*st.mean(pss) + 2           # K posts -> K*16 + 2 (one cell per candidate)
    rps = raw / st.mean(dts)            # raw per second (the 9000s-budget metric)
    per_post = st.mean(dts)/max(1e-9, st.mean(pss))
    if K == 1: base = rps
    print(f"K={K:2d}: time={stat(dts)}s posts={st.mean(pss):.2f}/{K} raw/s={rps:5.2f} "
          f"({rps/base:.2f}x vs single) s/post={per_post:.2f}", flush=True)
print("\nNOTE: LOCAL hypothesis only. Packing helps IFF env-build is a large fixed fraction AND"
      "\ncontext-growth doesn't eat the savings. Any K>1 winner must be Kaggle-validated.", flush=True)
print("done", flush=True)
