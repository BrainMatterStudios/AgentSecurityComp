#!/usr/bin/env python3
"""Build 3 GPT-ISOLATED diagnostic kernels (2026-08-28 endgame A/B).

Motivation: our attack.py already contains every published winning technique
(harmony reasoning-collapse via inj_close/close_ok + _p_forge_plan ported from
dimong4/nctuan LB 107-134; per-model fire-rate selector _run_l32_selector;
replay-safe adaptive sizing _run_replay_safe). We still score ~92 vs their
107-137. Local testing CANNOT explain the gap: attack.py:1521 documents that
local llama.cpp always suppresses the analysis channel, so local decode/fire
measurements are blind to how the REAL eval gpt-oss reasons and how many posts
our forge actually fires there. Only board A/B can read it.

Each kernel sets JED_RS_ONLY=gpt -> gemma row scores ~0, so publicScore =
gpt_row / 2. Doubling the observed score gives our true isolated gpt row, which
we compare against the ~130-164 gpt row implied by the 107-137 cluster.

  forge8  : forge_plan N=8 (current HEDGE-A primitive)      -> true forge8 ceiling
  single  : close_ok single-post (tidx 5, cheapest firing)  -> is 8-post forge > single on the EVAL?
  forge4  : forge_plan N=4                                   -> does N=8 under-fire vs N=4 (docstring ~4.0 posts@n=4)?

FIXED_N=2000 is an upper bound; the 9000s replay phase caps the count actually
run (~978, empirically non-voiding since HEDGE-A scores ~92 not 0).
"""
import base64, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATTACK_B64 = base64.b64encode((ROOT / "attack.py").read_bytes()).decode()

CELL0 = ("import sys,glob,os\n"
         "for p in glob.glob('/kaggle/input/**/kaggle_evaluation',recursive=True):\n"
         " r=os.path.dirname(p)\n"
         " if os.path.isdir(os.path.join(r,'aicomp_sdk')): sys.path.insert(0,r); break\n"
         "sys.path.insert(0,'/kaggle/working'); print('setup')\n")
CELL2 = ("import base64\n"
         "open('/kaggle/working/attack.py','wb').write(base64.b64decode('%s'))\n" % ATTACK_B64)
CELL3 = ("import os\nfrom pathlib import Path\n"
         "sub=Path('/kaggle/working/submission.csv')\n"
         "try:\n"
         " import kaggle_evaluation.jed_attack_134815.jed_attack_inference_server as srv\n"
         " srv.JEDAttackInferenceServer().serve()\n"
         "except Exception as e:\n"
         " if os.getenv('KAGGLE_IS_COMPETITION_RERUN') is not None: raise\n"
         " print('skip',repr(e)[:60])\n"
         "if not sub.exists(): sub.write_text('Id,Score\\ngpt_oss_public,0.0\\ngpt_oss_private,0.0\\ngemma_public,0.0\\ngemma_private,0.0\\n')\n")

_COMMON = {"JED_REPLAY_SAFE": "1", "JED_EXFIL_PAYLOAD": "SECRET_MARKER",
           "JED_RS_ONLY": "gpt", "JED_RS_FIXED_N": "2000"}

DIAG = {
 "jed-diag-gpt-forge8": (
   {**_COMMON, "JED_RS_FORGE_GPT_ONLY": "1", "JED_RS_FORGE_PLAN": "8"},
   "DIAG gpt-isolated forge8 (current HEDGE-A primitive) -> true forge8 gpt-row ceiling (score x2)"),
 "jed-diag-gpt-single": (
   {**_COMMON, "JED_RS_FIXED_TIDX": "5"},
   "DIAG gpt-isolated close_ok single-post (tidx5) -> is 8-post forge actually > single on the EVAL? (score x2)"),
 "jed-diag-gpt-forge4": (
   {**_COMMON, "JED_RS_FORGE_GPT_ONLY": "1", "JED_RS_FORGE_PLAN": "4"},
   "DIAG gpt-isolated forge4 -> does forge under-fire at N=8 vs N=4? (score x2)"),
}


def cc(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": src}


for slug, (envd, desc) in DIAG.items():
    cell1 = "import os\n" + "".join(f"os.environ['{k}']='{v}'\n" for k, v in envd.items()) + f"print({desc!r})\n"
    nb = {"cells": [cc(CELL0), cc(cell1), cc(CELL2), cc(CELL3)],
          "metadata": {"kernelspec": {"language": "python", "name": "python3", "display_name": "Python 3"}},
          "nbformat": 4, "nbformat_minor": 5}
    d = ROOT / ("submission_kernel_" + slug.replace("-", "_")); d.mkdir(exist_ok=True)
    (d / "k.ipynb").write_text(json.dumps(nb))
    (d / "kernel-metadata.json").write_text(json.dumps({
        "id": "ahmedmobasher86/" + slug, "title": slug.replace("-", " "),
        "code_file": "k.ipynb", "language": "python", "kernel_type": "notebook", "is_private": True,
        "enable_gpu": False, "machine_shape": "NvidiaTeslaT4", "enable_internet": False,
        "competition_sources": ["ai-agent-security-multi-step-tool-attacks"]}, indent=2))
    print("built", slug)
