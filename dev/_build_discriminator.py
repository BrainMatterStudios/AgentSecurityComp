#!/usr/bin/env python3
"""Build the mean-vs-sum discriminator submission kernel.

N=500 single-post on BOTH boards (fixed route: close_ok for gpt, terse_ok for gemma).
500 candidates is far under the replay budget, so all replay and fire (~100%), making
each public row exactly 0.09*500 = 45. Therefore the leaderboard publicScore reads:
  ~45  if aggregation is MEAN(gpt_public, gemma_public)
  ~90  if aggregation is SUM
No board-isolation (which broke at L22) and no throughput confound. Only meaningful if
the T4 full-gateway audit confirms ~100% fire first.

Writes a local kernel folder only. Does not push or submit.
"""
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATTACK_B64 = base64.b64encode((ROOT / "attack.py").read_bytes()).decode()
SLUG = "ahmedmobasher86/jed-l34-discriminator-n500"
DIRNAME = "submission_kernel_l34_discriminator_n500"

CELL0 = (
    "import sys,glob,os\n"
    "for p in glob.glob('/kaggle/input/**/kaggle_evaluation',recursive=True):\n"
    " r=os.path.dirname(p)\n"
    " if os.path.isdir(os.path.join(r,'aicomp_sdk')): sys.path.insert(0,r); break\n"
    "sys.path.insert(0,'/kaggle/working'); print('setup')\n"
)
ENV = (
    "import os\n"
    "os.environ['JED_REPLAY_SAFE']='1'\n"
    "os.environ['JED_EXFIL_PAYLOAD']='SECRET_MARKER'\n"
    "os.environ['JED_RS_TEMPLATES']='5,6'\n"
    "os.environ['JED_RS_MAX_CAND']='2000'\n"
    "os.environ['JED_RS_FIXED_ROUTE']='1'\n"
    "os.environ['JED_RS_FIXED_N']='500'\n"
    "print('discriminator N=500 both-boards single-post: mean->~45, sum->~90')\n"
)
ATT = (
    "import base64\n"
    "open('/kaggle/working/attack.py','wb').write(base64.b64decode('%s'))\n"
    "print('attack.py written')\n" % ATTACK_B64
)
CELL3 = (
    "import os\n"
    "from pathlib import Path\n"
    "sub=Path('/kaggle/working/submission.csv')\n"
    "try:\n"
    " import kaggle_evaluation.jed_attack_134815.jed_attack_inference_server as srv\n"
    " srv.JEDAttackInferenceServer().serve()\n"
    "except Exception as e:\n"
    " if os.getenv('KAGGLE_IS_COMPETITION_RERUN') is not None: raise\n"
    " print('skip',repr(e)[:60])\n"
    "if not sub.exists(): sub.write_text('Id,Score\\ngpt_oss_public,0.0\\n"
    "gpt_oss_private,0.0\\ngemma_public,0.0\\ngemma_private,0.0\\n')\n"
)


def cc(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": src}


def main():
    d = ROOT / DIRNAME
    d.mkdir(exist_ok=True)
    nb = {
        "cells": [cc(CELL0), cc(ENV), cc(ATT), cc(CELL3)],
        "metadata": {"kernelspec": {"language": "python", "name": "python3", "display_name": "Python 3"}},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    (d / "k.ipynb").write_text(json.dumps(nb))
    (d / "kernel-metadata.json").write_text(json.dumps({
        "id": SLUG,
        "title": "jed l34 discriminator n500",
        "code_file": "k.ipynb",
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": False,
        "enable_internet": False,
        "competition_sources": ["ai-agent-security-multi-step-tool-attacks"],
    }, indent=2))
    print("built", DIRNAME, "->", SLUG)


if __name__ == "__main__":
    main()
