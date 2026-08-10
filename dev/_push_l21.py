#!/usr/bin/env python3
"""Push the five L21 kernels sequentially and record saved versions."""
import datetime as dt
import json
import os
import re
import subprocess
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "logs", "l21_push.log")
VJSON = os.path.join(ROOT, "logs", "l21_versions.json")

PENDING = [
    ("submission_kernel_l21_anchor", "ahmedmobasher86/jed-public-mp-anchor"),
    ("submission_kernel_l21_safe", "ahmedmobasher86/jed-public-mp-safe"),
    ("submission_kernel_l21_moderate", "ahmedmobasher86/jed-public-mp-moderate"),
    ("submission_kernel_l21_aggressive", "ahmedmobasher86/jed-public-mp-aggressive"),
    ("submission_kernel_l21_stretch", "ahmedmobasher86/jed-public-mp-stretch"),
]
VERSIONS = {}
MAX_PUSH_ATTEMPTS = int(os.getenv("L21_PUSH_ATTEMPTS", "30"))


def log(m):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    line = f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}Z  {m}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def status(slug):
    out = subprocess.run(
        ["python3", "-m", "kaggle", "kernels", "status", slug],
        capture_output=True,
        text=True,
        timeout=60,
    )
    return out.stdout + out.stderr


def push(d, slug):
    for attempt in range(MAX_PUSH_ATTEMPTS):
        out = subprocess.run(
            ["python3", "-m", "kaggle", "kernels", "push", "-p", os.path.join(ROOT, d)],
            capture_output=True,
            text=True,
            timeout=180,
        )
        txt = out.stdout + out.stderr
        m = re.search(r"version (\d+) successfully pushed", txt)
        if m:
            v = int(m.group(1))
            VERSIONS[slug] = v
            log(f"pushed {slug} -> v{v}")
            with open(VJSON, "w") as f:
                json.dump(VERSIONS, f, indent=2)
            return v
        if "Conflict" in txt or "version" in txt.lower():
            log(f"push {slug} attempt {attempt}: {txt.strip().splitlines()[-1][:120]}")
        time.sleep(15)
    log(f"FAILED to push {slug}")
    return None


def main():
    for d, slug in PENDING:
        if slug in VERSIONS:
            continue
        v = push(d, slug)
        if v is not None:
            time.sleep(2)
    log(f"L21 push done. versions={json.dumps(VERSIONS)}")


if __name__ == "__main__":
    main()
