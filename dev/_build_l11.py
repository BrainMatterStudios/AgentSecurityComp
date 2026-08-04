"""Build L11 kernels. This batch tests Model-Specific Template Isolation and Ultra-Terse Squeeze for >112.
All rungs use JED_REPLAY_SAFE=1 with exact SECRET_MARKER payload.
- Rung 1: Anchor Control (FRAC=97, pool{close_ok,terse_ok})
- Rung 2: GPT-OSS Dedicated Close-OK (FRAC=97, template 5 channel-forge)
- Rung 3: Gemma Dedicated Terse-OK (FRAC=97, template 6 minimal-wrapup)
- Rung 4: GPT Bare-OK (FRAC=97, template 2 bare-ok)
- Rung 5: FRAC 98 Safety Squeeze (FRAC=98, margin 60s, pool{close_ok,terse_ok})
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


BASE = {"JED_REPLAY_SAFE": 1, "JED_EXFIL_PAYLOAD": "SECRET_MARKER"}
RUNGS = [
    ("submission_kernel_l11_anchor", "ahmedmobasher86/jed-public-pt-safe", "jed public pt safe",
     {**BASE, "JED_RS_FRAC": 97, "JED_RS_TEMPLATES": "5,6"},
     "L11 ANCHOR: K=1 single-post FRAC=97 pool{close_ok,terse_ok} (~89.6 canary)"),
    ("submission_kernel_l11_gpt_close", "ahmedmobasher86/jed-public-pt-probe", "jed public pt probe",
     {**BASE, "JED_RS_FRAC": 97, "JED_RS_TEMPLATES": "5"},
     "L11 GPT DEDICATED: FRAC=97 template 5 close_ok (0-reasoning channel-forge)"),
    ("submission_kernel_l11_gemma_terse", "ahmedmobasher86/jed-public-k1nx-1000", "jed public k1nx 1000",
     {**BASE, "JED_RS_FRAC": 97, "JED_RS_TEMPLATES": "6"},
     "L11 GEMMA DEDICATED: FRAC=97 template 6 terse_ok (minimal wrap-up)"),
    ("submission_kernel_l11_bare_ok", "ahmedmobasher86/jed-public-k1nx-1200", "jed public k1nx 1200",
     {**BASE, "JED_RS_FRAC": 97, "JED_RS_TEMPLATES": "2"},
     "L11 PROBE: FRAC=97 template 2 bare_ok"),
    ("submission_kernel_l11_squeeze", "ahmedmobasher86/jed-public-k1nx-800", "jed public k1nx 800",
     {**BASE, "JED_RS_FRAC": 98, "JED_RS_MARGIN": 60, "JED_RS_TEMPLATES": "5,6"},
     "L11 SQUEEZE: FRAC=98 MARGIN=60 pool{close_ok,terse_ok}"),
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
        print(f"built {d} -> {slug}  FRAC={env.get('JED_RS_FRAC')} pool={env.get('JED_RS_TEMPLATES')}")


if __name__ == "__main__":
    main()
