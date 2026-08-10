#!/usr/bin/env python3
"""Build L21 multi-call self-calibrating fast-emit kernels (Target >118 LB).

Each multi-call rung emits K=8 http.post directives per candidate in ONE message:
  - gpt-oss: sequential short-domain posts + harmony preclose (verified avg 7.9 posts)
  - gemma:   1-cycle special-token forge (_gemma_forge_msg, verified 8 posts local,
             ~6.7/8 on the real board via L18 ACO-FORGE)
The engine self-calibrates: it measures the real per-candidate generation cost of the
K-call message on the live model (3 samples), estimates the in-process replay cost
(gen minus ~1.5s RPC), and sizes N = 9000*safety/replay_est. Rungs differ only by
safety factor, spanning the linear-vs-amortized replay-cost uncertainty.
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


def mp(safety, note):
    return {
        "JED_FAST_EMIT": 1,
        "JED_EMIT_K": 8,
        "JED_EMIT_CALIBRATE": 1,
        "JED_EMIT_SAFETY": str(safety),
        "JED_EMIT_CAP_N": 2000,
        "JED_MAX_CANDIDATES": 2000,
        "JED_EMIT_NOTE": note,
    }


RUNGS = [
    (
        "submission_kernel_l21_anchor",
        "ahmedmobasher86/jed-public-mp-anchor",
        "jed public mp anchor",
        {
            "JED_REPLAY_SAFE": 1,
            "JED_EXFIL_PAYLOAD": "SECRET_MARKER",
            "JED_RS_TEMPLATES": "5,6",
            "JED_RS_FRAC": 97,
            "JED_RS_REPS": 3,
        },
        "L21 ANCHOR single-post FRAC97 (~89.5 banked)",
    ),
    (
        "submission_kernel_l21_safe",
        "ahmedmobasher86/jed-public-mp-safe",
        "jed public mp safe",
        mp(0.75, "SAFE"),
        "L21 MULTI-CALL K8 CAL SAFETY=0.75 (conservative ~110+)",
    ),
    (
        "submission_kernel_l21_moderate",
        "ahmedmobasher86/jed-public-mp-moderate",
        "jed public mp moderate",
        mp(0.90, "MODERATE"),
        "L21 MULTI-CALL K8 CAL SAFETY=0.90 (primary ~140+)",
    ),
    (
        "submission_kernel_l21_aggressive",
        "ahmedmobasher86/jed-public-mp-aggressive",
        "jed public mp aggressive",
        mp(1.05, "AGGRESSIVE"),
        "L21 MULTI-CALL K8 CAL SAFETY=1.05 (stretch ~165+)",
    ),
    (
        "submission_kernel_l21_stretch",
        "ahmedmobasher86/jed-public-mp-stretch",
        "jed public mp stretch",
        mp(1.20, "STRETCH"),
        "L21 MULTI-CALL K8 CAL SAFETY=1.20 (boundary probe)",
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
