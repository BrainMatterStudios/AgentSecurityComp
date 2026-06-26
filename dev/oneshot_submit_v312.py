#!/usr/bin/env python3
"""ONE-SHOT 3.1.2 recovery submitter (non-recurring).

Waits until just after the 00:00 UTC daily quota reset, re-checks that quota is
actually free, submits the three vetted recovery kernels ONCE, logs the result,
and exits. No loop, no recurrence — fires a single batch then stops.
"""
import datetime as dt
import json
import os
import subprocess
import sys
import time

COMP = "ai-agent-security-multi-step-tool-attacks"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "logs", "v312_oneshot_submit.log")
MARKER = os.path.join(ROOT, "logs", "v312_oneshot_DONE")
os.makedirs(os.path.dirname(LOG), exist_ok=True)

# (kernel slug, version, message) — all carry the SECRET_MARKER EXFIL fix + governor
BATCH = [
    ("ahmedmobasher86/jed-v312-k1-300",     "2", "v312: SECRET_MARKER EXFIL, static N=300 guaranteed-valid floor"),
    ("ahmedmobasher86/jed-v312-gov-safe",   "2", "v312: SECRET_MARKER EXFIL, adaptive governor safety=1.8 (9000s/phase)"),
    ("ahmedmobasher86/jed-public-k1nx-680", "3", "v312: SECRET_MARKER EXFIL, adaptive governor safety=1.5 (9000s/phase)"),
]


def log(msg):
    line = f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}Z  {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def creds():
    p = os.path.expanduser("~/.kaggle/kaggle.json")
    d = json.load(open(p))
    return d["username"], d["key"]


def submissions_today():
    # curl matches the working CLI TLS path (the framework Python lacks CA certs).
    u, k = creds()
    out = subprocess.run(
        ["curl", "-s", "-u", f"{u}:{k}",
         f"https://www.kaggle.com/api/v1/competitions/submissions/list/{COMP}"],
        capture_output=True, text=True, timeout=60)
    data = json.loads(out.stdout)
    subs = data if isinstance(data, list) else data.get("submissions", [])
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    return sum(1 for s in subs if (s.get("date") or "")[:10] == today)


def main():
    if os.path.exists(MARKER):
        log("marker present — already ran; exiting without submitting.")
        return
    now = dt.datetime.now(dt.timezone.utc)
    # next 00:00 UTC + 45s margin
    reset = (now + dt.timedelta(days=1)).replace(hour=0, minute=0, second=45, microsecond=0)
    if now.hour == 0 and now.minute < 5:
        reset = now.replace(second=45, microsecond=0)  # already just past reset
    wait_s = max(0, (reset - now).total_seconds())
    log(f"armed; now={now.strftime('%H:%M:%S')}Z, will submit at {reset.strftime('%Y-%m-%d %H:%M:%S')}Z (sleep {int(wait_s)}s)")
    # sleep in chunks so a kill is responsive
    end = time.time() + wait_s
    while time.time() < end:
        time.sleep(min(60, max(1, end - time.time())))

    try:
        used = submissions_today()
    except Exception as e:
        used = -1
        log(f"WARN: could not read quota ({e}); proceeding cautiously.")
    log(f"quota check: {used}/5 used today")
    if used >= 5:
        log("quota already full at fire time — aborting to avoid waste.")
        return

    free = 5 if used < 0 else (5 - used)
    for i, (kernel, ver, msg) in enumerate(BATCH):
        if i >= free:
            log(f"only {free} slots free — stopping before {kernel}")
            break
        cmd = ["python3", "-m", "kaggle", "competitions", "submit", COMP,
               "-k", kernel, "-v", ver, "-f", "submission.csv", "-m", msg]
        log(f"submitting {kernel} v{ver} ...")
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            tail = (out.stdout + out.stderr).strip().splitlines()
            log(f"  -> {tail[-1] if tail else '(no output)'}")
        except Exception as e:
            log(f"  -> ERROR submitting {kernel}: {e}")
        time.sleep(8)

    open(MARKER, "w").write(dt.datetime.now(dt.timezone.utc).isoformat())
    log("ONE-SHOT batch complete. Exiting (non-recurring).")


if __name__ == "__main__":
    main()
