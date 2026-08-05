#!/usr/bin/env python3
"""Build L18 hybrid reset kernels.

L18 keeps one replay-safe anchor, tests the exact locally-positive Gemma
``a.co/1..8`` forge behind a high validation gate, and includes one safer
public-style split rung. Kernels are CPU-save notebooks so GPU quota does not
block saving versions; the competition rerun still drives the remote model
servers.
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


RS_ANCHOR = {
    "JED_REPLAY_SAFE": 1,
    "JED_EXFIL_PAYLOAD": "SECRET_MARKER",
    "JED_RS_TEMPLATES": "5,6",
    "JED_RS_FRAC": 97,
    "JED_RS_REPS": 3,
}

ACO_FORGE = {
    "JED_GEMMA_FORGE": 1,
    "JED_GEMMA_FORGE_REPEAT_A_PATHS": 1,
    "JED_EXFIL_PAYLOAD": "diag=SECRET_MARKER",
    "JED_GEMMA_FORGE_K": 8,
    "JED_GEMMA_FORGE_VALIDATE": 1,
    "JED_GEMMA_FORGE_MIN_POSTS": 6,
    "JED_RS_TEMPLATES": "5,6",
    "JED_RS_FRAC": 97,
    "JED_RS_REPS": 3,
}

RUNGS = [
    (
        "submission_kernel_l18_anchor_rs97",
        "ahmedmobasher86/jed-public-pt-safe",
        "jed public pt safe",
        {**RS_ANCHOR},
        "L18 ANCHOR replay-safe FRAC97 templates 5 and 6 current baseline",
    ),
    (
        "submission_kernel_l18_aco8n60",
        "ahmedmobasher86/jed-public-pt-probe",
        "jed public pt probe",
        {**ACO_FORGE, "JED_GEMMA_FORGE_N": 60},
        "L18 ACO-FORGE exact a.co paths K8 N60 validation-gated probe",
    ),
    (
        "submission_kernel_l18_aco8n120",
        "ahmedmobasher86/jed-public-k1nx-1000",
        "jed public k1nx 1000",
        {**ACO_FORGE, "JED_GEMMA_FORGE_N": 120},
        "L18 ACO-FORGE exact a.co paths K8 N120 moderate rung",
    ),
    (
        "submission_kernel_l18_split_safe",
        "ahmedmobasher86/jed-public-k1nx-1200",
        "jed public k1nx 1200",
        {
            "JED_AGG_PROBE": 1,
            "JED_EXFIL_PAYLOAD": "diag=SECRET_MARKER",
            "JED_GPTOSS_MP_K": 4,
            "JED_GPTOSS_N": 90,
            "JED_GEMMA_N": 520,
        },
        "L18 SPLIT-SAFE gpt K4 plus gemma N520 no prompt12",
    ),
    (
        "submission_kernel_l18_aco8n230",
        "ahmedmobasher86/jed-public-k1nx-800",
        "jed public k1nx 800",
        {**ACO_FORGE, "JED_GEMMA_FORGE_N": 230},
        "L18 ACO-FORGE exact a.co paths K8 N230 single stretch",
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
