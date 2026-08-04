"""Build tomorrow's revised 5-slot ladder (push-both-boards). All gpt=idx13 preclose,
all gemma=natural. Reuses 5 existing slugs. Re-embeds current attack.py."""
import base64, json, copy
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
nb0 = json.loads((ROOT / "submission_kernel_pt_safe" / "k.ipynb").read_text())
B64 = base64.b64encode((ROOT / "attack.py").read_bytes()).decode()

# (dir, slug, title, gpt_N, gemma_N, mean_if_valid)
RUNGS = [
 ("l2_r1","ahmedmobasher86/jed-public-pt-safe",  "jed public pt safe",  740, 600, 60.3),
 ("l2_r2","ahmedmobasher86/jed-public-pt-probe", "jed public pt probe", 780, 640, 63.9),
 ("l2_r3","ahmedmobasher86/jed-public-k1nx-1000","jed public k1nx 1000",700, 720, 63.9),
 ("l2_r4","ahmedmobasher86/jed-public-k1nx-1200","jed public k1nx 1200",880, 560, 64.8),
 ("l2_r5","ahmedmobasher86/jed-public-k1nx-800", "jed public k1nx 800", 820, 700, 68.4),
]
for dn, slug, title, g, m, mean in RUNGS:
    nb = copy.deepcopy(nb0)
    env = {"JED_AGG_PROBE":"1","JED_GPTOSS_PROMPT":"13","JED_GPTOSS_N":str(g),"JED_GEMMA_N":str(m)}
    nb["cells"][1]["source"] = ("import os\n" + "".join(f"os.environ[{k!r}]={v!r}\n" for k,v in env.items())
                                + f"print('L2 gpt-idx13 N={g} + gemma-nat N={m} -> mean~{mean} if valid')")
    nb["cells"][2]["source"] = f"import base64\nopen('/kaggle/working/attack.py','wb').write(base64.b64decode('{B64}'))"
    for c in nb["cells"]:
        if c.get("cell_type") == "code": c["outputs"] = []; c["execution_count"] = None
    d = ROOT / f"submission_kernel_{dn}"; d.mkdir(exist_ok=True)
    (d / "k.ipynb").write_text(json.dumps(nb))
    (d / "kernel-metadata.json").write_text(json.dumps(
        {"id":slug,"title":title,"code_file":"k.ipynb","language":"python","kernel_type":"notebook",
         "is_private":True,"enable_gpu":True,"machine_shape":"NvidiaTeslaT4","enable_internet":False,
         "competition_sources":["ai-agent-security-multi-step-tool-attacks"]}, indent=2))
    print(f"built {dn}: gpt-idx13 {g} + gemma {m} -> {slug} (mean~{mean})")
print("done")
