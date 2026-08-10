#!/usr/bin/env python3
"""Build L20 instant fast-emit kernels targeting >118.0 public leaderboard score.

Constructs 5 ladder rungs testing target candidate bounds N=1200, N=1320,
N=1420 (primary target >118.0), plus baseline anchor and private deputy hedge.
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


EMIT_BASE = {
    "JED_FAST_EMIT": 1,
}

RUNGS = [
    (
        "submission_kernel_l20_anchor",
        "ahmedmobasher86/jed-public-pt-safe",
        "jed public pt safe",
        {
            "JED_REPLAY_SAFE": 1,
            "JED_EXFIL_PAYLOAD": "SECRET_MARKER",
            "JED_RS_TEMPLATES": "5,6",
            "JED_RS_FRAC": 97,
            "JED_RS_REPS": 3,
        },
        "L20 ANCHOR baseline single-post FRAC97 (~89.5 canary)",
    ),
    (
        "submission_kernel_l20_n1200",
        "ahmedmobasher86/jed-public-pt-probe",
        "jed public pt probe",
        {**EMIT_BASE, "JED_EMIT_GPT_N": 1200, "JED_EMIT_GEMMA_N": 1050},
        "L20 FAST EMIT GPT=1200 GEMMA=1050 (conservative ~108.0 target)",
    ),
    (
        "submission_kernel_l20_n1320",
        "ahmedmobasher86/jed-public-k1nx-1000",
        "jed public k1nx 1000",
        {**EMIT_BASE, "JED_EMIT_GPT_N": 1320, "JED_EMIT_GEMMA_N": 1150},
        "L20 FAST EMIT GPT=1320 GEMMA=1150 (secondary ~117.0 target)",
    ),
    (
        "submission_kernel_l20_n1420",
        "ahmedmobasher86/jed-public-k1nx-1200",
        "jed public k1nx 1200",
        {**EMIT_BASE, "JED_EMIT_GPT_N": 1420, "JED_EMIT_GEMMA_N": 1200},
        "L20 FAST EMIT GPT=1420 GEMMA=1200 (PRIMARY WIN TARGET >118.0)",
    ),
    (
        "submission_kernel_l20_deputy",
        "ahmedmobasher86/jed-public-k1nx-800",
        "jed public k1nx 800",
        {
            "JED_REPLAY_SAFE": 1,
            "JED_RS_CHANNEL": "deputy",
            "JED_RS_FRAC": 97,
            "JED_RS_REPS": 3,
        },
        "L20 DEPUTY HEDGE replay-safe single-message clean body (~24 private)",
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
