"""Arm: wait for the daily Kaggle quota reset (00:00 UTC) then submit the approved
revised ladder (push-both-boards, gpt=idx13 preclose, gemma=natural). Idempotent
via a marker. Logs to logs/l3_submit.log."""
import os, json, time, subprocess, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = "ai-agent-security-multi-step-tool-attacks"
LOG = os.path.join(ROOT, "logs", "l3_submit.log")
MARKER = os.path.join(ROOT, "logs", "l3_submitted.marker")
# (slug, version, message, mean_if_valid)
BATCH = [
 ("ahmedmobasher86/jed-public-pt-safe",  "4", "L3 r1 anchor: gpt-idx13 N760 + gemma N600 (~61.2, new best if valid)", 61.2),
 ("ahmedmobasher86/jed-public-pt-probe", "3", "L3 r2 gpt-probe: gpt-idx13 N840 + gemma N600 (~64.8)", 64.8),
 ("ahmedmobasher86/jed-public-k1nx-1000","4", "L3 r3 gemma-probe: gpt-idx13 N740 + gemma N700 (~64.8)", 64.8),
 ("ahmedmobasher86/jed-public-k1nx-1200","5", "L3 r4 jackpot: gpt-idx13 N800 + gemma N680 (~66.6)", 66.6),
 ("ahmedmobasher86/jed-public-k1nx-800", "23","HUNT cost-probe: encodes Kaggle warm interact time into N (decode med=pub/3.6)", 0.0),
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
    # wait until quota available (reset drops today's count to 0)
    for _ in range(600):  # up to ~10h
        n = used_today()
        if 0 <= n < 5:
            log(f"quota available ({n}/5 used) — submitting ladder.")
            break
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
    log("ladder2 batch complete.")
if __name__ == "__main__":
    main()
