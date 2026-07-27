"""Arm: wait for the 00:00 UTC Kaggle quota reset, then submit the L7 ladder.
Idempotent via a marker. Logs to logs/l7_submit.log.

L7 = the close_ok decode-cut lever (min-cost template, +~20pct candidates on the
reasoning board) on top of the validated replay-safe adaptive engine (80.145 base).
All rungs use bare SECRET_MARKER payload. FRAC + template-set vary per rung so the
lever, FRAC scaling, and a safe floor are all measured in one reset.
"""
import os, json, time, subprocess, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = "ai-agent-security-multi-step-tool-attacks"
LOG = os.path.join(ROOT, "logs", "l9_submit.log")
MARKER = os.path.join(ROOT, "logs", "l9_submitted.marker")
# (slug, version, message, mean_if_valid)
BATCH = [
 ("ahmedmobasher86/jed-public-pt-safe",  "9","L9 K=1 baseline single-post FRAC=97 pool (~87 canary)", 87.5),
 ("ahmedmobasher86/jed-public-pt-probe", "9","L9 PACK K=2 FRAC=97 (overhead amortization)", 92.0),
 ("ahmedmobasher86/jed-public-k1nx-1000","10","L9 PACK K=4 FRAC=97 (overhead amortization)", 100.0),
 ("ahmedmobasher86/jed-public-k1nx-1200","11","L9 PACK K=8 FRAC=97 (overhead amortization)", 105.0),
 ("ahmedmobasher86/jed-public-k1nx-800", "VK16","L9 PACK K=16 FRAC=95 (max amortization)", 108.0),
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
            log(f"quota available ({n}/5 used) — submitting L7 ladder."); break
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
    log("L7 batch complete.")
if __name__ == "__main__":
    main()
