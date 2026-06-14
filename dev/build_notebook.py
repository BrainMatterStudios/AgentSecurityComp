"""Build the Kaggle submission notebook + metadata from attack.py."""
import base64
import json
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]

# Profiles: default (heavy) and lean (fast rerun). Lean sets env knobs that
# attack.py reads to shrink candidate count / tool-hops / search fraction.
PROFILE = sys.argv[1] if len(sys.argv) > 1 else "default"
PROFILES = {
    "default": {"dir": "submission_kernel", "id": "ahmedmobasher86/jed-multi-step-tool-attack",
                "title": "JED Multi-Step Tool Attack", "env": {}},
    "lean": {"dir": "submission_kernel_lean", "id": "ahmedmobasher86/jed-multi-step-tool-attack-lean",
             "title": "JED Multi-Step Tool Attack Lean",
             "env": {"JED_MAX_CANDIDATES": "240", "JED_MULTI_ENDPOINTS": "1",
                     "JED_MAX_PRIVATE_CHAINS": "60", "JED_SEARCH_FRACTION": "45"}},
    "ultralean": {"dir": "submission_kernel_ultralean", "id": "ahmedmobasher86/jed-multi-step-tool-attack-ultralean",
             "title": "JED Multi-Step Tool Attack Ultralean",
             "env": {"JED_MAX_CANDIDATES": "120", "JED_MULTI_ENDPOINTS": "1",
                     "JED_MAX_PRIVATE_CHAINS": "30", "JED_SEARCH_FRACTION": "22"}},
}
P = PROFILES[PROFILE]
KDIR = ROOT / P["dir"]
KDIR.mkdir(exist_ok=True)

attack_src = (ROOT / "attack.py").read_text()
b64 = base64.b64encode(attack_src.encode()).decode()

cell_bootstrap = (
    "import sys, os, glob\n"
    "from pathlib import Path\n"
    "sys.argv = [sys.argv[0]]\n"
    "for candidate in glob.glob('/kaggle/input/**/kaggle_evaluation', recursive=True):\n"
    "    root = str(Path(candidate).parent)\n"
    "    if root not in sys.path:\n"
    "        sys.path.insert(0, root)\n"
    "    print('Dataset root:', root)\n"
    "    break\n"
    "else:\n"
    "    raise RuntimeError('Attach the competition data source first.')\n"
    "sys.path.insert(0, '/kaggle/working')\n"
    "print('Setup complete')\n"
)

# Optional env-knob cell (lean profile). Must run before serve() loads attack.py.
_env_lines = "".join(
    f"os.environ['{k}'] = '{v}'\n" for k, v in P["env"].items()
)
cell_env = ("import os\n" + _env_lines + "print('profile env set:', "
            + repr(sorted(P["env"].keys())) + ")\n") if P["env"] else None

cell_writeattack = (
    "import base64\n"
    "ATTACK_B64 = " + repr(b64) + "\n"
    "with open('/kaggle/working/attack.py', 'wb') as f:\n"
    "    f.write(base64.b64decode(ATTACK_B64))\n"
    "print('Wrote /kaggle/working/attack.py')\n"
)

cell_serve = (
    "import os\n"
    "from pathlib import Path\n"
    "sub = Path('/kaggle/working/submission.csv')\n"
    "try:\n"
    "    import kaggle_evaluation.jed_attack_134815.jed_attack_inference_server as srv\n"
    "    srv.JEDAttackInferenceServer().serve()\n"
    "except Exception as exc:\n"
    "    if os.getenv('KAGGLE_IS_COMPETITION_RERUN') is not None:\n"
    "        raise\n"
    "    print('skipped (non-rerun):', repr(exc))\n"
    "# Ensure submission.csv exists for the submit handshake; the gateway overwrites\n"
    "# it with real per-model/per-guardrail scores during the competition rerun.\n"
    "if not sub.exists():\n"
    "    sub.write_text('Id,Score\\n'\n"
    "                   'gpt_oss_public,0.0\\ngpt_oss_private,0.0\\n'\n"
    "                   'gemma_public,0.0\\ngemma_private,0.0\\n')\n"
    "    print('wrote fallback submission.csv')\n"
)

def code(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": src.splitlines(keepends=True)}

def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}

_cells = [
    md(f"# {P['title']} — submission ({PROFILE} profile)\n\n"
       "Verify-and-keep red-team attack targeting the predicates reachable under the public "
       "OptimalGuardrail (EXFILTRATION, CONFUSED_DEPUTY) plus snapshot-branched untrusted->action "
       "chains for the private board. The lean profile shrinks candidate count and tool-hops via "
       "env knobs to keep the rerun wall-clock low."),
    code(cell_bootstrap),
]
if cell_env:
    _cells.append(code(cell_env))
_cells += [
    code(cell_writeattack),
    md("## Run the gateway\nStarts the inference server. During the competition rerun the "
       "gateway drives it against gpt-oss and gemma and writes `submission.csv`."),
    code(cell_serve),
]
nb = {
    "cells": _cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

_nbfile = "jed-multistep-tool-attack.ipynb"
(KDIR / _nbfile).write_text(json.dumps(nb, indent=1))

meta = {
    "id": P["id"],
    "title": P["title"],
    "code_file": _nbfile,
    "language": "python",
    "kernel_type": "notebook",
    "is_private": True,
    "enable_gpu": True,
    "enable_tpu": False,
    "enable_internet": False,
    "keywords": [],
    "dataset_sources": [],
    "kernel_sources": [],
    "competition_sources": ["ai-agent-security-multi-step-tool-attacks"],
    "model_sources": [],
    "machine_shape": "NvidiaTeslaT4",
}
(KDIR / "kernel-metadata.json").write_text(json.dumps(meta, indent=2))
print("Built notebook + metadata in", KDIR)
print("attack.py bytes:", len(attack_src), "b64 bytes:", len(b64))
