#!/usr/bin/env python3
"""Arm-at-reset submitter for the L19 ultra-lean Hermes set.

Run under caffeinate:
nohup caffeinate -i python3 dev/_submit_l19_at_reset.py > logs/l19_reset_run.log 2>&1 &
"""
import csv
import datetime as dt
import io
import json
import os
import subprocess
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "logs", "l19_submit.log")
VJSON = os.path.join(ROOT, "logs", "l19_versions.json")
MARKER = os.path.join(ROOT, "logs", "l19_submitted.marker")
COMP = "ai-agent-security-multi-step-tool-attacks"

ARM_UTC_DATE = os.getenv("L19_ARM_DATE", "2026-08-07")

MSG = {
    "ahmedmobasher86/jed-public-pt-safe": "L19 ANCHOR baseline single-post FRAC97 (~89.5 canary)",
    "ahmedmobasher86/jed-public-pt-probe": "L19 LEAN HERMES N=1100 (conservative ~99.0 target)",
    "ahmedmobasher86/jed-public-k1nx-1000": "L19 LEAN HERMES N=1180 (moderate ~106.2 target)",
    "ahmedmobasher86/jed-public-k1nx-1200": "L19 LEAN HERMES N=1250 (PRIMARY TOP-BOARD TARGET ~112.5)",
    "ahmedmobasher86/jed-public-k1nx-800": "L19 LEAN HERMES N=1320 (stretch ~118.8 target)",
}
ORDER = list(MSG.keys())


def log(m):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    line = f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}Z  {m}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def list_submissions(run=subprocess.run):
    out = run(
        [
            "python3",
            "-m",
            "kaggle",
            "competitions",
            "submissions",
            COMP,
            "-v",
            "--page-size",
            "100",
        ],
        capture_output=True,
        text=True,
        timeout=90,
    )
    rows = {}
    for row in csv.DictReader(io.StringIO(out.stdout)):
        ref = row.get("ref")
        desc = row.get("description")
        if ref and desc:
            rows[ref] = desc
    return rows


def submit_all(versions, run=subprocess.run, before_refs=None):
    before_refs = set(before_refs or [])
    refs = {}
    for slug in ORDER:
        v = versions.get(slug)
        if v is None:
            log(f"SKIP {slug}: no version")
            continue
        out = run(
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
        for _ in range(20):
            seen = list_submissions(run=run)
            matches = [
                r for r, d in seen.items() if d == MSG[slug] and r not in before_refs
            ]
            if matches:
                ref = matches[0]
                refs[slug] = ref
                log(f"{slug} -> ref {ref}")
                break
            time.sleep(3)
        time.sleep(1)
    return refs


def main():
    if os.path.exists(MARKER):
        log(f"L19 marker {MARKER} exists; exiting.")
        return
    if not os.path.exists(VJSON):
        log(f"ERROR: {VJSON} missing; run _push_l19.py first.")
        sys.exit(1)
    with open(VJSON) as f:
        versions = json.load(f)

    log(f"Arming L19 submissions for UTC reset date {ARM_UTC_DATE} (5 kernels).")
    while True:
        now_utc = dt.datetime.now(dt.timezone.utc)
        today_str = now_utc.strftime("%Y-%m-%d")
        if today_str >= ARM_UTC_DATE:
            log(
                f"UTC date is {today_str} >= {ARM_UTC_DATE}; executing submissions..."
            )
            break
        left_sec = int(
            (
                dt.datetime.strptime(ARM_UTC_DATE + " 00:00:05", "%Y-%m-%d %H:%M:%S")
                .replace(tzinfo=dt.timezone.utc)
                - now_utc
            ).total_seconds()
        )
        if left_sec > 0:
            sleep_s = min(left_sec, 60)
            log(f"Waiting for UTC 00:00:05 reset... ~{left_sec}s remaining")
            time.sleep(sleep_s)
        else:
            time.sleep(5)

    before_refs = set(list_submissions().keys())
    refs = submit_all(versions, before_refs=before_refs)
    with open(MARKER, "w") as f:
        f.write(
            f"L19 submitted at {dt.datetime.now(dt.timezone.utc).isoformat()}\n"
            + json.dumps(refs, indent=2)
            + "\n"
        )
    log(f"L19 arm-at-reset COMPLETE. Marker written -> {MARKER}")


if __name__ == "__main__":
    main()
