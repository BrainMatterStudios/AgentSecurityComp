#!/usr/bin/env python3
"""Build the L33 fixed-N single-post ladder.

L33 tests the mechanism implied by the current public leaderboard: a high-density
single-post replay set with one unique EXFILTRATION cell per candidate. Local GPT
and Gemma checks showed the exact SECRET_MARKER payload fires cleanly, with GPT
favoring the harmony-close template and Gemma favoring the terse template.

This script only writes local Kaggle kernel folders. It does not push, run, or
submit anything.
"""

import base64
import json
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPETITION = "ai-agent-security-multi-step-tool-attacks"
ATTACK_B64 = base64.b64encode((ROOT / "attack.py").read_bytes()).decode()

CELL0 = (
    "import sys,glob,os\n"
    "for p in glob.glob('/kaggle/input/**/kaggle_evaluation',recursive=True):\n"
    " r=os.path.dirname(p)\n"
    " if os.path.isdir(os.path.join(r,'aicomp_sdk')): sys.path.insert(0,r); break\n"
    "sys.path.insert(0,'/kaggle/working'); print('setup')\n"
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


@dataclass(frozen=True)
class Rung:
    directory: str
    slug: str
    title: str
    env: dict[str, object]
    note: str


BASE_L33 = {
    "JED_REPLAY_SAFE": 1,
    "JED_EXFIL_PAYLOAD": "SECRET_MARKER",
    "JED_RS_TEMPLATES": "5,6",
    "JED_RS_MAX_CAND": 2000,
    "JED_RS_FIXED_ROUTE": 1,
}


RUNGS = [
    Rung(
        "submission_kernel_l33_fixed1530",
        "ahmedmobasher86/jed-l33-fixed-1530",
        "jed l33 fixed 1530",
        {**BASE_L33, "JED_RS_FIXED_N": 1530},
        "L33 fixed single-post N=1530: slight over-top boundary shot",
    ),
    Rung(
        "submission_kernel_l33_fixed1600",
        "ahmedmobasher86/jed-l33-fixed-1600",
        "jed l33 fixed 1600",
        {**BASE_L33, "JED_RS_FIXED_N": 1600},
        "L33 fixed single-post N=1600: high push if replay budget fits",
    ),
    Rung(
        "submission_kernel_l33_fixed1524",
        "ahmedmobasher86/jed-l33-fixed-1524",
        "jed l33 fixed 1524",
        {**BASE_L33, "JED_RS_FIXED_N": 1524},
        "L33 fixed single-post N=1524: direct 137.16 leaderboard shot",
    ),
    Rung(
        "submission_kernel_l33_fixed1450",
        "ahmedmobasher86/jed-l33-fixed-1450",
        "jed l33 fixed 1450",
        {**BASE_L33, "JED_RS_FIXED_N": 1450},
        "L33 fixed single-post N=1450: safer replay-dense validation rung",
    ),
    Rung(
        "submission_kernel_l33_fixed2000",
        "ahmedmobasher86/jed-l33-fixed-2000",
        "jed l33 fixed 2000",
        {**BASE_L33, "JED_RS_FIXED_N": 2000},
        "L33 fixed single-post N=2000: max-capacity probe if replay budget allows",
    ),
]


def env_cell(env: dict[str, object], note: str) -> str:
    lines = ["import os"]
    lines.extend(f"os.environ[{key!r}]={str(value)!r}" for key, value in env.items())
    lines.append(f"print({note!r})")
    return "\n".join(lines) + "\n"


def write_attack_cell() -> str:
    return (
        "import base64\n"
        "open('/kaggle/working/attack.py','wb').write(base64.b64decode('%s'))\n"
        "print('attack.py written')\n"
        % ATTACK_B64
    )


def cc(src: str) -> dict[str, object]:
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": src,
    }


def main() -> None:
    for rung in RUNGS:
        d = ROOT / rung.directory
        d.mkdir(exist_ok=True)
        nb = {
            "cells": [
                cc(CELL0),
                cc(env_cell(rung.env, rung.note)),
                cc(write_attack_cell()),
                cc(CELL3),
            ],
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
        meta = {
            "id": rung.slug,
            "title": rung.title,
            "code_file": "k.ipynb",
            "language": "python",
            "kernel_type": "notebook",
            "is_private": True,
            "enable_gpu": True,
            "machine_shape": "NvidiaTeslaT4",
            "enable_internet": False,
            "competition_sources": [COMPETITION],
        }
        (d / "k.ipynb").write_text(json.dumps(nb))
        (d / "kernel-metadata.json").write_text(json.dumps(meta, indent=2))
        print(f"built {rung.directory} -> {rung.slug} | {rung.note}")


if __name__ == "__main__":
    main()
