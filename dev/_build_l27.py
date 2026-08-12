#!/usr/bin/env python3
"""L27 — the PROBE_HOPS=1 candidate-throughput lever (the real 83->130 gap). Both kernel-
mining agents found it in the winning kernels' OWN docstrings: the validation-fill normally
probes each candidate at 8 hops; but the EXFIL fires at hop-0, so probing at 1 hop validates
identically while skipping the wrap-up generation -> ~2x faster probe -> ~2x more firing
candidates land toward the 2000 cap (= the ~1.6x score jump). EVERY public kernel ships this
DISABLED (PROBE_HOPS=0) because a 1-hop probe under-counts the true 8-hop replay cost and
VOIDS unless REPLAY_COST_COEF scales it back up. This ladder sweeps that calibration from
SAFE (2.5) toward the boundary (1.8), with a PROBE_HOPS=0 baseline that can't void. Built on
dimong4's proven engine (patched src). 89.6 stays permanently banked. Single-post EXFIL
unchanged -- this is a throughput lever, not a mechanism change."""
import base64, json, re, py_compile, tempfile, os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC = Path("/tmp/d4.py").read_text()

def patch(src, **kv):
    out = src
    for const, val in kv.items():
        out, n = re.subn(rf"(?m)^{const}\s*=\s*[0-9.]+", f"{const} = {val}", out)
        assert n == 1, f"expected 1 match for {const}, got {n}"
    fd, tmp = tempfile.mkstemp(suffix=".py"); os.close(fd)
    Path(tmp).write_text(out); py_compile.compile(tmp, doraise=True); os.unlink(tmp)
    return out

CELL0 = ("import sys,glob,os\n"
         "for p in glob.glob('/kaggle/input/**/kaggle_evaluation',recursive=True):\n"
         " r=os.path.dirname(p)\n"
         " if os.path.isdir(os.path.join(r,'aicomp_sdk')): sys.path.insert(0,r); break\n"
         "sys.path.insert(0,'/kaggle/working'); print('setup')\n")
def cell2(b64): return ("import base64\nopen('/kaggle/working/attack.py','wb').write(base64.b64decode('%s'))\nprint('written')\n" % b64)
CELL3 = ("import os\nfrom pathlib import Path\nsub=Path('/kaggle/working/submission.csv')\n"
         "try:\n import kaggle_evaluation.jed_attack_134815.jed_attack_inference_server as srv\n"
         " srv.JEDAttackInferenceServer().serve()\n"
         "except Exception as e:\n"
         " if os.getenv('KAGGLE_IS_COMPETITION_RERUN') is not None: raise\n"
         " print('skip',repr(e)[:60])\n"
         "if not sub.exists(): sub.write_text('Id,Score\\ngpt_oss_public,0.0\\ngpt_oss_private,0.0\\ngemma_public,0.0\\ngemma_private,0.0\\n')\n")
def cc(s): return {"cell_type":"code","metadata":{},"execution_count":None,"outputs":[],"source":s}

# PROBE_HOPS=1 is the ENABLER (unbinds the gen phase); MULT/COEF is the single aggression
# dial (N proportional to MULT/COEF). Sweep the dial WIDE to bracket the void boundary
# where max candidates (~130) live, given R (true 8hop/1hop ratio, ~1.1 gpt .. ~2.0 gemma)
# is unmeasurable now (models gone). Rung 5 expresses the SAME aggression via MULT instead
# of COEF -> a board test that the two knobs collapse to one axis. Rung 1 can't void.
RUNGS = [
    ("submission_kernel_l27_base", "ahmedmobasher86/jed-public-pt-safe", "jed public pt safe",
     patch(SRC, REPLAY_SAFE_FRAC=0.98),
     "L27 baseline RSF=0.98 PROBE_HOPS=0 (safe control, aim ~83)"),
    ("submission_kernel_l27_ph1_c22", "ahmedmobasher86/jed-public-pt-probe", "jed public pt probe",
     patch(SRC, REPLAY_SAFE_FRAC=0.98, PROBE_HOPS=1, REPLAY_COST_COEF=2.2),
     "L27 PROBE_HOPS=1 COEF=2.2 (safe density lever; aggression 0.45)"),
    ("submission_kernel_l27_ph1_c19", "ahmedmobasher86/jed-public-k1nx-1000", "jed public k1nx 1000",
     patch(SRC, REPLAY_SAFE_FRAC=0.98, PROBE_HOPS=1, REPLAY_COST_COEF=1.9),
     "L27 PROBE_HOPS=1 COEF=1.9 (aggression 0.53)"),
    ("submission_kernel_l27_ph1_c16", "ahmedmobasher86/jed-public-k1nx-1200", "jed public k1nx 1200",
     patch(SRC, REPLAY_SAFE_FRAC=0.98, PROBE_HOPS=1, REPLAY_COST_COEF=1.6),
     "L27 PROBE_HOPS=1 COEF=1.6 (aggressive; aggression 0.63; near/at boundary)"),
    ("submission_kernel_l27_ph1_mult", "ahmedmobasher86/jed-public-k1nx-800", "jed public k1nx 800",
     patch(SRC, REPLAY_SAFE_FRAC=0.98, PROBE_HOPS=1, REPLAY_COST_COEF=2.2, REPLAY_BUDGET_MULT=1.4),
     "L27 PROBE_HOPS=1 COEF=2.2 MULT=1.4 (2nd knob; effective aggression 0.64 ~= COEF=1.6 twin -> collapse test)"),
]
def main():
    for d, slug, title, src, note in RUNGS:
        dd = ROOT / d; dd.mkdir(exist_ok=True)
        b64 = base64.b64encode(src.encode()).decode()
        nb = {"cells":[cc(CELL0),cc(cell2(b64)),cc(CELL3)],
              "metadata":{"kernelspec":{"language":"python","name":"python3","display_name":"Python 3"}},
              "nbformat":4,"nbformat_minor":5}
        (dd/"k.ipynb").write_text(json.dumps(nb))
        (dd/"kernel-metadata.json").write_text(json.dumps({"id":slug,"title":title,"code_file":"k.ipynb",
            "language":"python","kernel_type":"notebook","is_private":True,"enable_gpu":False,
            "enable_internet":False,"competition_sources":["ai-agent-security-multi-step-tool-attacks"]}, indent=2))
        print("built", d, "->", slug, "|", note)
if __name__ == "__main__": main()
