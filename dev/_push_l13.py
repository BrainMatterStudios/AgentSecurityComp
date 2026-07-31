#!/usr/bin/env python3
"""Sequentially push the L13 kernels (respecting the 2-GPU-session cap), waiting for
each to leave the running state before the next, and record the assigned version numbers.
pt-safe already pushed as v13. Logs to logs/l13_push.log."""
import os, re, time, subprocess, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "logs", "l13_push.log")

# (dir, slug) — pt-safe (anchor) already pushed as v13
PENDING = [
    ("submission_kernel_l13_gpt97",   "ahmedmobasher86/jed-public-pt-probe"),
    ("submission_kernel_l13_gemma97",  "ahmedmobasher86/jed-public-k1nx-1000"),
    ("submission_kernel_l13_gpt99",    "ahmedmobasher86/jed-public-k1nx-1200"),
    ("submission_kernel_l13_blend96",  "ahmedmobasher86/jed-public-k1nx-800"),
]
VERSIONS = {"ahmedmobasher86/jed-public-pt-safe": 13}


def log(m):
    line = f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}Z  {m}"
    print(line, flush=True); open(LOG, "a").write(line + "\n")


def status(slug):
    out = subprocess.run(["python3", "-m", "kaggle", "kernels", "status", slug],
                         capture_output=True, text=True, timeout=60)
    return (out.stdout + out.stderr)


def push(d, slug):
    for attempt in range(40):  # up to ~40 min of waiting for a free GPU slot
        out = subprocess.run(["python3", "-m", "kaggle", "kernels", "push", "-p", os.path.join(ROOT, d)],
                             capture_output=True, text=True, timeout=180)
        txt = (out.stdout + out.stderr)
        m = re.search(r"version (\d+) successfully pushed", txt)
        if m:
            v = int(m.group(1)); VERSIONS[slug] = v
            log(f"pushed {slug} -> v{v}")
            return v
        if "session count" in txt or "batch GPU" in txt:
            log(f"{slug}: GPU cap reached, waiting 60s (attempt {attempt+1})…")
            time.sleep(60); continue
        log(f"{slug}: unexpected push output: {txt.strip().splitlines()[-1] if txt.strip() else txt!r}")
        time.sleep(30)
    log(f"{slug}: FAILED to push after retries")
    return None


def wait_running_below_2():
    # crude: after a successful push, wait for that kernel's save-run to finish so a slot frees
    time.sleep(20)


def main():
    log("L13 sequential push start (pt-safe already v13).")
    for d, slug in PENDING:
        v = push(d, slug)
        if v is not None:
            # wait for this kernel to complete its save-run so the GPU slot frees
            for _ in range(30):
                s = status(slug)
                if "COMPLETE" in s or "ERROR" in s or "CANCEL" in s:
                    log(f"{slug} v{v} save-run: {s.strip().splitlines()[-1] if s.strip() else '?'}")
                    break
                time.sleep(30)
    log("VERSIONS: " + ", ".join(f"{k.split('/')[-1]}=v{v}" for k, v in VERSIONS.items()))
    log("L13 push complete.")


if __name__ == "__main__":
    main()
