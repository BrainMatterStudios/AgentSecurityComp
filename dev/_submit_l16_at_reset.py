#!/usr/bin/env python3
"""Arm-at-reset submitter for the L16 deputy-fix validation ladder. Aug-3 quota is spent, so
this waits until the 00:00 UTC quota reset (UTC date rolls over) and then submits the 5 L16
kernels using logs/l16_versions.json. Marker-idempotent (won't double-submit). Run under
caffeinate: `nohup caffeinate -i python3 dev/_submit_l16_at_reset.py > logs/l16_reset_run.log 2>&1 &`
"""
import os, json, time, subprocess, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "logs", "l16_submit.log")
VJSON = os.path.join(ROOT, "logs", "l16_versions.json")
MARKER = os.path.join(ROOT, "logs", "l16_submitted.marker")
COMP = "ai-agent-security-multi-step-tool-attacks"

# arm date = the UTC date on which we want the submit to fire (the next reset day)
ARM_UTC_DATE = os.getenv("L16_ARM_DATE", "2026-08-04")

MSG = {
    "ahmedmobasher86/jed-public-pt-safe":   "L16 ANCHOR exfil shared FRAC=97 (~89 public re-bank / canary)",
    "ahmedmobasher86/jed-public-pt-probe":  "L16 DEPUTY-FIXED FRAC=85 (deep void insurance; terminating-deputy fix)",
    "ahmedmobasher86/jed-public-k1nx-1000": "L16 DEPUTY-FIXED FRAC=90 (main validation)",
    "ahmedmobasher86/jed-public-k1nx-1200": "L16 DEPUTY-FIXED FRAC=95 (A/B vs L15 deputy void)",
    "ahmedmobasher86/jed-public-k1nx-800":  "L16 DEPUTY-FIXED FRAC=97 (aggressive; deputy at exfil FRAC)",
}
ORDER = list(MSG.keys())


def log(m):
    line = f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}Z  {m}"
    print(line, flush=True); open(LOG, "a").write(line + "\n")


def main():
    if os.path.exists(MARKER):
        log("marker present -> already submitted; exiting."); return
    if not os.path.exists(VJSON):
        log("ERROR: no versions file; run _push_l16.py first."); return
    versions = json.load(open(VJSON))
    log(f"armed for {ARM_UTC_DATE} 00:00 UTC reset; waiting…")
    while True:
        today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
        if today >= ARM_UTC_DATE:
            break
        time.sleep(60)
    log(f"reset reached (UTC {today}); submitting {len(versions)} kernels.")
    for slug in ORDER:
        v = versions.get(slug)
        if v is None:
            log(f"SKIP {slug}: no version"); continue
        out = subprocess.run(
            ["python3", "-m", "kaggle", "competitions", "submit", COMP,
             "-k", slug, "-v", str(v), "-f", "submission.csv", "-m", MSG[slug]],
            capture_output=True, text=True, timeout=180)
        txt = (out.stdout + out.stderr).strip().splitlines()
        log(f"{slug.split('/')[-1]} v{v}: {txt[-1] if txt else '(no output)'}")
        time.sleep(3)
    open(MARKER, "w").write(dt.datetime.now(dt.timezone.utc).isoformat())
    log("L16 submit complete (marker written). Then poll dev/_poll_l16.py.")


if __name__ == "__main__":
    main()
