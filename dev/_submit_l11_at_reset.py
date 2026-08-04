#!/usr/bin/env python3
"""Arm: wait for the 00:00 UTC Kaggle quota reset, then submit the L11 ladder.
Idempotent via a marker. Logs to logs/l11_submit.log.

L11 tests Model-Specific Template Isolation and Ultra-Terse Squeeze for >112.
"""
import os, json, time, subprocess, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = "ai-agent-security-multi-step-tool-attacks"
LOG = os.path.join(ROOT, "logs", "l11_submit.log")
MARKER = os.path.join(ROOT, "logs", "l11_submitted.marker")

BATCH = [
 ("ahmedmobasher86/jed-public-pt-safe",  "11", "L11 ANCHOR: FRAC=97 pool{close_ok,terse_ok} (~89.6 canary)", 89.6),
 ("ahmedmobasher86/jed-public-pt-probe", "11", "L11 GPT DEDICATED: FRAC=97 template 5 close_ok (0-reasoning)", 105.0),
 ("ahmedmobasher86/jed-public-k1nx-1000","12", "L11 GEMMA DEDICATED: FRAC=97 template 6 terse_ok (minimal wrap-up)", 115.0),
 ("ahmedmobasher86/jed-public-k1nx-1200","13", "L11 PROBE: FRAC=97 template 2 bare_ok", 95.0),
 ("ahmedmobasher86/jed-public-k1nx-800", "30", "L11 SQUEEZE: FRAC=98 MARGIN=60 pool{close_ok,terse_ok}", 120.0),
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
            log(f"quota available ({n}/5 used) — submitting L11 ladder."); break
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
    log("L11 batch complete.")

if __name__ == "__main__":
    main()
