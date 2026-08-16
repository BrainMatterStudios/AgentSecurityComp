#!/usr/bin/env python3
"""Build the L32 adaptive-selector ladder.

L32 converts the local evidence into a live selector:

1. Always measure the single-post control arm.
2. Measure GPT forge arms only when they can plausibly beat the control.
3. Use Gemma single-post by default, because local Gemma forge value density was
   worse than the terse single-post control.
4. Fill either with the legacy live-verified ledger or a conservative fast-fill
   estimate, depending on the rung.

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


BASE_L32 = {
    "JED_REPLAY_SAFE": 1,
    "JED_EXFIL_PAYLOAD": "diag=SECRET_MARKER",
    "JED_RS_TEMPLATES": "5,6",
    "JED_RS_FRAC": 96,
    "JED_RS_REPS": 2,
    "JED_RS_MAX_CAND": 2000,
    "JED_L32_SELECTOR": 1,
    "JED_L32_REPS": 2,
    "JED_L32_WARMUP": 1,
    "JED_L32_MARGIN": "1.03",
    "JED_L32_COST_MULT": "1.10",
    "JED_L32_GPT_FORGE": 1,
    "JED_L32_GPT_FORGE_KS": "4,6,8",
    "JED_L32_FINAL_OPEN": 1,
    "JED_L32_GEMMA_FORGE": 0,
}


RUNGS = [
    Rung(
        "submission_kernel_l32_selector_safe",
        "ahmedmobasher86/jed-l32-selector-safe",
        "jed l32 selector safe",
        {
            **BASE_L32,
            "JED_RS_FRAC": 95,
            "JED_L32_MARGIN": "1.05",
            "JED_L32_COST_MULT": "1.15",
        },
        "L32 safe selector: live-verified fill; forge only if it clearly beats single-post control",
    ),
    Rung(
        "submission_kernel_l32_selector_fast_safe",
        "ahmedmobasher86/jed-l32-selector-fast-safe",
        "jed l32 selector fast safe",
        {
            **BASE_L32,
            "JED_RS_FRAC": 95,
            "JED_L32_FAST_FILL": 1,
            "JED_L32_MARGIN": "1.05",
            "JED_L32_COST_MULT": "1.20",
        },
        "L32 fast-safe selector: low replay fraction plus 20% measured-cost cushion",
    ),
    Rung(
        "submission_kernel_l32_selector_fast_push",
        "ahmedmobasher86/jed-l32-selector-fast-push",
        "jed l32 selector fast push",
        {
            **BASE_L32,
            "JED_RS_FRAC": 98,
            "JED_L32_FAST_FILL": 1,
            "JED_L32_MARGIN": "1.00",
            "JED_L32_COST_MULT": "1.08",
        },
        "L32 fast-push selector: leaderboard attempt with tighter replay cushion",
    ),
    Rung(
        "submission_kernel_l32_gpt_forge_selector",
        "ahmedmobasher86/jed-l32-gpt-forge-selector",
        "jed l32 gpt forge selector",
        {
            **BASE_L32,
            "JED_RS_ONLY": "gpt",
            "JED_RS_FRAC": 97,
            "JED_L32_FAST_FILL": 1,
            "JED_L32_MARGIN": "1.00",
            "JED_L32_COST_MULT": "1.10",
            "JED_L32_GEMMA_FORGE": 0,
        },
        "L32 GPT diagnostic: isolated selector readout for single vs GPT forge arms",
    ),
    Rung(
        "submission_kernel_l32_gemma_single_push",
        "ahmedmobasher86/jed-l32-gemma-single-push",
        "jed l32 gemma single push",
        {
            **BASE_L32,
            "JED_RS_ONLY": "gemma",
            "JED_RS_FRAC": 99,
            "JED_L32_FAST_FILL": 1,
            "JED_L32_MARGIN": "1.00",
            "JED_L32_COST_MULT": "1.10",
            "JED_L32_GPT_FORGE": 0,
            "JED_L32_GEMMA_FORGE": 0,
        },
        "L32 Gemma diagnostic: isolated high-fraction terse single-post readout",
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
