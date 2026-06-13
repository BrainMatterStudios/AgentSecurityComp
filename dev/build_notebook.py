"""Build the Kaggle submission notebook + metadata from attack.py."""
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KDIR = ROOT / "submission_kernel"
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

nb = {
    "cells": [
        md("# JED Multi-Step Tool Attack — submission\n\n"
           "Verify-and-keep red-team attack targeting the two predicates reachable under the "
           "public OptimalGuardrail: EXFILTRATION (http.post to a clean host, secret in the body) "
           "and CONFUSED_DEPUTY (email.send via the messaging tool, avoiding share words). "
           "Multi-endpoint messages fire up to 8 posts per turn; candidates are individually "
           "verified live so replay wastes no budget."),
        code(cell_bootstrap),
        code(cell_writeattack),
        md("## Run the gateway\nStarts the inference server. During the competition rerun the "
           "gateway drives it against gpt-oss and gemma and writes `submission.csv`."),
        code(cell_serve),
    ],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

(KDIR / "jed-multistep-tool-attack.ipynb").write_text(json.dumps(nb, indent=1))

meta = {
    "id": "ahmedmobasher86/jed-multi-step-tool-attack",
    "title": "JED Multi-Step Tool Attack",
    "code_file": "jed-multistep-tool-attack.ipynb",
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
