"""Build L9 kernels. Combines the confirmed decode optimum (gpt=close_ok idx5,
gemma=terse_ok idx6 — the cheapest firing templates per board, race self-routes)
with the packing-overhead lever. All rungs bare SECRET_MARKER + FRAC97 (except
last). Re-embeds current attack.py; reuses slugs.
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
# POOL {close_ok, terse_ok} = confirmed cheapest firing per board (gpt+gemma both
# route to close_ok; terse_ok is the safe fallback). PACKING K-SCALING curve is the
# experiment: K=1 baseline vs K=2/4/8/16 measures how much the per-candidate
# build_attack_env overhead amortizes. Void-safe (degrades to single-post per board).
RUNGS = [
    ("submission_kernel_l9_k1", "ahmedmobasher86/jed-public-pt-safe", "jed public pt safe",
     {**BASE, "JED_RS_FRAC": 97},
     "L9 K=1 baseline single-post FRAC=97 pool{close_ok,terse_ok} (~87 canary)"),
    ("submission_kernel_l9_k2", "ahmedmobasher86/jed-public-pt-probe", "jed public pt probe",
     {**BASE, "JED_RS_FRAC": 97, "JED_RS_PACK": 2},
     "L9 PACK K=2 FRAC=97 (overhead amortization curve)"),
    ("submission_kernel_l9_k4", "ahmedmobasher86/jed-public-k1nx-1000", "jed public k1nx 1000",
     {**BASE, "JED_RS_FRAC": 97, "JED_RS_PACK": 4},
     "L9 PACK K=4 FRAC=97 (overhead amortization curve)"),
    ("submission_kernel_l9_k8", "ahmedmobasher86/jed-public-k1nx-1200", "jed public k1nx 1200",
     {**BASE, "JED_RS_FRAC": 97, "JED_RS_PACK": 8},
     "L9 PACK K=8 FRAC=97 (overhead amortization curve)"),
    ("submission_kernel_l9_k16", "ahmedmobasher86/jed-public-k1nx-800", "jed public k1nx 800",
     {**BASE, "JED_RS_FRAC": 95, "JED_RS_PACK": 16},
     "L9 PACK K=16 FRAC=95 (max amortization, safer FRAC)"),
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
        print(f"built {d} -> {slug}  FRAC={env['JED_RS_FRAC']} pool={env.get('JED_RS_TEMPLATES','ALL')} pack={env.get('JED_RS_PACK',1)}")


if __name__ == "__main__":
    main()
