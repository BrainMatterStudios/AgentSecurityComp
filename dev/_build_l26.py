#!/usr/bin/env python3
"""L26 — the decisive frontier-reproduction + sizing ladder. L25 showed the dual-forge
(82) < banked single (89.6): we forged the FAST gemma row (wrong; should be wide single)
and fixed N=600 (under-sized). dimong4's own code says the gpt multipost is only ~1.1x —
the frontier's 134 is SIZING (probe hops=1, bet replay headroom -> ~2x candidates) +
asymmetric routing (gpt slow->multipost4, gemma fast->wide single) + MEAN aggregation.
Rung 1 (built separately) runs dimong4's EXACT kernel to test reproducibility. Rungs 2-5
here re-bank 89.6 and sweep OUR engine's sizing. Reuses the 5 slugs (version bump)."""
import base64, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ATTACK_B64 = base64.b64encode((ROOT / "attack.py").read_bytes()).decode()
CELL0 = ("import sys,glob,os\n"
         "for p in glob.glob('/kaggle/input/**/kaggle_evaluation',recursive=True):\n"
         " r=os.path.dirname(p)\n"
         " if os.path.isdir(os.path.join(r,'aicomp_sdk')): sys.path.insert(0,r); break\n"
         "sys.path.insert(0,'/kaggle/working'); print('setup')\n")
CELL2 = ("import base64\n"
         "open('/kaggle/working/attack.py','wb').write(base64.b64decode('%s'))\n" % ATTACK_B64)
CELL3 = ("import os\nfrom pathlib import Path\nsub=Path('/kaggle/working/submission.csv')\n"
         "try:\n import kaggle_evaluation.jed_attack_134815.jed_attack_inference_server as srv\n"
         " srv.JEDAttackInferenceServer().serve()\n"
         "except Exception as e:\n"
         " if os.getenv('KAGGLE_IS_COMPETITION_RERUN') is not None: raise\n"
         " print('skip',repr(e)[:60])\n"
         "if not sub.exists(): sub.write_text('Id,Score\\ngpt_oss_public,0.0\\ngpt_oss_private,0.0\\ngemma_public,0.0\\ngemma_private,0.0\\n')\n")
# BASE = adaptive single-post (NO fixed N -> the sizer self-fills the budget, the ~89.6 mechanism)
BASE = {"JED_REPLAY_SAFE": 1, "JED_EXFIL_PAYLOAD": "SECRET_MARKER", "JED_RS_TEMPLATES": "5,6", "JED_RS_REPS": 3}
def cc(s): return {"cell_type":"code","metadata":{},"execution_count":None,"outputs":[],"source":s}
def env_cell(env, note):
    return "\n".join(["import os"] + ["os.environ[%r]=%r" % (k, str(v)) for k,v in env.items()] + ["print(%r)" % note]) + "\n"
# Rungs 2-5 (rung 1 = dimong4 verbatim, built separately in submission_kernel_l26_dimong4/)
RUNGS = [
    ("submission_kernel_l26_rebank", "ahmedmobasher86/jed-public-pt-probe", "jed public pt probe",
     {**BASE, "JED_RS_FRAC":97},
     "L26 re-bank adaptive single-post FRAC97 (the ~89.6 baseline / canary)"),
    ("submission_kernel_l26_frac98", "ahmedmobasher86/jed-public-k1nx-1000", "jed public k1nx 1000",
     {**BASE, "JED_RS_FRAC":98},
     "L26 adaptive single-post FRAC98 (sizing push +1pt of budget)"),
    ("submission_kernel_l26_frac99", "ahmedmobasher86/jed-public-k1nx-1200", "jed public k1nx 1200",
     {**BASE, "JED_RS_FRAC":99},
     "L26 adaptive single-post FRAC99 (sizing boundary probe; may void gpt)"),
    ("submission_kernel_l26_split", "ahmedmobasher86/jed-public-k1nx-800", "jed public k1nx 800",
     {**BASE, "JED_RS_SPLIT":1},
     "L26 asymmetric adaptive routing JED_RS_SPLIT (gpt->hoppack2, gemma->wide single; our slow/fast analog)"),
]
def main():
    for d, slug, title, env, note in RUNGS:
        dd = ROOT / d; dd.mkdir(exist_ok=True)
        nb = {"cells":[cc(CELL0),cc(env_cell(env,note)),cc(CELL2),cc(CELL3)],
              "metadata":{"kernelspec":{"language":"python","name":"python3","display_name":"Python 3"}},
              "nbformat":4,"nbformat_minor":5}
        (dd/"k.ipynb").write_text(json.dumps(nb))
        (dd/"kernel-metadata.json").write_text(json.dumps({"id":slug,"title":title,"code_file":"k.ipynb",
            "language":"python","kernel_type":"notebook","is_private":True,"enable_gpu":False,
            "enable_internet":False,"competition_sources":["ai-agent-security-multi-step-tool-attacks"]}, indent=2))
        print("built", d, "->", slug, "|", note)
if __name__ == "__main__": main()
