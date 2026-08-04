#!/usr/bin/env python3
"""Poll the 5 L13 submissions until all have a public score, then print the split reads.
Exits when resolved (or after ~3h). Logs to logs/l13_results.log."""
import os, json, time, subprocess, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = "ai-agent-security-multi-step-tool-attacks"
LOG = os.path.join(ROOT, "logs", "l13_results.log")
REFS = {  # ref -> label
 "55160909": "anchor (both FRAC97)         ~89.6 floor",
 "55160913": "gpt-only FRAC97              -> gpt_row/2",
 "55160917": "gemma-only FRAC97            -> gemma_row/2",
 "55160920": "gpt-only FRAC99              gpt headroom",
 "55160923": "blend96 (both FRAC96)        climb bet",
}

def log(m):
    line = f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}Z  {m}"
    print(line, flush=True); open(LOG, "a").write(line + "\n")

def creds():
    d = json.load(open(os.path.expanduser("~/.kaggle/kaggle.json"))); return d["username"], d["key"]

def fetch():
    u, k = creds()
    out = subprocess.run(["curl","-s","-u",f"{u}:{k}",
        f"https://www.kaggle.com/api/v1/competitions/submissions/list/{COMP}"], capture_output=True, text=True, timeout=60)
    try: return json.loads(out.stdout)
    except Exception: return []

def main():
    log("polling L13 scores…")
    for _ in range(120):  # ~3h at 90s
        subs = {str(s.get("ref")): s for s in fetch()}
        got = {r: subs.get(r, {}).get("publicScore") for r in REFS}
        if all(v not in (None, "") for v in got.values()):
            log("ALL L13 SCORES IN:")
            for r, lab in REFS.items():
                log(f"  {got[r]:>8}  {lab}")
            # split arithmetic
            try:
                anchor=float(got["55160909"]); gpt=2*float(got["55160913"]); gem=2*float(got["55160917"])
                gpt99=2*float(got["55160920"])
                log(f"  => gpt_row={gpt:.1f}  gemma_row={gem:.1f}  (consistency: anchor {anchor:.1f} vs (gpt+gem)/2 {(gpt+gem)/2:.1f})")
                log(f"  => gpt headroom: gpt-only FRAC99 row={gpt99:.1f} vs FRAC97 row={gpt:.1f}  ({'HEADROOM' if gpt99>gpt+1 else 'flat/maxed'})")
            except Exception as e:
                log(f"  (split calc skipped: {e})")
            log("L13 poll complete.")
            return
        done = sum(1 for v in got.values() if v not in (None, ""))
        log(f"  {done}/5 scored…")
        time.sleep(90)
    log("poll timed out (scores still pending).")

if __name__ == "__main__":
    main()
