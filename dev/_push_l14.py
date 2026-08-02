#!/usr/bin/env python3
"""Sequentially push the 5 L14 hop-pack kernels (respecting the 2-GPU-session cap), waiting
for each save-run to finish before the next so a slot frees. Records versions to
logs/l14_versions.json for the submit step. Logs to logs/l14_push.log."""
import os, re, time, json, subprocess, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "logs", "l14_push.log")
VJSON = os.path.join(ROOT, "logs", "l14_versions.json")

PENDING = [
    ("submission_kernel_l14_anchor", "ahmedmobasher86/jed-public-pt-safe"),
    ("submission_kernel_l14_hp8f97", "ahmedmobasher86/jed-public-pt-probe"),
    ("submission_kernel_l14_hp8f85", "ahmedmobasher86/jed-public-k1nx-1000"),
    ("submission_kernel_l14_hp8f93", "ahmedmobasher86/jed-public-k1nx-1200"),
    ("submission_kernel_l14_hp4f93", "ahmedmobasher86/jed-public-k1nx-800"),
]
VERSIONS = {}


def log(m):
    line = f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}Z  {m}"
    print(line, flush=True); open(LOG, "a").write(line + "\n")


def status(slug):
    out = subprocess.run(["python3", "-m", "kaggle", "kernels", "status", slug],
                         capture_output=True, text=True, timeout=60)
    return (out.stdout + out.stderr)


def push(d, slug):
    for attempt in range(40):
        out = subprocess.run(["python3", "-m", "kaggle", "kernels", "push", "-p", os.path.join(ROOT, d)],
                             capture_output=True, text=True, timeout=180)
        txt = (out.stdout + out.stderr)
        m = re.search(r"version (\d+) successfully pushed", txt)
        if m:
            v = int(m.group(1)); VERSIONS[slug] = v
            log(f"pushed {slug} -> v{v}")
            json.dump(VERSIONS, open(VJSON, "w"))
            return v
        if "session count" in txt or "batch GPU" in txt or "maximum" in txt.lower():
            log(f"{slug}: GPU cap reached, waiting 60s (attempt {attempt+1})…")
            time.sleep(60); continue
        log(f"{slug}: unexpected push output: {txt.strip().splitlines()[-1] if txt.strip() else txt!r}")
        time.sleep(30)
    log(f"{slug}: FAILED to push after retries")
    return None


def main():
    log("L14 sequential push start (5 kernels).")
    for d, slug in PENDING:
        v = push(d, slug)
        if v is not None:
            for _ in range(40):
                s = status(slug)
                if "COMPLETE" in s or "ERROR" in s or "CANCEL" in s:
                    log(f"{slug} v{v} save-run: {s.strip().splitlines()[-1] if s.strip() else '?'}")
                    break
                time.sleep(30)
    json.dump(VERSIONS, open(VJSON, "w"))
    log("VERSIONS: " + ", ".join(f"{k.split('/')[-1]}=v{v}" for k, v in VERSIONS.items()))
    log("L14 push complete.")


if __name__ == "__main__":
    main()
