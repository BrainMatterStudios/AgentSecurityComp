#!/usr/bin/env python3
"""Arm-at-reset submitter for the L17 Gemma forge ladder.

Run under caffeinate:
nohup caffeinate -i python3 dev/_submit_l17_at_reset.py > logs/l17_reset_run.log 2>&1 &
"""
import datetime as dt
import json
import os
import subprocess
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "logs", "l17_submit.log")
VJSON = os.path.join(ROOT, "logs", "l17_versions.json")
MARKER = os.path.join(ROOT, "logs", "l17_submitted.marker")
COMP = "ai-agent-security-multi-step-tool-attacks"

ARM_UTC_DATE = os.getenv("L17_ARM_DATE", "2026-08-05")

MSG = {
    "ahmedmobasher86/jed-public-pt-safe": "L17 GEMMA-FORGE K=8 N=60; gpt fallback close_ok FRAC=97",
    "ahmedmobasher86/jed-public-pt-probe": "L17 GEMMA-FORGE K=8 N=90; medium ladder rung",
    "ahmedmobasher86/jed-public-k1nx-1000": "L17 GEMMA-FORGE K=8 N=120; aggressive under 960 posts",
    "ahmedmobasher86/jed-public-k1nx-1200": "L17 GEMMA-FORGE K=4 N=180; lower per-candidate hop risk",
    "ahmedmobasher86/jed-public-k1nx-800": "L17 SPLIT-MP hedge: agg-probe split, gpt K=4 plus gemma N=760",
}
ORDER = list(MSG.keys())


def log(m):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    line = f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}Z  {m}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def main():
    if os.path.exists(MARKER):
        log("marker present -> already submitted; exiting.")
        return
    if not os.path.exists(VJSON):
        log("ERROR: no versions file; run _push_l17.py first.")
        return
    with open(VJSON) as f:
        versions = json.load(f)
    log(f"armed for {ARM_UTC_DATE} 00:00 UTC reset; waiting.")
    while True:
        today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
        if today >= ARM_UTC_DATE:
            break
        time.sleep(60)
    log(f"reset reached (UTC {today}); submitting {len(versions)} kernels.")
    for slug in ORDER:
        v = versions.get(slug)
        if v is None:
            log(f"SKIP {slug}: no version")
            continue
        out = subprocess.run(
            [
                "python3",
                "-m",
                "kaggle",
                "competitions",
                "submit",
                COMP,
                "-k",
                slug,
                "-v",
                str(v),
                "-f",
                "submission.csv",
                "-m",
                MSG[slug],
            ],
            capture_output=True,
            text=True,
            timeout=180,
        )
        txt = (out.stdout + out.stderr).strip().splitlines()
        log(f"{slug.split('/')[-1]} v{v}: {txt[-1] if txt else '(no output)'}")
        time.sleep(3)
    with open(MARKER, "w") as f:
        f.write(dt.datetime.now(dt.timezone.utc).isoformat())
    log("L17 submit complete (marker written). Then poll dev/_poll_l17.py.")


if __name__ == "__main__":
    main()
