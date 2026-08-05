#!/usr/bin/env python3
"""Arm-at-reset submitter for the L18 hybrid set.

Run under caffeinate:
nohup caffeinate -i python3 dev/_submit_l18_at_reset.py > logs/l18_reset_run.log 2>&1 &
"""
import csv
import datetime as dt
import io
import json
import os
import subprocess
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "logs", "l18_submit.log")
VJSON = os.path.join(ROOT, "logs", "l18_versions.json")
MARKER = os.path.join(ROOT, "logs", "l18_submitted.marker")
COMP = "ai-agent-security-multi-step-tool-attacks"

ARM_UTC_DATE = os.getenv("L18_ARM_DATE", "2026-08-06")

MSG = {
    "ahmedmobasher86/jed-public-pt-safe": "L18 ANCHOR replay-safe FRAC97 templates 5 and 6 current baseline",
    "ahmedmobasher86/jed-public-pt-probe": "L18 ACO-FORGE exact a.co paths K8 N60 validation-gated probe",
    "ahmedmobasher86/jed-public-k1nx-1000": "L18 ACO-FORGE exact a.co paths K8 N120 moderate rung",
    "ahmedmobasher86/jed-public-k1nx-1200": "L18 SPLIT-SAFE gpt K4 plus gemma N520 no prompt12",
    "ahmedmobasher86/jed-public-k1nx-800": "L18 ACO-FORGE exact a.co paths K8 N230 single stretch",
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
                ref for ref, desc in seen.items()
                if ref not in before_refs and desc == MSG[slug]
            ]
            if matches:
                refs[slug] = matches[0]
                before_refs.add(matches[0])
                log(f"confirmed {slug.split('/')[-1]} -> ref {matches[0]}")
                break
            time.sleep(6)
        time.sleep(3)
    if len(refs) == len(ORDER):
        with open(MARKER, "w") as f:
            f.write(dt.datetime.now(dt.timezone.utc).isoformat())
        log("L18 submit complete; all refs confirmed; marker written.")
    else:
        missing = [slug for slug in ORDER if slug not in refs]
        log("ERROR: not writing marker; missing confirmed refs for " + ", ".join(missing))
    return refs


def main():
    if os.path.exists(MARKER):
        log("marker present -> already submitted; exiting.")
        return
    if not os.path.exists(VJSON):
        log("ERROR: no versions file; run _push_l18.py first.")
        return
    with open(VJSON) as f:
        versions = json.load(f)
    existing = set(list_submissions())
    log(f"armed for {ARM_UTC_DATE} 00:00 UTC reset; waiting.")
    while True:
        today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
        if today >= ARM_UTC_DATE:
            break
        time.sleep(60)
    log(f"reset reached (UTC {today}); submitting {len(versions)} kernels.")
    submit_all(versions, before_refs=existing)
    log("Then poll dev/_poll_l18.py.")


if __name__ == "__main__":
    main()
