"""Build L14 kernels — HOP-PACK NIGHT: test whether sequential hop-packing (JED_RS_HOPPACK)
amortizes Kaggle's per-candidate env-reset overhead and beats the 89.55 single-post plateau
(the only mechanistic path to the ~112 seen on the public LB).
All rungs JED_REPLAY_SAFE=1, pool {close_ok,terse_ok} (JED_RS_TEMPLATES=5,6), SECRET_MARKER.
- Rung 1 pt-safe  ANCHOR single-post FRAC=97 -> ~89.55 (canary + floor; protects standing)
- Rung 2 pt-probe HOPPACK=8 FRAC=97  -> direct A/B vs anchor (isolates the packing effect)
- Rung 3 k1nx-1000 HOPPACK=8 FRAC=85 -> void insurance (safe draw; confirms mechanism scores)
- Rung 4 k1nx-1200 HOPPACK=8 FRAC=93 -> FRAC curve / void-boundary between 85 and 97
- Rung 5 k1nx-800  HOPPACK=4 FRAC=93 -> K-slope vs rung 4 (is more packing better?)
Read: rung1 vs rung2 => reset-bound (big jump, 112 path) or decode-bound (flat). rung3<4<2 =>
FRAC curve. rung4 vs rung5 => K-slope. rung3 guarantees a read even if higher FRACs void.
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
    ("submission_kernel_l14_anchor", "ahmedmobasher86/jed-public-pt-safe", "jed public pt safe",
     {**BASE, "JED_RS_FRAC": 97},
     "L14 ANCHOR single-post FRAC=97 pool{close_ok,terse_ok} (~89.55 canary + floor)"),
    ("submission_kernel_l14_hp8f97", "ahmedmobasher86/jed-public-pt-probe", "jed public pt probe",
     {**BASE, "JED_RS_FRAC": 97, "JED_RS_HOPPACK": 8},
     "L14 HOPPACK K=8 FRAC=97 -> direct A/B vs anchor (does hop-packing beat single-post?)"),
    ("submission_kernel_l14_hp8f85", "ahmedmobasher86/jed-public-k1nx-1000", "jed public k1nx 1000",
     {**BASE, "JED_RS_FRAC": 85, "JED_RS_HOPPACK": 8},
     "L14 HOPPACK K=8 FRAC=85 -> void insurance (safe draw; confirms mechanism scores)"),
    ("submission_kernel_l14_hp8f93", "ahmedmobasher86/jed-public-k1nx-1200", "jed public k1nx 1200",
     {**BASE, "JED_RS_FRAC": 93, "JED_RS_HOPPACK": 8},
     "L14 HOPPACK K=8 FRAC=93 -> FRAC curve / void boundary"),
    ("submission_kernel_l14_hp4f93", "ahmedmobasher86/jed-public-k1nx-800", "jed public k1nx 800",
     {**BASE, "JED_RS_FRAC": 93, "JED_RS_HOPPACK": 4},
     "L14 HOPPACK K=4 FRAC=93 -> K-slope vs K=8 (amortization curve)"),
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
        print(f"built {d} -> {slug}  FRAC={env.get('JED_RS_FRAC')} HOPPACK={env.get('JED_RS_HOPPACK','off')}")


if __name__ == "__main__":
    main()
