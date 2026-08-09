#!/usr/bin/env python3
"""L24 — probe the rerun's TRUE single-post capacity (bypass the conservative ledger).
L23 fixed-N K8 revealed the rerun scores PARTIAL + COMPLETES (no void) and caps at
~1176 posts; our single-post ledger sizes only ~985. So forcing single-post past the
ledger may access ~20% more capacity. gpt-only rungs isolate the row; both-boards rungs
are the banked-improvement shot."""
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
BASE = {"JED_REPLAY_SAFE": 1, "JED_EXFIL_PAYLOAD": "SECRET_MARKER", "JED_RS_TEMPLATES": "5,6", "JED_RS_REPS": 3}
def cc(s): return {"cell_type":"code","metadata":{},"execution_count":None,"outputs":[],"source":s}
def env_cell(env, note):
    return "\n".join(["import os"] + ["os.environ[%r]=%r" % (k, str(v)) for k,v in env.items()] + ["print(%r)" % note]) + "\n"
RUNGS = [
    ("submission_kernel_l24_base", "ahmedmobasher86/jed-public-pt-safe", "jed public pt safe",
     {**BASE, "JED_RS_ONLY":"gpt", "JED_RS_FRAC":97}, "L24 gpt-only LEDGER single (control baseline)"),
    ("submission_kernel_l24_fp4_600", "ahmedmobasher86/jed-public-pt-probe", "jed public pt probe",
     {**BASE, "JED_RS_FIXED_N":600, "JED_RS_FORGE_PLAN":4}, "L24 both-boards FORGE-PLAN n=4 N=600 (dimong4 commitment-forge; 134 attempt)"),
    ("submission_kernel_l24_fp4_900", "ahmedmobasher86/jed-public-k1nx-1000", "jed public k1nx 1000",
     {**BASE, "JED_RS_FIXED_N":900, "JED_RS_FORGE_PLAN":4}, "L24 both-boards FORGE-PLAN n=4 N=900 (fill to wall)"),
    ("submission_kernel_l24_fp6_600", "ahmedmobasher86/jed-public-k1nx-1200", "jed public k1nx 1200",
     {**BASE, "JED_RS_FIXED_N":600, "JED_RS_FORGE_PLAN":6}, "L24 both-boards FORGE-PLAN n=6 N=600 (more posts/cand)"),
    ("submission_kernel_l24_fp4_gpt", "ahmedmobasher86/jed-public-k1nx-800", "jed public k1nx 800",
     {**BASE, "JED_RS_ONLY":"gpt", "JED_RS_FIXED_N":600, "JED_RS_FORGE_PLAN":4}, "L24 gpt-only FORGE-PLAN n=4 N=600 (isolate gpt row)"),
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
