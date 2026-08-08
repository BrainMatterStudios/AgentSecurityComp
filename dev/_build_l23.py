#!/usr/bin/env python3
"""Build L23 — deterministic-router amortization ladder.

Replaces the L22-broken safety fingerprint with the post-count router (_detect_board,
best-of-3) and adds the self-measuring JED_RS_SPLIT (gpt->hoppack2 with amortization
guard, gemma->single). All rungs downside-pinned at the anchor (the guard/misroute both
degrade to single-post). Hoppack rungs run at FRAC94-95 (untested at 97 on CUDA).

Reads when scores land:
  gpt amortization = gpt_hop2 / gpt_single  (both = gpt_row/2 via ONLY router)
  blended shot     = split95 / split94
  gemma baseline   = gem_single (= gemma_row/2; router cross-check)
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

BASE = {
    "JED_REPLAY_SAFE": 1,
    "JED_EXFIL_PAYLOAD": "SECRET_MARKER",
    "JED_RS_TEMPLATES": "5,6",
    "JED_RS_REPS": 3,
}


def env_cell(env, note):
    lines = ["import os"]
    lines.extend("os.environ[%r]=%r" % (k, str(v)) for k, v in env.items())
    lines.append("print(%r)" % note)
    return "\n".join(lines) + "\n"


def cc(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": src}


RUNGS = [
    ("submission_kernel_l23_gpt_single", "ahmedmobasher86/jed-public-pt-safe",
     "jed public pt safe", {**BASE, "JED_RS_ONLY": "gpt", "JED_RS_FRAC": 97},
     "L23 gpt-only SINGLE-post FRAC97 (gpt baseline row via router)"),
    ("submission_kernel_l23_gpt_hop2", "ahmedmobasher86/jed-public-pt-probe",
     "jed public pt probe", {**BASE, "JED_RS_ONLY": "gpt", "JED_RS_HOPPACK": 2, "JED_RS_FRAC": 95},
     "L23 gpt-only HOPPACK2 amort-guard FRAC95 (clean gpt amortization AB)"),
    ("submission_kernel_l23_split95", "ahmedmobasher86/jed-public-k1nx-1000",
     "jed public k1nx 1000", {**BASE, "JED_RS_SPLIT": 1, "JED_RS_FRAC": 95},
     "L23 SPLIT gpt-hoppack2 gemma-single FRAC95 (blended 100+ shot)"),
    ("submission_kernel_l23_split94", "ahmedmobasher86/jed-public-k1nx-1200",
     "jed public k1nx 1200", {**BASE, "JED_RS_SPLIT": 1, "JED_RS_FRAC": 94},
     "L23 SPLIT gpt-hoppack2 gemma-single FRAC94 (void-margin duplicate)"),
    ("submission_kernel_l23_gem_single", "ahmedmobasher86/jed-public-k1nx-800",
     "jed public k1nx 800", {**BASE, "JED_RS_ONLY": "gemma", "JED_RS_FRAC": 97},
     "L23 gemma-only SINGLE-post FRAC97 (gemma baseline row via router)"),
]


def main():
    for d, slug, title, env, note in RUNGS:
        dd = ROOT / d
        dd.mkdir(exist_ok=True)
        nb = {
            "cells": [cc(CELL0), cc(env_cell(env, note)), cc(CELL2), cc(CELL3)],
            "metadata": {"kernelspec": {"language": "python", "name": "python3",
                                        "display_name": "Python 3"}},
            "nbformat": 4, "nbformat_minor": 5,
        }
        (dd / "k.ipynb").write_text(json.dumps(nb))
        meta = {
            "id": slug, "title": title, "code_file": "k.ipynb", "language": "python",
            "kernel_type": "notebook", "is_private": True, "enable_gpu": False,
            "enable_internet": False,
            "competition_sources": ["ai-agent-security-multi-step-tool-attacks"],
        }
        (dd / "kernel-metadata.json").write_text(json.dumps(meta, indent=2))
        print(f"built {d} -> {slug}  {note}")


if __name__ == "__main__":
    main()
