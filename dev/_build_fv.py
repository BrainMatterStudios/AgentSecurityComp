#!/usr/bin/env python3
"""Build the FIRING-RATE + gemma-fill sweep (2026-08-29 endgame).

Board signal (2026-08-29 diagnostics): gpt-iso forge4 row 95 > forge8 row 83.
A candidate asking for 8 posts scoring LESS than one asking for 4 => _p_forge_plan
UNDER-FIRES at N=8 (~4 posts/cand ceiling); the extra hops burn replay budget without
firing. The 107-134 cluster (whose forge we ported) must fire closer to 8/8. So the
lever is FIRING RATE, not N. Test 4 structurally-distinct N=8 gpt forges (highest gpt-iso
row = fires most) + 1 gemma budget-fill-max read (is the ~76 gemma row leaving points on
the table vs its ~96-100 single-post ceiling?). All gpt kernels JED_RS_ONLY=gpt, gemma
kernel JED_RS_ONLY=gemma -> observed public x2 = that row. Matched same-day (variance hits
all equally). Uses ADAPTIVE self-sizing (no fixed-N) so a well-firing variant returns fewer,
costlier candidates that fill FRAC*9000s instead of voiding on a 9000s replay overrun.
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

# ADAPTIVE (not fixed-N): fixed_n=2000 has real void risk -- _replay_and_score iterates
# candidates[:2000] with no internal deadline and the gateway voids the WHOLE submission on a
# 9000s replay overrun (single-post N=1530 ERRORed). Worse, a forge that actually fires 8/8
# replays far slower and would VOID exactly the winning variant. So omit JED_RS_FIXED_N ->
# attack.py's adaptive forge fill self-sizes each variant to FRAC*9000s (void-safe by design).
_GPT = {"JED_REPLAY_SAFE": "1", "JED_EXFIL_PAYLOAD": "SECRET_MARKER", "JED_RS_ONLY": "gpt",
        "JED_RS_FORGE_PLAN": "8", "JED_RS_FRAC": "97"}

FV = {
 "jed-fv-plan": (
   {**_GPT, "JED_RS_FORGE_VARIANT": "plan"},
   "FV gpt-iso forge8 PLAN (control; current HEDGE-A) -> baseline gpt row (x2)"),
 "jed-fv-min": (
   {**_GPT, "JED_RS_FORGE_VARIANT": "min"},
   "FV gpt-iso forge8 MIN (shorter plan) -> firing rate vs plan (x2)"),
 "jed-fv-seq": (
   {**_GPT, "JED_RS_FORGE_VARIANT": "seq"},
   "FV gpt-iso forge8 SEQ (inline http.post x8 + final-preclose) -> firing rate (x2)"),
 "jed-fv-multipost": (
   {**_GPT, "JED_RS_FORGE_VARIANT": "multipost"},
   "FV gpt-iso forge8 MULTIPOST (newline URL list, one/turn until all sent) -> firing rate (x2)"),
 "jed-fv-gemmafill": (
   {"JED_REPLAY_SAFE": "1", "JED_EXFIL_PAYLOAD": "SECRET_MARKER", "JED_RS_ONLY": "gemma",
    "JED_RS_FRAC": "99"},
   "FV gemma-iso adaptive FRAC=99 budget-fill -> is the ~76 gemma row under-filling? (x2)"),
}


def cc(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": src}


for slug, (envd, desc) in FV.items():
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
