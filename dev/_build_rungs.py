"""Build the idx13 ladder submission kernels by cloning the proven pt_safe notebook
structure (cells 0=SDK-path, 1=env, 2=base64 attack.py, 3=serve) and swapping the
env cell + re-embedding the CURRENT attack.py. Reuses existing kernel slugs
(new-kernel creation is account-capped)."""
import base64, json, copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "submission_kernel_pt_safe" / "k.ipynb"
ATTACK_B64 = base64.b64encode((ROOT / "attack.py").read_bytes()).decode()

def env_cell(env: dict, note: str) -> str:
    lines = ["import os"]
    for k, v in env.items():
        lines.append(f"os.environ[{k!r}]={v!r}")
    lines.append(f"print({note!r})")
    return "\n".join(lines)

def attack_cell() -> str:
    return ("import base64\n"
            f"open('/kaggle/working/attack.py','wb').write(base64.b64decode('{ATTACK_B64}'))")

RUNGS = [
 ("submission_kernel_base440",  "ahmedmobasher86/jed-public-pt-safe",   "jed public pt safe",
  {"JED_AGG_PROBE":"1","JED_GPTOSS_N":"440","JED_GEMMA_N":"560"},
  "BASELINE gpt440-natural + gemma560 (confirm current-regime ~45, de-risk gemma560)"),
 ("submission_kernel_i13_700",  "ahmedmobasher86/jed-public-pt-probe",  "jed public pt probe",
  {"JED_AGG_PROBE":"1","JED_GPTOSS_PROMPT":"13","JED_GPTOSS_N":"700","JED_GEMMA_N":"560"},
  "i13-preclose gpt700 + gemma560 (validates iff idx13 >=1.5x on Kaggle -> mean ~57)"),
 ("submission_kernel_i13_950",  "ahmedmobasher86/jed-public-k1nx-1000", "jed public k1nx 1000",
  {"JED_AGG_PROBE":"1","JED_GPTOSS_PROMPT":"13","JED_GPTOSS_N":"950","JED_GEMMA_N":"560"},
  "i13-preclose gpt950 + gemma560 (tests >=2x -> mean ~68)"),
 ("submission_kernel_i13_1250", "ahmedmobasher86/jed-public-k1nx-1200", "jed public k1nx 1200",
  {"JED_AGG_PROBE":"1","JED_GPTOSS_PROMPT":"13","JED_GPTOSS_N":"1250","JED_GEMMA_N":"560"},
  "i13-preclose gpt1250 + gemma560 (tests ~2.6x full transfer -> mean ~81)"),
]

nb0 = json.loads(TEMPLATE.read_text())
for dirname, slug, title, env, note in RUNGS:
    nb = copy.deepcopy(nb0)
    # cell 1 = env, cell 2 = attack.py embed (indices verified from pt_safe)
    nb["cells"][1]["source"] = env_cell(env, note)
    nb["cells"][2]["source"] = attack_cell()
    # clear any stored outputs/exec counts
    for c in nb["cells"]:
        if c.get("cell_type") == "code":
            c["outputs"] = []; c["execution_count"] = None
    d = ROOT / dirname
    d.mkdir(exist_ok=True)
    (d / "k.ipynb").write_text(json.dumps(nb))
    meta = {"id": slug, "title": title, "code_file": "k.ipynb", "language": "python",
            "kernel_type": "notebook", "is_private": True, "enable_gpu": True,
            "machine_shape": "NvidiaTeslaT4", "enable_internet": False,
            "competition_sources": ["ai-agent-security-multi-step-tool-attacks"]}
    (d / "kernel-metadata.json").write_text(json.dumps(meta, indent=2))
    print(f"built {dirname}  slug={slug}  env={env}")
print("done")
