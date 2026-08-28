#!/usr/bin/env python3
"""Build the MULTI-MESSAGE forge test kernels — the untested throughput lever behind the 108-147
public cluster. Each candidate packs K forge messages into ONE finding (8*K EXFIL) so the
per-finding fixed replay overhead is amortized. Source: hop cap 8 (gateway:398) but
MAX_REPLAY_MESSAGES_PER_FINDING=32 (ops.py:48). Brackets K=2/3/4 to find the sweet spot vs the
~92 single-message baseline. Board-test these; if a K wins, that's the 92->130+ path."""
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

BASE = {"JED_REPLAY_SAFE": "1", "JED_EXFIL_PAYLOAD": "SECRET_MARKER",
        "JED_RS_FORGE_PLAN": "8", "JED_RS_FIXED_N": "2000"}
KS = {"jed-mm2": "2", "jed-mm3": "3", "jed-mm4": "4"}

def cc(src): return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": src}

for slug, k in KS.items():
    envd = dict(BASE); envd["JED_RS_MULTIMSG"] = k
    desc = f"MULTIMSG K={k}: {k} forge messages/candidate = 8*{k} EXFIL/finding (amortization lever vs ~92 baseline)"
    cell1 = "import os\n" + "".join(f"os.environ['{kk}']='{vv}'\n" for kk, vv in envd.items()) + f"print({desc!r})\n"
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
