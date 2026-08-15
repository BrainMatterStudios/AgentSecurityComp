#!/usr/bin/env python3
"""Build L29 research ladder from local evidence.

This ladder is intentionally our own experiment:

1. Control: current replay-safe engine.
2. Split hop-pack: route gpt to K=8 hop-pack, keep gemma single-post.
3. Gpt-only fixed-N bracket: measure whether K=8 replay cost can support a
   first-place-scale gpt row without mixing in gemma.
4. Gemma-only high replay fraction: test whether the fast row has hidden
   headroom without risking the gpt row.
5. Deputy hedge: preserve the private-board confused-deputy channel.

The script only writes local Kaggle kernel folders. It does not push, run, or
submit anything.
"""

from __future__ import annotations

import base64
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATTACK_B64 = base64.b64encode((ROOT / "attack.py").read_bytes()).decode()
COMPETITION = "ai-agent-security-multi-step-tool-attacks"

CELL0 = (
    "import sys,glob,os\n"
    "for p in glob.glob('/kaggle/input/**/kaggle_evaluation',recursive=True):\n"
    " r=os.path.dirname(p)\n"
    " if os.path.isdir(os.path.join(r,'aicomp_sdk')): sys.path.insert(0,r); break\n"
    "sys.path.insert(0,'/kaggle/working'); print('setup')\n"
)
CELL2 = (
    "import base64\n"
    "open('/kaggle/working/attack.py','wb').write(base64.b64decode('%s'))\n"
    "print('attack.py written')\n"
    % ATTACK_B64
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

BASE = {
    "JED_REPLAY_SAFE": 1,
    "JED_EXFIL_PAYLOAD": "diag=SECRET_MARKER",
    "JED_RS_TEMPLATES": "5,6",
    "JED_RS_FRAC": 98,
    "JED_RS_REPS": 3,
}


def env_cell(env: dict[str, object], note: str) -> str:
    lines = ["import os"]
    lines.extend(f"os.environ[{key!r}]={str(value)!r}" for key, value in env.items())
    lines.append(f"print({note!r})")
    return "\n".join(lines) + "\n"


def cc(src: str) -> dict[str, object]:
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": src,
    }


RUNGS = [
    (
        "submission_kernel_l29_control",
        "ahmedmobasher86/jed-public-pt-safe",
        "jed public pt safe",
        dict(BASE),
        "L29 control: current replay-safe engine, GPU/T4 metadata, no new mechanism",
    ),
    (
        "submission_kernel_l29_split_hop8",
        "ahmedmobasher86/jed-public-pt-probe",
        "jed public pt probe",
        {
            **BASE,
            "JED_RS_SPLIT": 1,
            "JED_RS_HOPPACK_GPT": 8,
            "JED_RS_HOPPACK_FORCE": 1,
        },
        "L29 split: route gpt to K8 hop-pack, keep gemma single-post",
    ),
    (
        "submission_kernel_l29_gpt_hop8_n260",
        "ahmedmobasher86/jed-public-k1nx-1000",
        "jed public k1nx 1000",
        {
            **BASE,
            "JED_RS_ONLY": "gpt",
            "JED_RS_HOPPACK": 8,
            "JED_RS_HOPPACK_FORCE": 1,
            "JED_RS_FIXED_N": 260,
        },
        "L29 gpt-only fixed N260 K8: bracket replay cost and row upside",
    ),
    (
        "submission_kernel_l29_gemma_frac999",
        "ahmedmobasher86/jed-public-k1nx-1200",
        "jed public k1nx 1200",
        {
            **BASE,
            "JED_RS_ONLY": "gemma",
            "JED_RS_FRAC_GEMMA": 999,
        },
        "L29 gemma-only RSF 0.999: test fast-row headroom without gpt risk",
    ),
    (
        "submission_kernel_l29_deputy_hedge",
        "ahmedmobasher86/jed-public-k1nx-800",
        "jed public k1nx 800",
        {
            **BASE,
            "JED_RS_CHANNEL": "deputy",
            "JED_RS_ONLY": "gemma",
        },
        "L29 deputy hedge: private-board confused-deputy channel",
    ),
]


def main() -> None:
    for directory, slug, title, env, note in RUNGS:
        d = ROOT / directory
        d.mkdir(exist_ok=True)
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
        (d / "k.ipynb").write_text(json.dumps(nb))
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
            "competition_sources": [COMPETITION],
        }
        (d / "kernel-metadata.json").write_text(json.dumps(meta, indent=2))
        print(f"built {directory} -> {slug} | {note}")


if __name__ == "__main__":
    main()
