"""Build L12 kernels. Multi-Endpoint Single-Message Prompting (K=4, 5, 6 endpoints/msg).
All rungs use JED_REPLAY_SAFE=1 with exact SECRET_MARKER payload.
- Rung 1: Single-Post Control (FRAC=97, ENDPOINTS=1, pool{close_ok, terse_ok}) -> ~89.6 canary
- Rung 2: Multi-Endpoint K=4 (FRAC=95, ENDPOINTS=4) -> Target ~95-100
- Rung 3: Multi-Endpoint K=5 (FRAC=95, ENDPOINTS=5) -> Target ~105-110
- Rung 4: Multi-Endpoint K=6 (FRAC=95, ENDPOINTS=6) -> Target ~110-115
- Rung 5: Multi-Endpoint K=5 Squeeze (FRAC=96, ENDPOINTS=5, MAX_CAND=280) -> Target ~115+
"""
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
CELL3 = ("import os\n"
         "from pathlib import Path\n"
         "sub=Path('/kaggle/working/submission.csv')\n"
         "try:\n"
         " import kaggle_evaluation.jed_attack_134815.jed_attack_inference_server as srv\n"
         " srv.JEDAttackInferenceServer().serve()\n"
         "except Exception as e:\n"
         " if os.getenv('KAGGLE_IS_COMPETITION_RERUN') is not None: raise\n"
         " print('skip',repr(e)[:60])\n"
         "if not sub.exists(): sub.write_text('Id,Score\\ngpt_oss_public,0.0\\ngpt_oss_private,0.0\\ngemma_public,0.0\\ngemma_private,0.0\\n')\n")


def env_cell(env, note):
    lines = ["import os"] + ["os.environ[%r]=%r" % (k, str(v)) for k, v in env.items()] + ["print(%r)" % note]
    return "\n".join(lines) + "\n"


def cc(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": src}


BASE = {"JED_REPLAY_SAFE": 1, "JED_EXFIL_PAYLOAD": "SECRET_MARKER", "JED_RS_TEMPLATES": "5,6"}
RUNGS = [
    ("submission_kernel_l12_anchor", "ahmedmobasher86/jed-public-pt-safe", "jed public pt safe",
     {**BASE, "JED_RS_FRAC": 97, "JED_RS_ENDPOINTS": 1},
     "L12 ANCHOR: Single-post control FRAC=97 ENDPOINTS=1 pool{close_ok,terse_ok} (~89.6 canary)"),
    ("submission_kernel_l12_k4", "ahmedmobasher86/jed-public-pt-probe", "jed public pt probe",
     {**BASE, "JED_RS_FRAC": 95, "JED_RS_ENDPOINTS": 4},
     "L12 MULTI-ENDPOINT: K=4 FRAC=95 (4 posts/msg -> ~95-100)"),
    ("submission_kernel_l12_k5", "ahmedmobasher86/jed-public-k1nx-1000", "jed public k1nx 1000",
     {**BASE, "JED_RS_FRAC": 95, "JED_RS_ENDPOINTS": 5},
     "L12 MULTI-ENDPOINT: K=5 FRAC=95 (5 posts/msg -> ~105-110)"),
    ("submission_kernel_l12_k6", "ahmedmobasher86/jed-public-k1nx-1200", "jed public k1nx 1200",
     {**BASE, "JED_RS_FRAC": 95, "JED_RS_ENDPOINTS": 6},
     "L12 MULTI-ENDPOINT: K=6 FRAC=95 (6 posts/msg -> ~110-115)"),
    ("submission_kernel_l12_k5sqz", "ahmedmobasher86/jed-public-k1nx-800", "jed public k1nx 800",
     {**BASE, "JED_RS_FRAC": 96, "JED_RS_ENDPOINTS": 5, "JED_RS_MAX_CAND": 280},
     "L12 SQUEEZE: K=5 FRAC=96 MAX_CAND=280 -> ~115+"),
]


def main():
    for d, slug, title, env, note in RUNGS:
        dd = ROOT / d
        dd.mkdir(exist_ok=True)
        nb = {"cells": [cc(CELL0), cc(env_cell(env, note)), cc(CELL2), cc(CELL3)],
              "metadata": {"kernelspec": {"language": "python", "name": "python3", "display_name": "Python 3"}},
              "nbformat": 4, "nbformat_minor": 5}
        (dd / "k.ipynb").write_text(json.dumps(nb))
        meta = {"id": slug, "title": title, "code_file": "k.ipynb", "language": "python",
                "kernel_type": "notebook", "is_private": True, "enable_gpu": True,
                "machine_shape": "NvidiaTeslaT4", "enable_internet": False,
                "competition_sources": ["ai-agent-security-multi-step-tool-attacks"]}
        (dd / "kernel-metadata.json").write_text(json.dumps(meta, indent=2))
        print(f"built {d} -> {slug}  FRAC={env.get('JED_RS_FRAC')} ENDPOINTS={env.get('JED_RS_ENDPOINTS')} pool={env.get('JED_RS_TEMPLATES')}")


if __name__ == "__main__":
    main()
