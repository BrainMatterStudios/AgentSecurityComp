#!/usr/bin/env python3
"""Push the five L22 amortization-A/B kernels sequentially and record versions."""
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "logs", "l24_push.log")
VJSON = os.path.join(ROOT, "logs", "l24_versions.json")

PENDING = [
    ("submission_kernel_l24_base", "ahmedmobasher86/jed-public-pt-safe"),
    ("submission_kernel_l24_g1600", "ahmedmobasher86/jed-public-pt-probe"),
    ("submission_kernel_l24_g2000", "ahmedmobasher86/jed-public-k1nx-1000"),
    ("submission_kernel_l24_both2000", "ahmedmobasher86/jed-public-k1nx-1200"),
    ("submission_kernel_l24_both1400", "ahmedmobasher86/jed-public-k1nx-800"),
]
VERSIONS = {}
MAX_PUSH_ATTEMPTS = int(os.getenv("L22_PUSH_ATTEMPTS", "30"))


def log(m):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    line = f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}Z  {m}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def status(slug):
    out = subprocess.run(["python3", "-m", "kaggle", "kernels", "status", slug],
                         capture_output=True, text=True, timeout=60)
    return out.stdout + out.stderr


def push(d, slug):
    for attempt in range(MAX_PUSH_ATTEMPTS):
        out = subprocess.run(
            ["python3", "-m", "kaggle", "kernels", "push", "-p", os.path.join(ROOT, d)],
            capture_output=True, text=True, timeout=180)
        txt = out.stdout + out.stderr
        m = re.search(r"version (\d+) successfully pushed", txt)
        if m:
            v = int(m.group(1))
            VERSIONS[slug] = v
            log(f"pushed {slug} -> v{v}")
            with open(VJSON, "w") as f:
                json.dump(VERSIONS, f, indent=2)
            return v
        if "session count" in txt or "batch GPU" in txt or "maximum" in txt.lower():
            log(f"{slug}: resource cap reached, waiting 60s (attempt {attempt + 1})")
            time.sleep(60)
            continue
        tail = txt.strip().splitlines()[-1] if txt.strip() else repr(txt)
        log(f"{slug}: unexpected push output: {tail}")
        time.sleep(30)
    log(f"{slug}: FAILED to push after retries")
    return None


def main():
    log("L22 sequential CPU-save push start (5 kernels).")
    for d, slug in PENDING:
        v = push(d, slug)
        if v is not None:
            for _ in range(40):
                s = status(slug)
                if "COMPLETE" in s or "ERROR" in s or "CANCEL" in s:
                    tail = s.strip().splitlines()[-1] if s.strip() else "?"
                    log(f"{slug} v{v} save-run: {tail}")
                    break
                time.sleep(30)
    with open(VJSON, "w") as f:
        json.dump(VERSIONS, f, indent=2)
    log("VERSIONS: " + ", ".join(f"{k.split('/')[-1]}=v{v}" for k, v in VERSIONS.items()))
    missing = [slug for _, slug in PENDING if slug not in VERSIONS]
    if missing:
        log("ERROR: missing versions for " + ", ".join(missing))
        sys.exit(1)
    log("L22 push complete.")


if __name__ == "__main__":
    main()
