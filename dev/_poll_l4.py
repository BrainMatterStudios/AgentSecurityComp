import subprocess, json, os, time, datetime as dt
COMP="ai-agent-security-multi-step-tool-attacks"
d=json.load(open(os.path.expanduser("~/.kaggle/kaggle.json"))); u,k=d["username"],d["key"]
def poll():
    out=subprocess.run(["curl","-s","-u",f"{u}:{k}",f"https://www.kaggle.com/api/v1/competitions/submissions/list/{COMP}"],capture_output=True,text=True,timeout=60)
    try: subs=json.loads(out.stdout)
    except Exception: return []
    return [s for s in subs if str(s.get('date','')).startswith('2026-07-25')]
for _ in range(240):
    rows=poll()
    done=[s for s in rows if s.get('publicScore') not in (None,'') or s.get('errorDescription')]
    with open("logs/l4_results.log","w") as f:
        f.write(f"updated {dt.datetime.utcnow().isoformat()}Z  ({len(rows)} subs, {len(done)} scored)\n")
        for s in sorted(rows,key=lambda x:x.get('date','')):
            ps=s.get('publicScore'); err=s.get('errorDescription')
            f.write(f"  {(s.get('description') or '')[:44]:44} -> {('VOID' if err else ps) if (ps or err) else 'pending'}\n")
    if rows and len(done)>=len(rows) and len(rows)>=5: break
    time.sleep(240)
