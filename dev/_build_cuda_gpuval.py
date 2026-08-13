#!/usr/bin/env python3
"""Build the GPU-vs-CPU validation replica (enable_gpu:true, internet:true, non-submission).
Cell 0 checks the DEFAULT llama_cpp CUDA capability in a subprocess FIRST (this is Q1 = what
the no-internet enable_gpu:true rerun would see), THEN force-installs a CUDA build so the
harness can measure GPU-vs-CPU decode speed (Q2)."""
import base64, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ATTACK_B64 = base64.b64encode((ROOT / "attack.py").read_bytes()).decode()
HARNESS_B64 = base64.b64encode((ROOT / "dev" / "_cuda_gpuval.py").read_bytes()).decode()

CELL_INSTALL = r'''
import subprocess, sys, os
# --- Q1: does the DEFAULT env already have a CUDA-capable llama_cpp? (fresh subprocess) ---
q1 = subprocess.run([sys.executable,"-c",
    "import importlib.util as u;\n"
    "spec=u.find_spec('llama_cpp')\n"
    "print('DEFAULT_LLAMA_CPP_PRESENT=', spec is not None)\n"
    "import llama_cpp; print('DEFAULT_VERSION=', llama_cpp.__version__); "
    "print('DEFAULT_CUDA_OFFLOAD=', llama_cpp.llama_supports_gpu_offload())"],
    capture_output=True, text=True)
print("=== Q1 DEFAULT llama_cpp (what the no-internet rerun sees) ===", flush=True)
print(q1.stdout or "(no llama_cpp import)", (q1.stderr[:200] if q1.returncode else ""), flush=True)
print("=> if DEFAULT_CUDA_OFFLOAD=True, enable_gpu:true submission works out-of-the-box; "
      "if False/absent, must bundle a CUDA wheel dataset for the rerun.\n", flush=True)
def pip(*a, extra_env=None):
    env=dict(os.environ); env.update(extra_env or {})
    return subprocess.run([sys.executable,"-m","pip","install","-q",*a], env=env).returncode
pip("huggingface_hub")
# force a CUDA build so Q2 (the speedup measurement) is valid regardless of the default
rc = pip("llama-cpp-python","--no-cache-dir","--force-reinstall",
         extra_env={"CMAKE_ARGS":"-DGGML_CUDA=on","FORCE_CMAKE":"1"})
if rc != 0:
    for tag in ("cu124","cu122","cu121"):
        if pip("llama-cpp-python","--extra-index-url","https://abetlen.github.io/llama-cpp-python/whl/"+tag)==0: break
import llama_cpp; print("measurement llama_cpp", llama_cpp.__version__, "CUDA", llama_cpp.llama_supports_gpu_offload(), flush=True)
'''
CELL_SETUP = ("import sys, glob, os, base64\n"
    "for p in glob.glob('/kaggle/input/**/kaggle_evaluation', recursive=True):\n"
    "    r = os.path.dirname(p)\n"
    "    if os.path.isdir(os.path.join(r,'aicomp_sdk')): sys.path.insert(0,r); break\n"
    "sys.path.insert(0,'/kaggle/working')\n"
    "open('/kaggle/working/attack.py','wb').write(base64.b64decode('%s'))\n" % ATTACK_B64
    + "open('/kaggle/working/_cuda_gpuval.py','wb').write(base64.b64decode('%s'))\n" % HARNESS_B64
    + "import aicomp_sdk; print('aicomp_sdk OK', flush=True)\n")
CELL_RUN = ('import runpy\nrunpy.run_path("/kaggle/working/_cuda_gpuval.py", run_name="__main__")\n')

def cc(s): return {"cell_type":"code","metadata":{},"execution_count":None,"outputs":[],"source":s}
def main():
    d = ROOT / "submission_kernel_cuda_gpuval"; d.mkdir(exist_ok=True)
    nb = {"cells":[cc(CELL_INSTALL),cc(CELL_SETUP),cc(CELL_RUN)],
          "metadata":{"kernelspec":{"language":"python","name":"python3","display_name":"Python 3"}},
          "nbformat":4,"nbformat_minor":5}
    (d/"k.ipynb").write_text(json.dumps(nb))
    (d/"kernel-metadata.json").write_text(json.dumps({"id":"ahmedmobasher86/jed-cuda-gpuval","title":"jed cuda gpuval",
        "code_file":"k.ipynb","language":"python","kernel_type":"notebook","is_private":True,
        "enable_gpu":True,"enable_internet":True,
        "competition_sources":["ai-agent-security-multi-step-tool-attacks"]}, indent=2))
    print("built", d, "-> jed-cuda-gpuval")
if __name__ == "__main__": main()
