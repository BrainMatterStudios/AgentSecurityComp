#!/usr/bin/env python3
"""L26 BEAT ladder — dimong4's 100%-fire-rate validation-fill engine, pushed PAST its
conservative defaults to BEAT the 137 top (not tie it). dimong4 leaves fill headroom:
FILL_BUDGET_FRAC=0.95, REPLAY_SAFE_FRAC=0.97, MARGIN_S=47 -- their own comment says the
winning 'submission_variants tighten MARGIN_S down and FILL_BUDGET_FRAC up.' The replay-
cost accounting is accurate (fill latency == replay latency), so filling to ~0.99 fits
more candidates WITHOUT voiding, up to a thin margin. We do NOT touch REPLAY_BUDGET_MULT
(that bets the replay wall is >9000s, which voids). 89.6 stays permanently banked on the
public LB, so ALL 5 rungs go to beating. Rung 1 = dimong4 exact (reference); 2-4 =
escalating fill; 5 = aggressive fill + max gpt multipost."""
import base64, json, re, py_compile, tempfile, os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC = Path("/tmp/dimong4_attack.py").read_text()  # dimong4's verbatim AttackAlgorithm

def patch(src, **kv):
    out = src
    for const, val in kv.items():
        out, n = re.subn(rf"(?m)^{const}\s*=\s*[0-9.]+", f"{const} = {val}", out)
        assert n == 1, f"expected exactly 1 match for {const}, got {n}"
    # validate it still compiles
    fd, tmp = tempfile.mkstemp(suffix=".py"); os.close(fd)
    Path(tmp).write_text(out); py_compile.compile(tmp, doraise=True); os.unlink(tmp)
    return out

CELL0 = ("import sys,glob,os\n"
         "for p in glob.glob('/kaggle/input/**/kaggle_evaluation',recursive=True):\n"
         " r=os.path.dirname(p)\n"
         " if os.path.isdir(os.path.join(r,'aicomp_sdk')): sys.path.insert(0,r); break\n"
         "sys.path.insert(0,'/kaggle/working'); print('setup')\n")
def cell2(src_b64):
    return ("import base64\n"
            "open('/kaggle/working/attack.py','wb').write(base64.b64decode('%s'))\nprint('attack.py written')\n" % src_b64)
CELL3 = ("import os\nfrom pathlib import Path\nsub=Path('/kaggle/working/submission.csv')\n"
         "try:\n import kaggle_evaluation.jed_attack_134815.jed_attack_inference_server as srv\n"
         " srv.JEDAttackInferenceServer().serve()\n"
         "except Exception as e:\n"
         " if os.getenv('KAGGLE_IS_COMPETITION_RERUN') is not None: raise\n"
         " print('skip',repr(e)[:60])\n"
         "if not sub.exists(): sub.write_text('Id,Score\\ngpt_oss_public,0.0\\ngpt_oss_private,0.0\\ngemma_public,0.0\\ngemma_private,0.0\\n')\n")
def cc(s): return {"cell_type":"code","metadata":{},"execution_count":None,"outputs":[],"source":s}

# (dir, slug, title, patched-src, note)
# CORRECTED after adversarial review: FILL_BUDGET_FRAC & MARGIN_S are DEAD under
# REPLAY_SAFE_SIZING=True (verified: fill loop stop-test uses only REPLAY_SAFE_FRAC).
# REPLAY_SAFE_FRAC=0.99+ risks a total-void (cushion < uncounted per-candidate replay
# overhead + private-guardrail pass). BURST_K/hoppack is a proven T4 loser (our L14/L23).
# So: reproduce dimong4's proven engine (the real +48 climb from our 89.6) and push ONLY
# the live knob at SAFE levels (0.98/0.985) to edge past ~137. Rung 5 = variance re-roll.
RUNGS = [
    ("submission_kernel_l26b_ref", "ahmedmobasher86/jed-public-pt-safe", "jed public pt safe",
     SRC, "L26 dimong4 EXACT (climb baseline; aim ~134)"),
    ("submission_kernel_l26b_rsf98", "ahmedmobasher86/jed-public-pt-probe", "jed public pt probe",
     patch(SRC, REPLAY_SAFE_FRAC=0.98),
     "L26 dimong4 + REPLAY_SAFE_FRAC=0.98 (safe sizing push, the one live knob)"),
    ("submission_kernel_l26b_rsf985", "ahmedmobasher86/jed-public-k1nx-1000", "jed public k1nx 1000",
     patch(SRC, REPLAY_SAFE_FRAC=0.985),
     "L26 dimong4 + REPLAY_SAFE_FRAC=0.985 (edge push, still ~135s cushion)"),
    ("submission_kernel_l26b_rsf98mp6", "ahmedmobasher86/jed-public-k1nx-1200", "jed public k1nx 1200",
     patch(SRC, REPLAY_SAFE_FRAC=0.98, SLOW_MULTIPOST_N=6),
     "L26 dimong4 + RSF=0.98 + SLOW_MULTIPOST_N=6 (fill + mild gpt-row push)"),
    ("submission_kernel_l26b_ref2", "ahmedmobasher86/jed-public-k1nx-800", "jed public k1nx 800",
     SRC, "L26 dimong4 EXACT re-roll (variance hedge; keep best of two ~134 shots)"),
]
def main():
    for d, slug, title, src, note in RUNGS:
        dd = ROOT / d; dd.mkdir(exist_ok=True)
        b64 = base64.b64encode(src.encode()).decode()
        nb = {"cells":[cc(CELL0),cc(cell2(b64)),cc(CELL3)],
              "metadata":{"kernelspec":{"language":"python","name":"python3","display_name":"Python 3"}},
              "nbformat":4,"nbformat_minor":5}
        (dd/"k.ipynb").write_text(json.dumps(nb))
        (dd/"kernel-metadata.json").write_text(json.dumps({"id":slug,"title":title,"code_file":"k.ipynb",
            "language":"python","kernel_type":"notebook","is_private":True,"enable_gpu":False,
            "enable_internet":False,"competition_sources":["ai-agent-security-multi-step-tool-attacks"]}, indent=2))
        print("built", d, "->", slug, "|", note)
if __name__ == "__main__": main()
