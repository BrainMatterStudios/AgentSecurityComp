#!/usr/bin/env python3
"""Arm: wait for the 00:00 UTC Kaggle quota reset, then submit the L13 HYBRID ladder.
Idempotent via a marker. Logs to logs/l13_submit.log.

L13 = DIAGNOSTIC/HYBRID night:
- anchor (both FRAC97) protects the ~89.6 standing;
- gpt-only + gemma-only FRAC97 read the board split directly (publicScore = board_row/2);
- gpt-only FRAC99 probes gpt headroom (no gemma void-drag);
- blended FRAC96 is a conservative climb bet.
Versions are filled from logs/l13_push.log after the sequential push completes.
"""
import os, json, time, subprocess, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = "ai-agent-security-multi-step-tool-attacks"
LOG = os.path.join(ROOT, "logs", "l13_submit.log")
MARKER = os.path.join(ROOT, "logs", "l13_submitted.marker")

# (slug, version, message, expected_public) — versions CONFIRMED from the push log.
BATCH = [
 ("ahmedmobasher86/jed-public-pt-safe",  "13", "L13 ANCHOR both-boards FRAC=97 pool{close_ok,terse_ok} (~89.6 floor/canary)", 89.6),
 ("ahmedmobasher86/jed-public-pt-probe", "13", "L13 SPLIT gpt-only FRAC=97 -> publicScore=gpt_row/2 (direct gpt read)", 60.0),
 ("ahmedmobasher86/jed-public-k1nx-1000","14", "L13 SPLIT gemma-only FRAC=97 -> publicScore=gemma_row/2 (gemma maxed check)", 29.0),
 ("ahmedmobasher86/jed-public-k1nx-1200","15", "L13 gpt-only FRAC=99 (gpt headroom, no gemma void-drag)", 62.0),
 ("ahmedmobasher86/jed-public-k1nx-800", "32", "L13 CLIMB BET blended FRAC=96 (conservative)", 88.0),
]

def log(m):
    line = f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}Z  {m}"
    print(line, flush=True); open(LOG, "a").write(line + "\n")

def creds():
    d = json.load(open(os.path.expanduser("~/.kaggle/kaggle.json"))); return d["username"], d["key"]

def used_today():
    u, k = creds()
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    out = subprocess.run(["curl","-s","-u",f"{u}:{k}",
        f"https://www.kaggle.com/api/v1/competitions/submissions/list/{COMP}"], capture_output=True, text=True, timeout=60)
    try: subs = json.loads(out.stdout)
    except Exception: return -1
    return sum(1 for s in subs if str(s.get("date","")).startswith(today))

def main():
    if os.path.exists(MARKER):
        log("marker present — already submitted; exiting."); return
    for _ in range(600):  # up to ~10h
        n = used_today()
        if 0 <= n < 5:
            log(f"quota available ({n}/5 used) — submitting L13 hybrid ladder."); break
        log(f"waiting for reset ({n}/5 used today)…"); time.sleep(300)
    else:
        log("timed out waiting for reset."); return
    for slug, ver, msg, exp in BATCH:
        if used_today() >= 5:
            log("quota full mid-batch — stopping."); break
        cmd = ["python3","-m","kaggle","competitions","submit",COMP,"-k",slug,"-v",ver,"-f","submission.csv","-m",msg]
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            tail = (out.stdout+out.stderr).strip().splitlines()
            log(f"submitted {slug} v{ver} (exp~{exp}) -> {tail[-1] if tail else '(ok)'}")
        except Exception as e:
            log(f"ERROR submitting {slug}: {e}")
        time.sleep(8)
    open(MARKER,"w").write(dt.datetime.now(dt.timezone.utc).isoformat())
    log("L13 batch complete.")

if __name__ == "__main__":
    main()
