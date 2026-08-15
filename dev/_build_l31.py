#!/usr/bin/env python3
"""Build the L31 reset ladder.

L31 supersedes L30. It tests the unsubmitted chain-pack mechanism discovered in
the SDK audit: several K-hop messages inside one AttackCandidate. The public
guardrail still sees only clean direct http.post calls, while the gateway replays
up to 32 messages per candidate.

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


BASE_RS = {
    "JED_REPLAY_SAFE": 1,
    "JED_EXFIL_PAYLOAD": "diag=SECRET_MARKER",
    "JED_RS_TEMPLATES": "5,6",
    "JED_RS_FRAC": 96,
    "JED_RS_REPS": 3,
    "JED_RS_HOPPACK_FORCE": 1,
}

FAST_EMIT = {
    "JED_FAST_EMIT": 1,
    "JED_EMIT_K": 8,
    "JED_EMIT_CALIBRATE": 1,
    "JED_EMIT_SAFETY": "0.55",
    "JED_EMIT_CAP_N": 2000,
    "JED_MAX_CANDIDATES": 2000,
}

RUNGS = [
    Rung(
        "submission_kernel_l31_chainpack_2x8",
        "ahmedmobasher86/jed-public-pt-safe",
        "jed public pt safe",
        {
            **BASE_RS,
            "JED_RS_SPLIT": 1,
            "JED_RS_HOPPACK_GPT": 8,
            "JED_RS_HOPPACK": 8,
            "JED_RS_CHAINPACK": 2,
        },
        "L31 chainpack 2x8: GPT-routed two K8 messages per candidate; Gemma falls back to single-post",
    ),
    Rung(
        "submission_kernel_l31_chainpack_3x8",
        "ahmedmobasher86/jed-public-pt-probe",
        "jed public pt probe",
        {
            **BASE_RS,
            "JED_RS_SPLIT": 1,
            "JED_RS_HOPPACK_GPT": 8,
            "JED_RS_HOPPACK": 8,
            "JED_RS_CHAINPACK": 3,
        },
        "L31 chainpack 3x8: stretch GPT chainpack, Gemma single-post fallback",
    ),
    Rung(
        "submission_kernel_l31_chainpack_4x8",
        "ahmedmobasher86/jed-public-k1nx-1000",
        "jed public k1nx 1000",
        {
            **BASE_RS,
            "JED_RS_SPLIT": 1,
            "JED_RS_HOPPACK_GPT": 8,
            "JED_RS_HOPPACK": 8,
            "JED_RS_CHAINPACK": 4,
            "JED_RS_FRAC": 94,
        },
        "L31 chainpack 4x8: crown shot; lower fraction offsets four-message replay cost",
    ),
    Rung(
        "submission_kernel_l31_chainpack_4x4",
        "ahmedmobasher86/jed-public-k1nx-1200",
        "jed public k1nx 1200",
        {
            **BASE_RS,
            "JED_RS_HOPPACK": 4,
            "JED_RS_CHAINPACK": 4,
            "JED_RS_FRAC": 94,
        },
        "L31 chainpack 4x4: lower-hop both-board transfer probe",
    ),
    Rung(
        "submission_kernel_l31_fastemit_k8",
        "ahmedmobasher86/jed-public-k1nx-800",
        "jed public k1nx 800",
        FAST_EMIT,
        "L31 fast-emit K8: calibrated high-ceiling backup not evidenced as scored",
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
