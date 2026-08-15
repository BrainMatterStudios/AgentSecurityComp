#!/usr/bin/env python3
"""Build the L30 reset ladder.

The ladder is based on the scored evidence through 2026-08-15:

1. Keep one exact high-water control so the reset batch has a reliable canary.
2. Test whether the replay-safe ledger is undersizing single-post capacity.
3. Spend one slot on a single-post count that can clear the current top.
4. Re-test amortization with K=4, not K=8, because K=8 has a poor score history.
5. Keep one calibrated high-ceiling K=8 fast-emit attempt.

This script only writes local Kaggle kernel folders. It does not push, run, or
submit anything.
"""

import base64
import json
import os
import py_compile
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPETITION = "ai-agent-security-multi-step-tool-attacks"
ATTACK_B64 = base64.b64encode((ROOT / "attack.py").read_bytes()).decode()
D4_PATH = Path("/tmp/d4.py")


def _patch_d4_control(src: str) -> str:
    out, n = re.subn(r"(?m)^REPLAY_SAFE_FRAC\s*=\s*[0-9.]+", "REPLAY_SAFE_FRAC = 0.98", src)
    if n != 1:
        raise RuntimeError(f"expected one REPLAY_SAFE_FRAC constant in d4 source, got {n}")
    fd, tmp = tempfile.mkstemp(suffix=".py")
    os.close(fd)
    try:
        Path(tmp).write_text(out)
        py_compile.compile(tmp, doraise=True)
    finally:
        Path(tmp).unlink(missing_ok=True)
    return out


D4_CONTROL_SOURCE = _patch_d4_control(D4_PATH.read_text()) if D4_PATH.exists() else (ROOT / "attack.py").read_text()
D4_B64 = base64.b64encode(D4_CONTROL_SOURCE.encode()).decode()

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
    source_kind: str
    env: dict[str, object]
    note: str


BASE_RS = {
    "JED_REPLAY_SAFE": 1,
    "JED_EXFIL_PAYLOAD": "diag=SECRET_MARKER",
    "JED_RS_TEMPLATES": "5,6",
    "JED_RS_FRAC": 98,
    "JED_RS_REPS": 3,
}

RUNGS = [
    Rung(
        "submission_kernel_l30_l27_control",
        "ahmedmobasher86/jed-public-pt-safe",
        "jed public pt safe",
        "d4",
        {},
        "L30 control: exact historical L27/dimong4 control path; canary for ~88.7 capability",
    ),
    Rung(
        "submission_kernel_l30_fixed1100",
        "ahmedmobasher86/jed-public-pt-probe",
        "jed public pt probe",
        "attack",
        {**BASE_RS, "JED_RS_FIXED_N": 1100},
        "L30 fixed-N 1100: single-post capacity probe above the current self-sizer",
    ),
    Rung(
        "submission_kernel_l30_fixed1530",
        "ahmedmobasher86/jed-public-k1nx-1000",
        "jed public k1nx 1000",
        "attack",
        {**BASE_RS, "JED_RS_FIXED_N": 1530},
        "L30 fixed-N 1530: single-post boundary attempt above 137.130 if both rows fit",
    ),
    Rung(
        "submission_kernel_l30_split_hop4",
        "ahmedmobasher86/jed-public-k1nx-1200",
        "jed public k1nx 1200",
        "attack",
        {
            **BASE_RS,
            "JED_RS_SPLIT": 1,
            "JED_RS_HOPPACK_GPT": 4,
            "JED_RS_HOPPACK_FORCE": 1,
        },
        "L30 split-hop4: lower-risk amortization than pending L29 K8",
    ),
    Rung(
        "submission_kernel_l30_fastemit_k8",
        "ahmedmobasher86/jed-public-k1nx-800",
        "jed public k1nx 800",
        "attack",
        {
            "JED_FAST_EMIT": 1,
            "JED_EMIT_K": 8,
            "JED_EMIT_CALIBRATE": 1,
            "JED_EMIT_SAFETY": "0.55",
            "JED_EMIT_CAP_N": 2000,
            "JED_MAX_CANDIDATES": 2000,
        },
        "L30 fast-emit K8: calibrated high-ceiling crown attempt",
    ),
]


def env_cell(env: dict[str, object], note: str) -> str:
    lines = ["import os"]
    lines.extend(f"os.environ[{key!r}]={str(value)!r}" for key, value in env.items())
    lines.append(f"print({note!r})")
    return "\n".join(lines) + "\n"


def write_attack_cell(source_kind: str) -> str:
    b64_name = "D4_B64" if source_kind == "d4" else "ATTACK_B64"
    b64 = D4_B64 if source_kind == "d4" else ATTACK_B64
    return (
        "import base64\n"
        f"# source={source_kind}; encoded_as={b64_name}\n"
        "open('/kaggle/working/attack.py','wb').write(base64.b64decode('%s'))\n"
        "print('attack.py written')\n"
        % b64
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
                cc(write_attack_cell(rung.source_kind)),
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
