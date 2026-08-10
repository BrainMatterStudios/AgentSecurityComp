#!/usr/bin/env python3
"""Arm-at-reset submitter for the L21 multi-call fast-emit set.

Run under caffeinate:
nohup caffeinate -i python3 dev/_submit_l21_at_reset.py > logs/l21_reset_run.log 2>&1 &
"""
import csv
import datetime as dt
import io
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "logs", "l21_submit.log")
VJSON = os.path.join(ROOT, "logs", "l21_versions.json")
MARKER = os.path.join(ROOT, "logs", "l21_submitted.marker")
COMP = "ai-agent-security-multi-step-tool-attacks"

ARM_UTC_DATE = os.getenv("L21_ARM_DATE", "2026-08-09")

MSG = {
    "ahmedmobasher86/jed-public-mp-anchor": "L21 ANCHOR single-post FRAC97 (~89.5 banked)",
    "ahmedmobasher86/jed-public-mp-safe": "L21 MULTI-CALL K8 CAL SAFETY=0.75 (conservative ~110+)",
    "ahmedmobasher86/jed-public-mp-moderate": "L21 MULTI-CALL K8 CAL SAFETY=0.90 (PRIMARY ~140+)",
    "ahmedmobasher86/jed-public-mp-aggressive": "L21 MULTI-CALL K8 CAL SAFETY=1.05 (stretch ~165+)",
    "ahmedmobasher86/jed-public-mp-stretch": "L21 MULTI-CALL K8 CAL SAFETY=1.20 (boundary probe)",
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
    try:
        seen_all = list_submissions(run=run)
    except Exception:
        seen_all = {}
    existing_descs = set(seen_all.values())
    refs = {}
    for slug in ORDER:
        v = versions.get(slug)
        if v is None:
            log(f"SKIP {slug}: no version")
            continue
        if MSG[slug] in existing_descs:
            log(f"SKIP {slug}: already submitted (ref present)")
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
        log(f"L21 marker {MARKER} exists; exiting.")
        return
    if not os.path.exists(VJSON):
        log(f"ERROR: {VJSON} missing; run _push_l21.py first.")
        sys.exit(1)
    with open(VJSON) as f:
        versions = json.load(f)

    log(f"Arming L21 submissions for UTC reset date {ARM_UTC_DATE} (5 kernels).")
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
            f"L21 submitted at {dt.datetime.now(dt.timezone.utc).isoformat()}\n"
            + json.dumps(refs, indent=2)
            + "\n"
        )
    log(f"L21 arm-at-reset COMPLETE. Marker written -> {MARKER}")


if __name__ == "__main__":
    import sys
    main()
