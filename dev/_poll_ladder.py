import subprocess, json, os, time, datetime as dt
COMP="ai-agent-security-multi-step-tool-attacks"
IDS={"54899163":"r1 base gpt440+gemma560","54899164":"r2 i13-700+gemma560",
     "54899168":"r3 i13-950+gemma560","54899170":"r4 i13-1250+gemma560",
     "54905822":"DIAG gpt200+gemma200"}
d=json.load(open(os.path.expanduser("~/.kaggle/kaggle.json"))); u,k=d["username"],d["key"]
def poll():
    out=subprocess.run(["curl","-s","-u",f"{u}:{k}",
        f"https://www.kaggle.com/api/v1/competitions/submissions/list/{COMP}"],capture_output=True,text=True,timeout=60)
    try: subs=json.loads(out.stdout)
    except Exception: return {}
    done={}
    for s in subs:
        sid=str(s.get("ref") or s.get("id"))
        if sid in IDS:
            ps=s.get("publicScore"); err=s.get("errorDescription")
            if ps not in (None,"") or err: done[sid]=(ps,err)
    return done
for _ in range(200):
    r=poll()
    with open("logs/ladder_results.log","w") as f:
        f.write(f"updated {dt.datetime.utcnow().isoformat()}Z\n")
        for sid,name in IDS.items():
            if sid in r:
                ps,err=r[sid]; f.write(f"{name}: score={ps} {'VOID:'+(err or '')[:50] if err else ''}\n")
            else:
                f.write(f"{name}: pending\n")
    if len(r)>=5: break
    time.sleep(240)
print("poll done")
