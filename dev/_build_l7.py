"""Build L7 kernels: re-embed the CURRENT attack.py (with close_ok/terse_ok
templates) + per-rung env, into the 4-cell replay-safe kernel structure.
Reuses existing slugs. Writes k.ipynb + kernel-metadata.json into each dir.
Push separately (batches of 2). Usage: python3 dev/_build_l7.py
"""
import base64, json, os
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


def env_cell(env: dict, note: str) -> str:
    lines = ["import os"]
    for k, v in env.items():
        lines.append("os.environ[%r]=%r" % (k, str(v)))
    lines.append("print(%r)" % note)
    return "\n".join(lines) + "\n"


def code_cell(src: str) -> dict:
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": src}


# (dir, slug, title, env, note)
RUNGS = [
    ("submission_kernel_l7_floor", "ahmedmobasher86/jed-public-pt-safe", "jed public pt safe",
     {"JED_REPLAY_SAFE": 1, "JED_RS_FRAC": 95, "JED_EXFIL_PAYLOAD": "SECRET_MARKER"},
     "L7 FLOOR: replay-safe FRAC=95 bare-marker all-templates (safe >80)"),
    ("submission_kernel_l7_ctrl", "ahmedmobasher86/jed-public-pt-probe", "jed public pt probe",
     {"JED_REPLAY_SAFE": 1, "JED_RS_FRAC": 99, "JED_EXFIL_PAYLOAD": "SECRET_MARKER", "JED_RS_TEMPLATES": "0,1,2,3,4"},
     "L7 CONTROL: FRAC=99 bare NO close_ok (old 5 templates) -> isolates the lever"),
    ("submission_kernel_l7_max", "ahmedmobasher86/jed-public-k1nx-1000", "jed public k1nx 1000",
     {"JED_REPLAY_SAFE": 1, "JED_RS_FRAC": 99, "JED_EXFIL_PAYLOAD": "SECRET_MARKER"},
     "L7 MAX PLAY: FRAC=99 bare close_ok-enabled (the 20pct decode-cut lever)"),
    ("submission_kernel_l7_mid", "ahmedmobasher86/jed-public-k1nx-1200", "jed public k1nx 1200",
     {"JED_REPLAY_SAFE": 1, "JED_RS_FRAC": 97, "JED_EXFIL_PAYLOAD": "SECRET_MARKER"},
     "L7 MID: FRAC=97 bare close_ok-enabled (safety rung of the max play)"),
    ("submission_kernel_l7_ceil", "ahmedmobasher86/jed-public-k1nx-800", "jed public k1nx 800",
     {"JED_REPLAY_SAFE": 1, "JED_RS_FRAC": 99.5, "JED_EXFIL_PAYLOAD": "SECRET_MARKER"},
     "L7 CEILING PROBE: FRAC=99.5 bare close_ok-enabled (max squeeze)"),
]


def main():
    for d, slug, title, env, note in RUNGS:
        dd = ROOT / d
        dd.mkdir(exist_ok=True)
        nb = {"cells": [code_cell(CELL0), code_cell(env_cell(env, note)),
                        code_cell(CELL2), code_cell(CELL3)],
              "metadata": {"kernelspec": {"language": "python", "name": "python3", "display_name": "Python 3"}},
              "nbformat": 4, "nbformat_minor": 5}
        (dd / "k.ipynb").write_text(json.dumps(nb))
        meta = {"id": slug, "title": title, "code_file": "k.ipynb", "language": "python",
                "kernel_type": "notebook", "is_private": True, "enable_gpu": True,
                "machine_shape": "NvidiaTeslaT4", "enable_internet": False,
                "competition_sources": ["ai-agent-security-multi-step-tool-attacks"]}
        (dd / "kernel-metadata.json").write_text(json.dumps(meta, indent=2))
        print(f"built {d} -> {slug}  FRAC={env['JED_RS_FRAC']} tmpl={env.get('JED_RS_TEMPLATES','ALL')}")
    print("\nattack.py b64 len:", len(ATTACK_B64))


if __name__ == "__main__":
    main()
