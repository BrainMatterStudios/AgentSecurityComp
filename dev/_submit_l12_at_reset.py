#!/usr/bin/env python3
"""Arm: wait for the 00:00 UTC Kaggle quota reset, then submit the L12 ladder.
Idempotent via a marker. Logs to logs/l12_submit.log.

L12 tests Multi-Endpoint Single-Message Prompting (K=4, 5, 6 endpoints/msg) for 110-115+.
"""
import os, json, time, subprocess, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = "ai-agent-security-multi-step-tool-attacks"
LOG = os.path.join(ROOT, "logs", "l12_submit.log")
MARKER = os.path.join(ROOT, "logs", "l12_submitted.marker")

BATCH = [
 ("ahmedmobasher86/jed-public-pt-safe",  "12", "L12 ANCHOR: Single-post control FRAC=97 ENDPOINTS=1 (~89.6 canary)", 89.6),
 ("ahmedmobasher86/jed-public-pt-probe", "12", "L12 MULTI-ENDPOINT: K=4 FRAC=95 (4 posts/msg -> ~95-100)", 97.5),
 ("ahmedmobasher86/jed-public-k1nx-1000","13", "L12 MULTI-ENDPOINT: K=5 FRAC=95 (5 posts/msg -> ~105-110)", 108.0),
 ("ahmedmobasher86/jed-public-k1nx-1200","14", "L12 MULTI-ENDPOINT: K=6 FRAC=95 (6 posts/msg -> ~110-115)", 112.5),
 ("ahmedmobasher86/jed-public-k1nx-800", "31", "L12 SQUEEZE: K=5 FRAC=96 MAX_CAND=280 -> ~115+", 115.0),
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
            log(f"quota available ({n}/5 used) — submitting L12 ladder."); break
        log(f"waiting for reset ({n}/5 used today)…"); time.sleep(300)
    else:
        log("timed out waiting for reset."); return
    for slug, ver, msg, mean in BATCH:
        if used_today() >= 5:
            log("quota full mid-batch — stopping."); break
        cmd = ["python3","-m","kaggle","competitions","submit",COMP,"-k",slug,"-v",ver,"-f","submission.csv","-m",msg]
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            tail = (out.stdout+out.stderr).strip().splitlines()
            log(f"submitted {slug} v{ver} (mean~{mean}) -> {tail[-1] if tail else '(ok)'}")
        except Exception as e:
            log(f"ERROR submitting {slug}: {e}")
        time.sleep(8)
    open(MARKER,"w").write(dt.datetime.now(dt.timezone.utc).isoformat())
    log("L12 batch complete.")

if __name__ == "__main__":
    main()
