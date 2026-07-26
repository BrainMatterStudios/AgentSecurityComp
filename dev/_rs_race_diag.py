"""Local faithful-engine diagnostic (gpt-oss GGUF, real SDK path).
Answers:
 (1) Which _RS_TEMPLATES does the tetsutani-style race SELECT on gpt-oss?
     -> does the Harmony forge (inj_close/inj_commentary) win on eff_cost = med_lat/fire_rate?
 (2) hops=1 vs hops=8 cost for the winner -> empirical REPLAY_COST_COEF.
 (3) dual-post (K=2 forge) raw-per-second vs single-post forge -> is the bandit worth it?
Only RELATIVE orderings/ratios transfer to Kaggle (wall-time does not).
"""
import sys, time, contextlib, io, statistics
sys.path.insert(0, 'comp'); sys.path.insert(0, '.'); sys.path.insert(0, 'dev')
from pathlib import Path
from aicomp_sdk.agents.gpt_oss_agent import GPTOSSAgent, build_gpt_oss_backend_config
from aicomp_sdk.agents.hf_chat_template.backends.llama_cpp import LlamaCppChatTemplateBackend
from aicomp_sdk.core.env.sandbox import SandboxEnv
from aicomp_sdk.guardrails.optimal import Guardrail as Optimal
from aicomp_sdk.core.predicates import eval_predicates
import attack

GGUF = "models/gpt-oss-20b-Q4_K_M.gguf"
FIX = Path('comp') / 'aicomp_sdk' / 'fixtures'
cfg = build_gpt_oss_backend_config(model_path=GGUF)
with contextlib.redirect_stderr(io.StringIO()):
    backend = LlamaCppChatTemplateBackend.from_model_path(
        model_path=GGUF, config=cfg, n_ctx=8192, n_gpu_layers=-1, verbose=False)
agent = GPTOSSAgent(backend=backend)


def measure(msg, seed, hops):
    env = SandboxEnv(seed=seed, fixtures_dir=FIX, agent=agent, guardrail=Optimal()); env.reset()
    t0 = time.time()
    with contextlib.redirect_stderr(io.StringIO()):
        env.interact(msg, max_tool_hops=hops)
    dt = time.time() - t0
    n = sum(1 for x in eval_predicates(env.export_trace_dict()) if x['predicate'] == 'EXFILTRATION')
    return n, dt


MARKER = attack.EXFIL_PAYLOAD  # "diag=SECRET_MARKER"
TMPLS = attack._RS_TEMPLATES
def rsurl(i): return attack._rs_url(i)

# ---- warmup (discard) ----
print("warming up...", flush=True)
measure(TMPLS[0][1].format(m=MARKER, u=rsurl(999000)), 7, 8)

# ---- (1) race the 5 templates at hops=8 ----
SEEDS = [1, 2, 3, 4, 5]
print("\n=== (1) RS TEMPLATE RACE on gpt-oss (hops=8) ===")
results = {}
hi = 900100
for ti, (name, tpl) in enumerate(TMPLS):
    lats, fires = [], 0
    for s in SEEDS:
        n, dt = measure(tpl.format(m=MARKER, u=rsurl(hi)), s, 8); hi += 1
        lats.append(dt); fires += (1 if n > 0 else 0)
    med = statistics.median(lats)
    fr = fires / len(SEEDS)
    eff = med / fr if fr > 0 else float('inf')
    results[ti] = (name, med, fr, eff)
    print(f"  [{ti}] {name:15s} med={med:5.2f}s fire={fr:.2f} eff_cost={eff:6.2f}  lats={[round(x,1) for x in lats]}")

fireable = {ti: v for ti, v in results.items() if v[2] >= 0.2}
sel = min(fireable, key=lambda ti: fireable[ti][3]) if fireable else 0
print(f"  -> SELECTED: [{sel}] {results[sel][0]}  (lowest eff_cost among fire>=0.2)")
forge_ids = [i for i, (n, *_ ) in enumerate([(t[0],) for t in TMPLS]) if TMPLS[i][0] in ('inj_close', 'inj_commentary')]
print(f"  forge template ids = {forge_ids}; selected is {'a FORGE' if sel in forge_ids else 'NOT a forge (BAD)'}")

# ---- (2) hops=1 vs hops=8 for the selected template -> COEF ----
print("\n=== (2) hops=1 vs hops=8 for selected template -> REPLAY_COST_COEF ===")
sel_tpl = TMPLS[sel][1]
l1, l8 = [], []
for s in SEEDS:
    _, d1 = measure(sel_tpl.format(m=MARKER, u=rsurl(hi)), s, 1); hi += 1
    _, d8 = measure(sel_tpl.format(m=MARKER, u=rsurl(hi)), s, 8); hi += 1
    l1.append(d1); l8.append(d8)
m1, m8 = statistics.median(l1), statistics.median(l8)
print(f"  hops1 med={m1:.2f}s  hops8 med={m8:.2f}s  COEF(h8/h1)={m8/m1:.2f}")

# ---- (3) dual-post (K=2 forge) raw/second vs single-post forge ----
print("\n=== (3) DUAL-POST (K=2 forge) vs SINGLE-POST forge: raw per replay-second ===")
alg = attack.AttackAlgorithm()
def single_forge(i): return attack._p_preclose(MARKER, alg._k1_url(i))
def dual_forge(i):    return attack._p_forge_multipost(MARKER, alg._k1_urls_multi(i, 2))
def trip_forge(i):    return attack._p_forge_multipost(MARKER, alg._k1_urls_multi(i, 3))

for label, fn, k in [("single", single_forge, 1), ("dual K2", dual_forge, 2), ("trip K3", trip_forge, 3)]:
    posts, secs = [], []
    for s in SEEDS:
        n, dt = measure(fn(hi), s, 8); hi += 1
        posts.append(n); secs.append(dt)
    avg_posts = sum(posts) / len(posts)
    med_s = statistics.median(secs)
    raw = 16 * avg_posts + 2  # one cell/finding
    print(f"  {label:9s}: posts={posts} avg={avg_posts:.2f} med_s={med_s:5.2f}  raw/cand={raw:5.1f}  raw/sec={raw/med_s:5.2f}")
print("\n(raw/sec is the deciding metric: higher => that arm fills a higher row within 9000s)")
