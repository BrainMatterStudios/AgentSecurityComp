#!/usr/bin/env python3
"""Build the gpt-oss T4/CUDA diagnostic kernel (NON-submission; enable_gpu + internet).

Cells: (1) compile llama-cpp-python with CUDA + huggingface_hub, (2) discover aicomp_sdk
from the competition data source and write attack.py + the harness, (3) download the exact
gpt GGUF from HF (unsloth), (4) HARD-ASSERT gpu offload is active, then run the harness.
Output is read from the kernel log. Free GPU; zero submission slots.
"""
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATTACK_B64 = base64.b64encode((ROOT / "attack.py").read_bytes()).decode()
HARNESS_B64 = base64.b64encode((ROOT / "dev" / "_cuda_gemma_harness.py").read_bytes()).decode()

CELL_INSTALL = r'''
import subprocess, sys, os
def pip(*args, extra_env=None):
    env = dict(os.environ)
    if extra_env:
        env.update(extra_env)
    print("+ pip install", *args, flush=True)
    return subprocess.run([sys.executable, "-m", "pip", "install", "-q", *args], env=env).returncode
pip("huggingface_hub")
# CUDA build from source (deterministic; prebuilt wheels can silently be CPU-only)
rc = pip("llama-cpp-python", "--no-cache-dir", "--force-reinstall",
         extra_env={"CMAKE_ARGS": "-DGGML_CUDA=on", "FORCE_CMAKE": "1"})
if rc != 0:
    for tag in ("cu124", "cu122", "cu121"):
        if pip("llama-cpp-python", "--extra-index-url",
               "https://abetlen.github.io/llama-cpp-python/whl/" + tag) == 0:
            print("fell back to prebuilt wheel", tag, flush=True)
            break
import llama_cpp
print("llama_cpp", llama_cpp.__version__, flush=True)
try:
    print("gpu_offload_supported:", llama_cpp.llama_supports_gpu_offload(), flush=True)
except Exception as e:
    print("gpu check err:", repr(e), flush=True)
subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"])
'''

CELL_SETUP = (
    "import sys, glob, os, base64\n"
    "for p in glob.glob('/kaggle/input/**/kaggle_evaluation', recursive=True):\n"
    "    r = os.path.dirname(p)\n"
    "    if os.path.isdir(os.path.join(r, 'aicomp_sdk')): sys.path.insert(0, r); break\n"
    "sys.path.insert(0, '/kaggle/working')\n"
    "open('/kaggle/working/attack.py','wb').write(base64.b64decode('%s'))\n" % ATTACK_B64
    + "open('/kaggle/working/_cuda_gemma_harness.py','wb').write(base64.b64decode('%s'))\n" % HARNESS_B64
    + "import aicomp_sdk; print('aicomp_sdk OK from', aicomp_sdk.__file__, flush=True)\n"
)

CELL_DOWNLOAD = r'''
import os
from huggingface_hub import hf_hub_download, HfApi
REPO = "unsloth/gemma-4-26B-A4B-it-GGUF"
FN = "gemma-4-26B-A4B-it-UD-Q4_K_M.gguf"
path = None
try:
    path = hf_hub_download(repo_id=REPO, filename=FN)
except Exception as e:
    print("direct filename failed:", repr(e)[:140], flush=True)
    files = HfApi().list_repo_files(REPO)
    cand = [f for f in files if "Q4_K_M" in f and f.endswith(".gguf")]
    print("Q4_K_M candidates in repo:", cand, flush=True)
    if cand:
        path = hf_hub_download(repo_id=REPO, filename=cand[0])
assert path and os.path.exists(path), "GGUF download failed"
os.environ["CUDA_GGUF"] = path
print("GGUF:", path, round(os.path.getsize(path) / 1e9, 2), "GB", flush=True)
'''

CELL_RUN = r'''
import llama_cpp, runpy
assert llama_cpp.llama_supports_gpu_offload(), "CUDA NOT active in llama_cpp -> timings invalid; abort"
print("CUDA active; running harness...", flush=True)
runpy.run_path("/kaggle/working/_cuda_gemma_harness.py", run_name="__main__")
'''


def cc(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": src}


def main():
    d = ROOT / "submission_kernel_cuda_gemma"
    d.mkdir(exist_ok=True)
    nb = {
        "cells": [cc(CELL_INSTALL), cc(CELL_SETUP), cc(CELL_DOWNLOAD), cc(CELL_RUN)],
        "metadata": {"kernelspec": {"language": "python", "name": "python3", "display_name": "Python 3"}},
        "nbformat": 4, "nbformat_minor": 5,
    }
    (d / "k.ipynb").write_text(json.dumps(nb))
    meta = {
        "id": "ahmedmobasher86/jed-cuda-gemma",
        "title": "jed cuda gemma",
        "code_file": "k.ipynb",
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": True,
        "enable_internet": True,
        "competition_sources": ["ai-agent-security-multi-step-tool-attacks"],
    }
    (d / "kernel-metadata.json").write_text(json.dumps(meta, indent=2))
    print("built", d, "-> ahmedmobasher86/jed-cuda-gemma")


if __name__ == "__main__":
    main()
