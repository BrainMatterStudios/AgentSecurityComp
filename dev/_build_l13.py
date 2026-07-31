"""Build L13 kernels — DIAGNOSTIC NIGHT: resolve the board split + bracket the gpt ceiling.
All rungs JED_REPLAY_SAFE=1, pool {close_ok,terse_ok} (JED_RS_TEMPLATES=5,6), SECRET_MARKER.
- Rung 1 ANCHOR: both boards, FRAC=97 -> ~89.6 (canary + safe floor; protects standing)
- Rung 2 GPT-ONLY FRAC=97: JED_RS_ONLY=gpt -> publicScore = gpt_row/2 (direct gpt read)
- Rung 3 GEMMA-ONLY FRAC=97: JED_RS_ONLY=gemma -> publicScore = gemma_row/2 (confirms gemma maxed; completes split)
- Rung 4 GPT-ONLY FRAC=99: gpt headroom, isolated from gemma void-drag
- Rung 5 GPT-ONLY FRAC=99.5: gpt ceiling / void-boundary probe
Consistency check: rung1 ~= rung2 + rung3 (each isolated board = row/2).
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
CELL3 = ("import os\n"
         "from pathlib import Path\n"
         "sub=Path('/kaggle/working/submission.csv')\n"
         "try:\n"
         " import kaggle_evaluation.jed_attack_134815.jed_attack_inference_server as srv\n"
         " srv.JEDAttackInferenceServer().serve()\n"
         "except Exception as e:\n"
         " if os.getenv('KAGGLE_IS_COMPETITION_RERUN') is not None: raise\n"
         " print('skip',repr(e)[:60])\n"
         "if not sub.exists(): sub.write_text('Id,Score\\ngpt_oss_public,0.0\\ngpt_oss_private,0.0\\ngemma_public,0.0\\ngemma_private,0.0\\n')\n")


def env_cell(env, note):
    lines = ["import os"] + ["os.environ[%r]=%r" % (k, str(v)) for k, v in env.items()] + ["print(%r)" % note]
    return "\n".join(lines) + "\n"


def cc(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": src}


BASE = {"JED_REPLAY_SAFE": 1, "JED_EXFIL_PAYLOAD": "SECRET_MARKER", "JED_RS_TEMPLATES": "5,6"}
RUNGS = [
    ("submission_kernel_l13_anchor", "ahmedmobasher86/jed-public-pt-safe", "jed public pt safe",
     {**BASE, "JED_RS_FRAC": 97},
     "L13 ANCHOR: both boards FRAC=97 pool{close_ok,terse_ok} (~89.6 canary + floor)"),
    ("submission_kernel_l13_gpt97", "ahmedmobasher86/jed-public-pt-probe", "jed public pt probe",
     {**BASE, "JED_RS_FRAC": 97, "JED_RS_ONLY": "gpt"},
     "L13 SPLIT gpt-only FRAC=97 -> publicScore = gpt_row/2 (direct gpt read)"),
    ("submission_kernel_l13_gemma97", "ahmedmobasher86/jed-public-k1nx-1000", "jed public k1nx 1000",
     {**BASE, "JED_RS_FRAC": 97, "JED_RS_ONLY": "gemma"},
     "L13 SPLIT gemma-only FRAC=97 -> publicScore = gemma_row/2 (confirms gemma maxed)"),
    ("submission_kernel_l13_gpt99", "ahmedmobasher86/jed-public-k1nx-1200", "jed public k1nx 1200",
     {**BASE, "JED_RS_FRAC": 99, "JED_RS_ONLY": "gpt"},
     "L13 GPT CEILING gpt-only FRAC=99 (headroom, no gemma void-drag)"),
    ("submission_kernel_l13_blend96", "ahmedmobasher86/jed-public-k1nx-800", "jed public k1nx 800",
     {**BASE, "JED_RS_FRAC": 96},
     "L13 CLIMB BET: blended both-boards FRAC=96 (conservative; anchor is the blended peak)"),
]


def main():
    for d, slug, title, env, note in RUNGS:
        dd = ROOT / d
        dd.mkdir(exist_ok=True)
        nb = {"cells": [cc(CELL0), cc(env_cell(env, note)), cc(CELL2), cc(CELL3)],
              "metadata": {"kernelspec": {"language": "python", "name": "python3", "display_name": "Python 3"}},
              "nbformat": 4, "nbformat_minor": 5}
        (dd / "k.ipynb").write_text(json.dumps(nb))
        meta = {"id": slug, "title": title, "code_file": "k.ipynb", "language": "python",
                "kernel_type": "notebook", "is_private": True, "enable_gpu": True,
                "machine_shape": "NvidiaTeslaT4", "enable_internet": False,
                "competition_sources": ["ai-agent-security-multi-step-tool-attacks"]}
        (dd / "kernel-metadata.json").write_text(json.dumps(meta, indent=2))
        print(f"built {d} -> {slug}  FRAC={env.get('JED_RS_FRAC')} ONLY={env.get('JED_RS_ONLY','both')}")


if __name__ == "__main__":
    main()
