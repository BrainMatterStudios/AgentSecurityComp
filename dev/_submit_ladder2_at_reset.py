"""Arm: wait for the daily Kaggle quota reset (00:00 UTC) then submit the approved
revised ladder (push-both-boards, gpt=idx13 preclose, gemma=natural). Idempotent
via a marker. Logs to logs/ladder2_submit.log."""
import os, json, time, subprocess, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = "ai-agent-security-multi-step-tool-attacks"
LOG = os.path.join(ROOT, "logs", "ladder2_submit.log")
MARKER = os.path.join(ROOT, "logs", "ladder2_submitted.marker")
# (slug, version, message, mean_if_valid)
BATCH = [
 ("ahmedmobasher86/jed-public-pt-safe",  "3", "L2 r1: gpt-idx13 N740 + gemma-nat N600 (mean~60.3, safety anchor)", 60.3),
 ("ahmedmobasher86/jed-public-pt-probe", "2", "L2 r2: gpt-idx13 N780 + gemma-nat N640 (mean~63.9)", 63.9),
 ("ahmedmobasher86/jed-public-k1nx-1000","3", "L2 r3: gpt-idx13 N700 + gemma-nat N720 (mean~63.9, gemma ceiling probe)", 63.9),
 ("ahmedmobasher86/jed-public-k1nx-1200","4", "L2 r4: gpt-idx13 N880 + gemma-nat N560 (mean~64.8, gpt ceiling pin)", 64.8),
 ("ahmedmobasher86/jed-public-k1nx-800", "22","L2 r5: gpt-idx13 N820 + gemma-nat N700 (mean~68.4, jackpot)", 68.4),
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
