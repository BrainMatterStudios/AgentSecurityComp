#!/usr/bin/env python3
"""Build L17 kernels for the Gemma forge ladder.

L17 tests the only locally positive mechanism with headroom above the current
~89 public anchor: Gemma special-token continuation forge for multi-post
candidates, with the proven replay-safe close_ok path as the gpt fallback.
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


GF = {
    "JED_GEMMA_FORGE": 1,
    "JED_EXFIL_PAYLOAD": "diag=SECRET_MARKER",
    "JED_GEMMA_FORGE_VALIDATE": 2,
    "JED_GEMMA_FORGE_MIN_POSTS": 3,
    "JED_RS_TEMPLATES": "5,6",
    "JED_RS_FRAC": 97,
    "JED_RS_REPS": 3,
}

RUNGS = [
    (
        "submission_kernel_l17_gf8n60",
        "ahmedmobasher86/jed-public-pt-safe",
        "jed public pt safe",
        {**GF, "JED_GEMMA_FORGE_K": 8, "JED_GEMMA_FORGE_N": 60},
        "L17 GEMMA-FORGE K=8 N=60; gpt fallback close_ok FRAC=97",
    ),
    (
        "submission_kernel_l17_gf8n90",
        "ahmedmobasher86/jed-public-pt-probe",
        "jed public pt probe",
        {**GF, "JED_GEMMA_FORGE_K": 8, "JED_GEMMA_FORGE_N": 90},
        "L17 GEMMA-FORGE K=8 N=90; medium ladder rung",
    ),
    (
        "submission_kernel_l17_gf8n120",
        "ahmedmobasher86/jed-public-k1nx-1000",
        "jed public k1nx 1000",
        {**GF, "JED_GEMMA_FORGE_K": 8, "JED_GEMMA_FORGE_N": 120},
        "L17 GEMMA-FORGE K=8 N=120; aggressive but under 960 posts",
    ),
    (
        "submission_kernel_l17_gf4n180",
        "ahmedmobasher86/jed-public-k1nx-1200",
        "jed public k1nx 1200",
        {**GF, "JED_GEMMA_FORGE_K": 4, "JED_GEMMA_FORGE_N": 180},
        "L17 GEMMA-FORGE K=4 N=180; lower per-candidate hop risk",
    ),
    (
        "submission_kernel_l17_splitmp",
        "ahmedmobasher86/jed-public-k1nx-800",
        "jed public k1nx 800",
        {
            "JED_AGG_PROBE": 1,
            "JED_EXFIL_PAYLOAD": "diag=SECRET_MARKER",
            "JED_GPTOSS_MP_K": 4,
            "JED_GPTOSS_N": 90,
            "JED_GEMMA_N": 760,
            "JED_GEMMA_PROMPT": 12,
        },
        "L17 SPLIT-MP hedge: existing agg-probe split, gpt K=4 plus gemma N=760",
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
            "enable_gpu": True,
            "machine_shape": "NvidiaTeslaT4",
            "enable_internet": False,
            "competition_sources": ["ai-agent-security-multi-step-tool-attacks"],
        }
        (dd / "kernel-metadata.json").write_text(json.dumps(meta, indent=2))
        print(f"built {d} -> {slug}  {note}")


if __name__ == "__main__":
    main()
