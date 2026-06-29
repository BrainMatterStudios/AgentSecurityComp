#!/usr/bin/env python3
"""Poll the 3 v312-bracket submissions until they reach a terminal state
(scored or errored), then exit so the loop re-invokes with results in hand.
Bounded: gives up after MAX_WAIT_S. Non-recurring."""
import datetime as dt
import json
import os
import subprocess
import time

COMP = "ai-agent-security-multi-step-tool-attacks"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "logs", "v312_results.log")
POLL_S = 300
MAX_WAIT_S = 6 * 3600
WATCH = {  # description-substring -> label
    "m6 N=600": "m6_600 (optimal prompt)",
    "m6 N=700": "m6_700 (optimal prompt)",
}


def log(m):
    line = f"{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}Z  {m}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def creds():
    d = json.load(open(os.path.expanduser("~/.kaggle/kaggle.json")))
    return d["username"], d["key"]


def fetch():
    u, k = creds()
    out = subprocess.run(
        ["curl", "-s", "-u", f"{u}:{k}",
         f"https://www.kaggle.com/api/v1/competitions/submissions/list/{COMP}"],
        capture_output=True, text=True, timeout=60)
    d = json.loads(out.stdout)
    return d if isinstance(d, list) else d.get("submissions", [])


def terminal(s):
    # terminal = has a public score OR an error description
    return bool(s.get("publicScore")) or bool(s.get("errorDescription"))


def main():
    log("poller armed; watching 3 v312 submissions")
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    end = time.time() + MAX_WAIT_S
    while time.time() < end:
        try:
            subs = [s for s in fetch() if (s.get("date") or "")[:10] == today]
        except Exception as e:
            log(f"fetch error: {e}")
            time.sleep(POLL_S); continue
        mine = []
        for sub in WATCH:
            for s in subs:
                if sub in (s.get("description") or ""):
                    mine.append((WATCH[sub], s)); break
        done = [m for m in mine if terminal(m[1])]
        if len(done) >= len(WATCH) and mine:
            log("ALL RESOLVED:")
            for label, s in mine:
                sc = s.get("publicScore") or "—"
                err = (s.get("errorDescription") or "")[:60]
                log(f"  {label:16} score={sc}  {('ERR: '+err) if err else 'OK'}")
            return
        log(f"pending: {len(mine)-len(done)}/{len(mine) or len(WATCH)} not yet terminal; sleeping {POLL_S}s")
        time.sleep(POLL_S)
    log("MAX_WAIT reached; exiting (check manually).")


if __name__ == "__main__":
    main()
