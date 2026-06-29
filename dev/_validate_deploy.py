"""End-to-end check of the DEPLOYED config: emit real candidates from attack.py
(JED_K1_PROMPT=6, .com hosts) and run each through the EXACT competition model.
Confirms fires + measures per-candidate tokens (the cal_t/void driver)."""
import os, sys
sys.path.insert(0, 'comp'); sys.path.insert(0, '.'); sys.path.insert(0, 'dev')
for k in list(os.environ):
    if k.startswith("JED_"):
        os.environ.pop(k, None)
os.environ.update({"JED_K1_SHORT": "1", "JED_K1_ADAPTIVE": "0", "JED_K1_PROMPT": "6", "JED_MAX_CANDIDATES": "8"})
import attack
import local_calt_bench as b

cands = attack.AttackAlgorithm()._run_k1_short(env=None, budget=9000.0, max_hops=8)
print("sample emitted message:", repr(cands[0].user_messages[0]))
print(f"\n{'idx':>3} {'fires':5} {'tokens':>6}")
toks = []
for i, c in enumerate(cands):
    msg = c.user_messages[0]
    tot, g, fired, _ = b.one_candidate(msg)
    toks.append(tot)
    print(f"{i:>3} {str(fired):5} {tot:>6}", flush=True)
print(f"\nfires_all={all(b.one_candidate(c.user_messages[0])[2] for c in cands[:1])}  "
      f"tokens: min={min(toks)} max={max(toks)} mean={sum(toks)//len(toks)}")
print(f"vs k1_short=183 -> N multiplier ~{183/(sum(toks)/len(toks)):.2f}x  (boundary ~450 -> ~{int(450*183/(sum(toks)/len(toks)))})")
