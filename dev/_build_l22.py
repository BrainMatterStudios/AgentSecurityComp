#!/usr/bin/env python3
"""Build L22 AMORTIZATION A/B ladder — the decisive test of whether adding a 2nd
http.post hop per candidate is NET-POSITIVE on the real T4 board (the 100+ crux).

All rungs use PROVEN existing knobs (no attack.py change): JED_REPLAY_SAFE self-
calibrating ledger + JED_RS_ONLY board isolation + JED_RS_HOPPACK=2 (one message ->
2 sequential http.post over 2 hops -> 2 EXFIL = 32/finding vs single 16). The ledger
measures the real packed-candidate cost live and sizes N to FRAC97*9000s, so an
over-cost board self-limits (no void) and a board that won't pack auto-falls-back to
single-post. Board-isolated rungs read one board's row directly (publicScore = row/2).

Read (after scores land):
  gpt amortization  = pt-probe / pt-safe      (both = gpt_row/2)
  gemma amortization= k1nx-1200 / k1nx-1000   (both = gemma_row/2)
  blended 100+ shot = k1nx-800                 (should ~= pt-probe + k1nx-1200)
If pt-probe > pt-safe -> gpt fixed-cost amortizes -> 2-post is the throughput lever
to 100+. If flat/negative -> genuinely decode-bound, proven directly (not by analogy).
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
    "JED_RS_FRAC": 97,
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
    ("submission_kernel_l22_gpt_single", "ahmedmobasher86/jed-public-pt-safe",
     "jed public pt safe", {**BASE, "JED_RS_ONLY": "gpt"},
     "L22 gpt-only SINGLE-post FRAC97 (gpt baseline row/2)"),
    ("submission_kernel_l22_gpt_hop2", "ahmedmobasher86/jed-public-pt-probe",
     "jed public pt probe", {**BASE, "JED_RS_ONLY": "gpt", "JED_RS_HOPPACK": 2},
     "L22 gpt-only HOPPACK2 (2 EXFIL/cand) FRAC97 (gpt amortization A/B)"),
    ("submission_kernel_l22_gem_single", "ahmedmobasher86/jed-public-k1nx-1000",
     "jed public k1nx 1000", {**BASE, "JED_RS_ONLY": "gemma"},
     "L22 gemma-only SINGLE-post FRAC97 (gemma baseline row/2)"),
    ("submission_kernel_l22_gem_hop2", "ahmedmobasher86/jed-public-k1nx-1200",
     "jed public k1nx 1200", {**BASE, "JED_RS_ONLY": "gemma", "JED_RS_HOPPACK": 2},
     "L22 gemma-only HOPPACK2 FRAC97 (gemma amortization A/B; auto-fallback if no pack)"),
    ("submission_kernel_l22_both_hop2", "ahmedmobasher86/jed-public-k1nx-800",
     "jed public k1nx 800", {**BASE, "JED_RS_HOPPACK": 2},
     "L22 BOTH-boards HOPPACK2 FRAC97 (the 100+ blended shot)"),
]


def main():
    versions = {}
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
        versions[slug] = d
        print(f"built {d} -> {slug}  {note}")
    print("\nslug->dir map:", json.dumps(versions, indent=2))


if __name__ == "__main__":
    main()
