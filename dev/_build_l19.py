#!/usr/bin/env python3
"""Build L19 ultra-lean Hermes kernels targeting 112+ public leaderboard score.

Constructs 5 ladder rungs testing target candidate bounds N=1100, N=1180,
N=1250 (112.5 target), N=1320, plus one safe anchor baseline.
"""
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATTACK_B64 = base64.b64encode((ROOT / "attack.py").read_bytes()).decode()

CELL0 = (
    "import sys,glob,os\n"
    "for p in glob.glob('/kaggle/input/**/kaggle_evaluation',recursive=True):\n"
    " r=os.path.dirname(p)\n"
    " if os.path.isdir(os.path.join(r,'aicomp_sdk')): sys.path.insert(0,r); break\n"
    "sys.path.insert(0,'/kaggle/working'); print('setup')\n"
)
CELL2 = (
    "import base64\n"
    "open('/kaggle/working/attack.py','wb').write(base64.b64decode('%s'))\n" % ATTACK_B64
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
    "if not sub.exists(): sub.write_text('Id,Score\\ngpt_oss_public,0.0\\ngpt_oss_private,0.0\\ngemma_public,0.0\\ngemma_private,0.0\\n')\n"
)


def env_cell(env, note):
    lines = ["import os"]
    lines.extend("os.environ[%r]=%r" % (k, str(v)) for k, v in env.items())
    lines.append("print(%r)" % note)
    return "\n".join(lines) + "\n"


def cc(src):
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": src,
    }


LEAN_BASE = {
    "JED_LEAN_HERMES": 1,
    "JED_HERMES_MARGIN_MULT": "1.12",
    "JED_HERMES_MARGIN_S": "25.0",
}

RUNGS = [
    (
        "submission_kernel_l19_anchor",
        "ahmedmobasher86/jed-public-pt-safe",
        "jed public pt safe",
        {
            "JED_REPLAY_SAFE": 1,
            "JED_EXFIL_PAYLOAD": "SECRET_MARKER",
            "JED_RS_TEMPLATES": "5,6",
            "JED_RS_FRAC": 97,
            "JED_RS_REPS": 3,
        },
        "L19 ANCHOR baseline single-post FRAC97 (~89.5 canary)",
    ),
    (
        "submission_kernel_l19_n1100",
        "ahmedmobasher86/jed-public-pt-probe",
        "jed public pt probe",
        {**LEAN_BASE, "JED_HERMES_TARGET_N": 1100},
        "L19 LEAN HERMES N=1100 (conservative ~99.0 target)",
    ),
    (
        "submission_kernel_l19_n1180",
        "ahmedmobasher86/jed-public-k1nx-1000",
        "jed public k1nx 1000",
        {**LEAN_BASE, "JED_HERMES_TARGET_N": 1180},
        "L19 LEAN HERMES N=1180 (moderate ~106.2 target)",
    ),
    (
        "submission_kernel_l19_n1250",
        "ahmedmobasher86/jed-public-k1nx-1200",
        "jed public k1nx 1200",
        {**LEAN_BASE, "JED_HERMES_TARGET_N": 1250},
        "L19 LEAN HERMES N=1250 (PRIMARY TOP-BOARD TARGET ~112.5)",
    ),
    (
        "submission_kernel_l19_n1320",
        "ahmedmobasher86/jed-public-k1nx-800",
        "jed public k1nx 800",
        {**LEAN_BASE, "JED_HERMES_TARGET_N": 1320},
        "L19 LEAN HERMES N=1320 (stretch ~118.8 target)",
    ),
]


def main():
    for d, slug, title, env, note in RUNGS:
        dd = ROOT / d
        dd.mkdir(exist_ok=True)
        nb = {
            "cells": [cc(CELL0), cc(env_cell(env, note)), cc(CELL2), cc(CELL3)],
            "metadata": {
                "kernelspec": {
                    "language": "python",
                    "name": "python3",
                    "display_name": "Python 3",
                }
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }
        (dd / "k.ipynb").write_text(json.dumps(nb))
        meta = {
            "id": slug,
            "title": title,
            "code_file": "k.ipynb",
            "language": "python",
            "kernel_type": "notebook",
            "is_private": True,
            "enable_gpu": False,
            "enable_internet": False,
            "competition_sources": ["ai-agent-security-multi-step-tool-attacks"],
        }
        (dd / "kernel-metadata.json").write_text(json.dumps(meta, indent=2))
        print(f"built {d} -> {slug}  {note}")


if __name__ == "__main__":
    main()
