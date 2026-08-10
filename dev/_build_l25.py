#!/usr/bin/env python3
"""L25 — the DUAL-FORGE crown shot (beat-dimong4). L24 proved: (a) the gpt commitment-
forge is board-capped ~47.85 (= hoppack, no edge); (b) running the gpt forge on BOTH
boards POISONS the gemma row (both-forge 72.785 < both-single 82.35). The fix = route
gpt->_p_forge_plan, gemma->_gemma_forge_msg (its NATIVE clean forge) in one run
(JED_RS_DUAL_FORGE=1). This ladder banks the crown shot AND decomposes it: does the
gemma forge actually beat gemma single ON THE BOARD (offline it fires 3, but gpt's forge
was throttled offline->board too)? Reuses the 5 L24 slugs (version bump)."""
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
    ("submission_kernel_l25_single", "ahmedmobasher86/jed-public-pt-safe", "jed public pt safe",
     {**BASE, "JED_RS_FIXED_N":600},
     "L25 both-boards SINGLE N=600 (clean baseline the dual-forge must beat)"),
    ("submission_kernel_l25_gemforge_k4", "ahmedmobasher86/jed-public-pt-probe", "jed public pt probe",
     {**BASE, "JED_RS_DUAL_FORGE":1, "JED_RS_ONLY":"gemma", "JED_RS_FIXED_N":600, "JED_GEMMA_FORGE_K":4},
     "L25 gemma-only FORGE isolate k=4 N=600 (gemma-native-forge row)"),
    ("submission_kernel_l25_gemsingle", "ahmedmobasher86/jed-public-k1nx-1000", "jed public k1nx 1000",
     {**BASE, "JED_RS_ONLY":"gemma", "JED_RS_FIXED_N":600},
     "L25 gemma-only SINGLE isolate N=600 (gemma baseline; forge-vs-single A/B)"),
    ("submission_kernel_l25_dual_k4", "ahmedmobasher86/jed-public-k1nx-1200", "jed public k1nx 1200",
     {**BASE, "JED_RS_DUAL_FORGE":1, "JED_RS_FIXED_N":600, "JED_RS_FORGE_PLAN":4, "JED_GEMMA_FORGE_K":4},
     "L25 both-boards DUAL-FORGE n=4 k=4 N=600 (CROWN: gpt forge + gemma native forge)"),
    ("submission_kernel_l25_dual_k3", "ahmedmobasher86/jed-public-k1nx-800", "jed public k1nx 800",
     {**BASE, "JED_RS_DUAL_FORGE":1, "JED_RS_FIXED_N":600, "JED_RS_FORGE_PLAN":4, "JED_GEMMA_FORGE_K":3},
     "L25 both-boards DUAL-FORGE n=4 k=3 N=600 (crown A/B: gemma k=3 + variance re-roll)"),
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
