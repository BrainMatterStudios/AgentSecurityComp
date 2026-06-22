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
    "mforce1_400": {"dir": "submission_kernel_mforce1_400", "id": "ahmedmobasher86/jed-public-mforce1-400",
             "title": "JED Public MFORCE1_400", "env": {"JED_PUBLIC_MULTI": "1", "JED_MULTI_POSTS": "8", "JED_MULTI_PROMPT": "1", "JED_MAX_CANDIDATES": "400", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "mforce1_360": {"dir": "submission_kernel_mforce1_360", "id": "ahmedmobasher86/jed-public-mforce1-360",
             "title": "JED Public MFORCE1_360", "env": {"JED_PUBLIC_MULTI": "1", "JED_MULTI_POSTS": "8", "JED_MULTI_PROMPT": "1", "JED_MAX_CANDIDATES": "360", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "mforce5_130": {"dir": "submission_kernel_mforce5_130", "id": "ahmedmobasher86/jed-public-mforce5-130",
             "title": "JED Public MFORCE5_130", "env": {"JED_PUBLIC_MULTI": "1", "JED_MULTI_POSTS": "8", "JED_MULTI_PROMPT": "5", "JED_MAX_CANDIDATES": "130", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "mforce6_130": {"dir": "submission_kernel_mforce6_130", "id": "ahmedmobasher86/jed-public-mforce6-130",
             "title": "JED Public MFORCE6_130", "env": {"JED_PUBLIC_MULTI": "1", "JED_MULTI_POSTS": "8", "JED_MULTI_PROMPT": "6", "JED_MAX_CANDIDATES": "130", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "mforce7_130": {"dir": "submission_kernel_mforce7_130", "id": "ahmedmobasher86/jed-public-mforce7-130",
             "title": "JED Public MFORCE7_130", "env": {"JED_PUBLIC_MULTI": "1", "JED_MULTI_POSTS": "8", "JED_MULTI_PROMPT": "7", "JED_MAX_CANDIDATES": "130", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "mforce1_130": {"dir": "submission_kernel_mforce1_130", "id": "ahmedmobasher86/jed-public-mforce1-130",
             "title": "JED Public MFORCE1_130", "env": {"JED_PUBLIC_MULTI": "1", "JED_MULTI_POSTS": "8", "JED_MULTI_PROMPT": "1", "JED_MAX_CANDIDATES": "130", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "mforce2_130": {"dir": "submission_kernel_mforce2_130", "id": "ahmedmobasher86/jed-public-mforce2-130",
             "title": "JED Public MFORCE2_130", "env": {"JED_PUBLIC_MULTI": "1", "JED_MULTI_POSTS": "8", "JED_MULTI_PROMPT": "2", "JED_MAX_CANDIDATES": "130", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "mforce3_130": {"dir": "submission_kernel_mforce3_130", "id": "ahmedmobasher86/jed-public-mforce3-130",
             "title": "JED Public MFORCE3_130", "env": {"JED_PUBLIC_MULTI": "1", "JED_MULTI_POSTS": "8", "JED_MULTI_PROMPT": "3", "JED_MAX_CANDIDATES": "130", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "mforce4_130": {"dir": "submission_kernel_mforce4_130", "id": "ahmedmobasher86/jed-public-mforce4-130",
             "title": "JED Public MFORCE4_130", "env": {"JED_PUBLIC_MULTI": "1", "JED_MULTI_POSTS": "8", "JED_MULTI_PROMPT": "4", "JED_MAX_CANDIDATES": "130", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "k1_660": {"dir": "submission_kernel_k1_660", "id": "ahmedmobasher86/jed-public-k1-660",
             "title": "JED Public K1_660", "env": {"JED_K1_SHORT": "1", "JED_MAX_CANDIDATES": "660", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "k1_680": {"dir": "submission_kernel_k1_680", "id": "ahmedmobasher86/jed-public-k1-680",
             "title": "JED Public K1_680",
             "env": {"JED_K1_SHORT": "1", "JED_MAX_CANDIDATES": "680", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "k1_700": {"dir": "submission_kernel_k1_700", "id": "ahmedmobasher86/jed-public-k1-700",
             "title": "JED Public K1_700",
             "env": {"JED_K1_SHORT": "1", "JED_MAX_CANDIDATES": "700", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "k1_720": {"dir": "submission_kernel_k1_720", "id": "ahmedmobasher86/jed-public-k1-720",
             "title": "JED Public K1_720",
             "env": {"JED_K1_SHORT": "1", "JED_MAX_CANDIDATES": "720", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "k1_740": {"dir": "submission_kernel_k1_740", "id": "ahmedmobasher86/jed-public-k1-740",
             "title": "JED Public K1_740",
             "env": {"JED_K1_SHORT": "1", "JED_MAX_CANDIDATES": "740", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "multi8_110": {"dir": "submission_kernel_multi8_110", "id": "ahmedmobasher86/jed-public-multi8-110",
             "title": "JED Public multi8_110",
             "env": {"JED_PUBLIC_MULTI": "1", "JED_MULTI_TINY": "1", "JED_MULTI_POSTS": "8",
                     "JED_MAX_CANDIDATES": "110", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "multi8_130": {"dir": "submission_kernel_multi8_130", "id": "ahmedmobasher86/jed-public-multi8-130",
             "title": "JED Public multi8_130",
             "env": {"JED_PUBLIC_MULTI": "1", "JED_MULTI_TINY": "1", "JED_MULTI_POSTS": "8",
                     "JED_MAX_CANDIDATES": "130", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "multi6_160": {"dir": "submission_kernel_multi6_160", "id": "ahmedmobasher86/jed-public-multi6-160",
             "title": "JED Public multi6_160",
             "env": {"JED_PUBLIC_MULTI": "1", "JED_MULTI_TINY": "1", "JED_MULTI_POSTS": "6",
                     "JED_MAX_CANDIDATES": "160", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "multi4_220": {"dir": "submission_kernel_multi4_220", "id": "ahmedmobasher86/jed-public-multi4-220",
             "title": "JED Public multi4_220",
             "env": {"JED_PUBLIC_MULTI": "1", "JED_MULTI_TINY": "1", "JED_MULTI_POSTS": "4",
                     "JED_MAX_CANDIDATES": "220", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "multi2_400": {"dir": "submission_kernel_multi2_400", "id": "ahmedmobasher86/jed-public-multi2-400",
             "title": "JED Public multi2_400",
             "env": {"JED_PUBLIC_MULTI": "1", "JED_MULTI_TINY": "1", "JED_MULTI_POSTS": "2",
                     "JED_MAX_CANDIDATES": "400", "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "lean": {"dir": "submission_kernel_lean", "id": "ahmedmobasher86/jed-multi-step-tool-attack-lean",
             "title": "JED Multi-Step Tool Attack Lean",
             "env": {"JED_MAX_CANDIDATES": "240", "JED_MULTI_ENDPOINTS": "1",
                     "JED_MAX_PRIVATE_CHAINS": "60", "JED_SEARCH_FRACTION": "45"}},
    "ultralean": {"dir": "submission_kernel_ultralean", "id": "ahmedmobasher86/jed-multi-step-tool-attack-ultralean",
             "title": "JED Multi-Step Tool Attack Ultralean",
             "env": {"JED_MAX_CANDIDATES": "100", "JED_MULTI_ENDPOINTS": "1",
                     "JED_MAX_PRIVATE_CHAINS": "25", "JED_SEARCH_FRACTION": "12"}},
    "scaled": {"dir": "submission_kernel_scaled", "id": "ahmedmobasher86/jed-multi-step-tool-attack-scaled",
             "title": "JED Multi-Step Tool Attack Scaled",
             "env": {"JED_MAX_CANDIDATES": "250", "JED_MULTI_ENDPOINTS": "1",
                     "JED_MAX_PRIVATE_CHAINS": "70", "JED_SEARCH_FRACTION": "15"}},
    "big": {"dir": "submission_kernel_big", "id": "ahmedmobasher86/jed-multi-step-tool-attack-big",
             "title": "JED Multi-Step Tool Attack Big",
             "env": {"JED_MAX_CANDIDATES": "400", "JED_MULTI_ENDPOINTS": "1",
                     "JED_MAX_PRIVATE_CHAINS": "110", "JED_SEARCH_FRACTION": "16"}},
    "public_dense_650": {"dir": "submission_kernel_public_dense_650",
             "id": "ahmedmobasher86/jed-public-dense-650",
             "title": "JED Public Dense 650",
             "env": {"JED_PUBLIC_DENSE": "1", "JED_MAX_CANDIDATES": "650",
                     "JED_MULTI_ENDPOINTS": "1", "JED_MAX_PRIVATE_CHAINS": "0",
                     "JED_SEARCH_FRACTION": "1", "JED_DENSE_VERIFY": "0"}},
    "public_dense_620_c1": {"dir": "submission_kernel_public_dense_620_c1",
             "id": "ahmedmobasher86/jed-public-dense-620-c1",
             "title": "JED Public Dense 620 C1",
             "env": {"JED_PUBLIC_DENSE": "1", "JED_MAX_CANDIDATES": "620",
                     "JED_MULTI_ENDPOINTS": "1", "JED_MAX_PRIVATE_CHAINS": "0",
                     "JED_SEARCH_FRACTION": "1", "JED_DENSE_VERIFY": "0",
                     "JED_DENSE_VARIANTS": "1", "JED_DENSE_SHORT_HOST": "1"}},
    "public_dense_800": {"dir": "submission_kernel_public_dense_800",
             "id": "ahmedmobasher86/jed-public-dense-800",
             "title": "JED Public Dense 800",
             "env": {"JED_PUBLIC_DENSE": "1", "JED_MAX_CANDIDATES": "800",
                     "JED_MULTI_ENDPOINTS": "1", "JED_MAX_PRIVATE_CHAINS": "0",
                     "JED_SEARCH_FRACTION": "1", "JED_DENSE_VERIFY": "0",
                     "JED_DENSE_VARIANTS": "1", "JED_DENSE_SHORT_HOST": "1"}},
    "public_dense_900": {"dir": "submission_kernel_public_dense_900",
             "id": "ahmedmobasher86/jed-public-dense-900",
             "title": "JED Public Dense 900",
             "env": {"JED_PUBLIC_DENSE": "1", "JED_MAX_CANDIDATES": "900",
                     "JED_MULTI_ENDPOINTS": "1", "JED_MAX_PRIVATE_CHAINS": "0",
                     "JED_SEARCH_FRACTION": "1", "JED_DENSE_VERIFY": "0",
                     "JED_DENSE_VARIANTS": "1", "JED_DENSE_SHORT_HOST": "1"}},
    "public_dense_1000": {"dir": "submission_kernel_public_dense_1000",
             "id": "ahmedmobasher86/jed-public-dense-1000",
             "title": "JED Public Dense 1000",
             "env": {"JED_PUBLIC_DENSE": "1", "JED_MAX_CANDIDATES": "1000",
                     "JED_MULTI_ENDPOINTS": "1", "JED_MAX_PRIVATE_CHAINS": "0",
                     "JED_SEARCH_FRACTION": "1", "JED_DENSE_VERIFY": "0",
                     "JED_DENSE_VARIANTS": "1", "JED_DENSE_SHORT_HOST": "1"}},
    "public_dense_900_nomarker": {"dir": "submission_kernel_public_dense_900_nomarker",
             "id": "ahmedmobasher86/jed-public-dense-900-nomarker",
             "title": "JED Public Dense 900 No Marker",
             "env": {"JED_PUBLIC_DENSE": "1", "JED_MAX_CANDIDATES": "900",
                     "JED_MULTI_ENDPOINTS": "1", "JED_MAX_PRIVATE_CHAINS": "0",
                     "JED_SEARCH_FRACTION": "1", "JED_DENSE_VERIFY": "0",
                     "JED_DENSE_VARIANTS": "1", "JED_DENSE_SHORT_HOST": "1",
                     "JED_DENSE_TOKEN_COUNT": "8"}},
    "public_dense_840_c3": {"dir": "submission_kernel_public_dense_840_c3",
             "id": "ahmedmobasher86/jed-public-dense-840-c3",
             "title": "JED Public Dense 840 C3",
             "env": {"JED_PUBLIC_DENSE": "1", "JED_MAX_CANDIDATES": "840",
                     "JED_MULTI_ENDPOINTS": "1", "JED_MAX_PRIVATE_CHAINS": "0",
                     "JED_SEARCH_FRACTION": "1", "JED_DENSE_VERIFY": "0",
                     "JED_DENSE_VARIANTS": "3", "JED_DENSE_SHORT_HOST": "1"}},
    "public_dense_864_c3": {"dir": "submission_kernel_public_dense_864_c3",
             "id": "ahmedmobasher86/jed-public-dense-864-c3",
             "title": "JED Public Dense 864 C3",
             "env": {"JED_PUBLIC_DENSE": "1", "JED_MAX_CANDIDATES": "864",
                     "JED_MULTI_ENDPOINTS": "1", "JED_MAX_PRIVATE_CHAINS": "0",
                     "JED_SEARCH_FRACTION": "1", "JED_DENSE_VERIFY": "0",
                     "JED_DENSE_VARIANTS": "3", "JED_DENSE_SHORT_HOST": "1"}},
    "public_dense_900_c3": {"dir": "submission_kernel_public_dense_900_c3",
             "id": "ahmedmobasher86/jed-public-dense-900-c3",
             "title": "JED Public Dense 900 C3",
             "env": {"JED_PUBLIC_DENSE": "1", "JED_MAX_CANDIDATES": "900",
                     "JED_MULTI_ENDPOINTS": "1", "JED_MAX_PRIVATE_CHAINS": "0",
                     "JED_SEARCH_FRACTION": "1", "JED_DENSE_VERIFY": "0",
                     "JED_DENSE_VARIANTS": "3", "JED_DENSE_SHORT_HOST": "1"}},
    "public_dense_1000_c3": {"dir": "submission_kernel_public_dense_1000_c3",
             "id": "ahmedmobasher86/jed-public-dense-1000-c3",
             "title": "JED Public Dense 1000 C3",
             "env": {"JED_PUBLIC_DENSE": "1", "JED_MAX_CANDIDATES": "1000",
                     "JED_MULTI_ENDPOINTS": "1", "JED_MAX_PRIVATE_CHAINS": "0",
                     "JED_SEARCH_FRACTION": "1", "JED_DENSE_VERIFY": "0",
                     "JED_DENSE_VARIANTS": "3", "JED_DENSE_SHORT_HOST": "1"}},
    "public_multi8_150": {"dir": "submission_kernel_public_multi8_150",
             "id": "ahmedmobasher86/jed-public-multi8-150",
             "title": "JED Public Multi8 150",
             "env": {"JED_PUBLIC_MULTI": "1", "JED_MAX_CANDIDATES": "150",
                     "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1",
                     "JED_MULTI_POSTS": "8", "JED_MULTI_VARIANTS": "4",
                     "JED_DENSE_TOKEN_COUNT": "8"}},
    "public_multi8_180": {"dir": "submission_kernel_public_multi8_180",
             "id": "ahmedmobasher86/jed-public-multi8-180",
             "title": "JED Public Multi8 180",
             "env": {"JED_PUBLIC_MULTI": "1", "JED_MAX_CANDIDATES": "180",
                     "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1",
                     "JED_MULTI_POSTS": "8", "JED_MULTI_VARIANTS": "4",
                     "JED_DENSE_TOKEN_COUNT": "8"}},
    "public_tiny_864": {"dir": "submission_kernel_public_tiny_864",
             "id": "ahmedmobasher86/jed-public-tiny-864",
             "title": "JED Public Tiny 864",
             "env": {"JED_PUBLIC_DENSE": "1", "JED_DENSE_TINY": "1",
                     "JED_MAX_CANDIDATES": "864", "JED_MAX_PRIVATE_CHAINS": "0",
                     "JED_SEARCH_FRACTION": "1", "JED_DENSE_VERIFY": "0",
                     "JED_DENSE_VARIANTS": "1", "JED_DENSE_TOKEN_COUNT": "1"}},
    "public_tiny_1000": {"dir": "submission_kernel_public_tiny_1000",
             "id": "ahmedmobasher86/jed-public-tiny-1000",
             "title": "JED Public Tiny 1000",
             "env": {"JED_PUBLIC_DENSE": "1", "JED_DENSE_TINY": "1",
                     "JED_MAX_CANDIDATES": "1000", "JED_MAX_PRIVATE_CHAINS": "0",
                     "JED_SEARCH_FRACTION": "1", "JED_DENSE_VERIFY": "0",
                     "JED_DENSE_VARIANTS": "1", "JED_DENSE_TOKEN_COUNT": "1"}},
    "public_tiny_1200": {"dir": "submission_kernel_public_tiny_1200",
             "id": "ahmedmobasher86/jed-public-tiny-1200",
             "title": "JED Public Tiny 1200",
             "env": {"JED_PUBLIC_DENSE": "1", "JED_DENSE_TINY": "1",
                     "JED_MAX_CANDIDATES": "1200", "JED_MAX_PRIVATE_CHAINS": "0",
                     "JED_SEARCH_FRACTION": "1", "JED_DENSE_VERIFY": "0",
                     "JED_DENSE_VARIANTS": "1", "JED_DENSE_TOKEN_COUNT": "1"}},
    "public_tiny_1500": {"dir": "submission_kernel_public_tiny_1500",
             "id": "ahmedmobasher86/jed-public-tiny-1500",
             "title": "JED Public Tiny 1500",
             "env": {"JED_PUBLIC_DENSE": "1", "JED_DENSE_TINY": "1",
                     "JED_MAX_CANDIDATES": "1500", "JED_MAX_PRIVATE_CHAINS": "0",
                     "JED_SEARCH_FRACTION": "1", "JED_DENSE_VERIFY": "0",
                     "JED_DENSE_VARIANTS": "1", "JED_DENSE_TOKEN_COUNT": "1"}},
    "public_multitiny8_180": {"dir": "submission_kernel_public_multitiny8_180",
             "id": "ahmedmobasher86/jed-public-multitiny8-180",
             "title": "JED Public MultiTiny8 180",
             "env": {"JED_PUBLIC_MULTI": "1", "JED_MULTI_TINY": "1",
                     "JED_MAX_CANDIDATES": "180", "JED_MAX_PRIVATE_CHAINS": "0",
                     "JED_SEARCH_FRACTION": "1", "JED_MULTI_POSTS": "8",
                     "JED_MULTI_VARIANTS": "1", "JED_DENSE_TOKEN_COUNT": "1"}},
    "public_multitiny8_240": {"dir": "submission_kernel_public_multitiny8_240",
             "id": "ahmedmobasher86/jed-public-multitiny8-240",
             "title": "JED Public MultiTiny8 240",
             "env": {"JED_PUBLIC_MULTI": "1", "JED_MULTI_TINY": "1",
                     "JED_MAX_CANDIDATES": "240", "JED_MAX_PRIVATE_CHAINS": "0",
                     "JED_SEARCH_FRACTION": "1", "JED_MULTI_POSTS": "8",
                     "JED_MULTI_VARIANTS": "1", "JED_DENSE_TOKEN_COUNT": "1"}},
    "public_k1_620": {"dir": "submission_kernel_public_k1_620",
             "id": "ahmedmobasher86/jed-public-k1-620",
             "title": "JED Public K1 620",
             "env": {"JED_K1_SHORT": "1", "JED_MAX_CANDIDATES": "620",
                     "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "public_k1_745": {"dir": "submission_kernel_public_k1_745",
             "id": "ahmedmobasher86/jed-public-k1-745",
             "title": "JED Public K1 745",
             "env": {"JED_K1_SHORT": "1", "JED_MAX_CANDIDATES": "745",
                     "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "public_k1_1000": {"dir": "submission_kernel_public_k1_1000",
             "id": "ahmedmobasher86/jed-public-k1-1000",
             "title": "JED Public K1 1000",
             "env": {"JED_K1_SHORT": "1", "JED_MAX_CANDIDATES": "1000",
                     "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "public_k1_1200": {"dir": "submission_kernel_public_k1_1200",
             "id": "ahmedmobasher86/jed-public-k1-1200-v2",
             "title": "JED Public K1 1200 V2",
             "env": {"JED_K1_SHORT": "1", "JED_MAX_CANDIDATES": "1200",
                     "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
    "public_k1_1500": {"dir": "submission_kernel_public_k1_1500",
             "id": "ahmedmobasher86/jed-public-k1-1500-v2",
             "title": "JED Public K1 1500 V2",
             "env": {"JED_K1_SHORT": "1", "JED_MAX_CANDIDATES": "1500",
                     "JED_MAX_PRIVATE_CHAINS": "0", "JED_SEARCH_FRACTION": "1"}},
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
