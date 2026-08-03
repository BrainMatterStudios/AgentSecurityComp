"""Build L15 kernels — PER-MODEL FRAC (aim-higher) NIGHT.
The public score is throughput-bound near a per-board void wall. Every prior FRAC push
raised BOTH boards and gpt voids first (L13 gpt-only FRAC99 VOIDED), so gemma's headroom
above the shared 97 has NEVER been isolated. New knob JED_RS_FRAC_GPT / JED_RS_FRAC_GEMMA
sizes each board to its OWN FRAC after the fingerprint (verified: dev/_permodel_frac_smoke.py
-> reads+applies+fires, no crash). This is the one untested public aim-higher lever.
All exfil rungs JED_REPLAY_SAFE=1, pool {close_ok,terse_ok} (JED_RS_TEMPLATES=5,6), SECRET_MARKER.
- Rung 1 pt-safe   ANCHOR shared FRAC=97 -> ~89.6 (canary + floor; protects standing / insurance)
- Rung 2 pt-probe  ASYM gpt97 / gemma99  -> isolates gemma headroom (gpt held safe). THE aim-higher A/B.
- Rung 3 k1nx-1000 ASYM gpt98 / gemma99  -> push both toward the wall (aggressive climb)
- Rung 4 k1nx-1200 DEPUTY shared FRAC=95 -> private $50k hedge (clean CONFUSED_DEPUTY, all framings, both boards)
- Rung 5 k1nx-800  SHARED FRAC=98        -> code-independent climb (robust if the per-model knob misbehaves)
Read: rung2/rung3 vs rung1 => does gemma headroom exist (climb) or void/flat (wall confirmed).
rung5 => single-knob FRAC98 sanity. rung1 guarantees a banked draw; rung4 banks the private hedge.
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
    ("submission_kernel_l15_anchor", "ahmedmobasher86/jed-public-pt-safe", "jed public pt safe",
     {**BASE, "JED_RS_FRAC": 97},
     "L15 ANCHOR single-post shared FRAC=97 pool{close_ok,terse_ok} (~89.6 canary + floor)"),
    ("submission_kernel_l15_asym97_99", "ahmedmobasher86/jed-public-pt-probe", "jed public pt probe",
     {**BASE, "JED_RS_FRAC_GPT": 97, "JED_RS_FRAC_GEMMA": 99},
     "L15 ASYM gpt97/gemma99 -> isolate gemma FRAC headroom (gpt held safe). Aim-higher A/B vs anchor"),
    ("submission_kernel_l15_asym98_99", "ahmedmobasher86/jed-public-k1nx-1000", "jed public k1nx 1000",
     {**BASE, "JED_RS_FRAC_GPT": 98, "JED_RS_FRAC_GEMMA": 99},
     "L15 ASYM gpt98/gemma99 -> push both toward the void wall (aggressive climb)"),
    ("submission_kernel_l15_deputy", "ahmedmobasher86/jed-public-k1nx-1200", "jed public k1nx 1200",
     {"JED_REPLAY_SAFE": 1, "JED_EXFIL_PAYLOAD": "SECRET_MARKER", "JED_RS_CHANNEL": "deputy", "JED_RS_FRAC": 95},
     "L15 DEPUTY clean CONFUSED_DEPUTY FRAC=95 (all 5 framings, both boards) -> PRIVATE $50k hedge"),
    ("submission_kernel_l15_sharedf98", "ahmedmobasher86/jed-public-k1nx-800", "jed public k1nx 800",
     {**BASE, "JED_RS_FRAC": 98},
     "L15 SHARED FRAC=98 -> single-knob climb (code-independent insurance vs per-model knob)"),
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
        fr = env.get("JED_RS_FRAC", "%s/%s" % (env.get("JED_RS_FRAC_GPT", "-"), env.get("JED_RS_FRAC_GEMMA", "-")))
        print(f"built {d} -> {slug}  FRAC={fr} channel={env.get('JED_RS_CHANNEL','exfil')}")


if __name__ == "__main__":
    main()
