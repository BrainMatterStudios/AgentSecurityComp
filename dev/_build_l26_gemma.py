#!/usr/bin/env python3
"""L26 gemma-headroom rungs (3-5). The Fable hunt + our OWN L25 data (gemma-forge isolate
34 > gemma-single 27 at N=600) point at the gemma FAST row as the only real headroom past
dimong4's ~134: the FILLED gemma continuation forge fires >1 post on the board (unlike the
dead empty-close hoppack). We only ever tested it at a crippled fixed N=600. These rungs run
the decisive forge-vs-single A/B at HIGH N (isolated gemma row) to see if the forge keeps
beating single as N scales -- the signal that the gemma row can be pushed toward its ~180 cap.
Rungs 1-2 (dimong4 exact + re-roll) stay as-is to bank the safe ~134 climb."""
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
    # gemma-FORGE isolate at high N -- does the forge row scale?
    ("submission_kernel_l26g_forge900", "ahmedmobasher86/jed-public-pt-probe", "jed public pt probe",
     {**BASE, "JED_RS_DUAL_FORGE":1, "JED_RS_ONLY":"gemma", "JED_RS_FIXED_N":900, "JED_GEMMA_FORGE_K":4},
     "L26 gemma-FORGE isolate k=4 N=900 (headroom probe)"),
    # gemma-SINGLE isolate at the SAME N -- the decisive control (forge vs single at matched high N)
    ("submission_kernel_l26g_single900", "ahmedmobasher86/jed-public-k1nx-1000", "jed public k1nx 1000",
     {**BASE, "JED_RS_ONLY":"gemma", "JED_RS_FIXED_N":900},
     "L26 gemma-SINGLE isolate N=900 (control: forge-vs-single A/B at matched N)"),
    # gemma-FORGE isolate even higher -- scaling + void boundary
    ("submission_kernel_l26g_forge1200", "ahmedmobasher86/jed-public-k1nx-1200", "jed public k1nx 1200",
     {**BASE, "JED_RS_DUAL_FORGE":1, "JED_RS_ONLY":"gemma", "JED_RS_FIXED_N":1200, "JED_GEMMA_FORGE_K":4},
     "L26 gemma-FORGE isolate k=4 N=1200 (scaling / void-boundary probe)"),
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
