#!/usr/bin/env python3
"""Poll L19 ultra-lean Hermes results until they score. Matches on 'L19' in description. Logs to logs/l19_results.log."""
import datetime as dt
import os
import re
import subprocess
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "logs", "l19_results.log")
COMP = "ai-agent-security-multi-step-tool-attacks"


def log(m):
    line = f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}Z  {m}"
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")


def poll():
    out = subprocess.run(
        ["python3", "-m", "kaggle", "competitions", "submissions", COMP],
        capture_output=True,
        text=True,
        timeout=90,
    ).stdout
    rows = {}
    for line in out.splitlines():
        if "L19 " not in line:
            continue
        ref = line.split()[0]
        complete = "COMPLETE" in line
        m = re.search(r"COMPLETE\s+([0-9]+\.[0-9]+)", line)
        rows[ref] = (
            "VOID" if (complete and not m) else (m.group(1) if m else "PENDING"),
            line.strip(),
        )
    return rows


def main():
    log("polling L19 (ultra-lean Hermes) results...")
    for _ in range(300):
        rows = poll()
        scored = {r: v for r, (v, _) in rows.items() if v not in ("PENDING",)}
        log(
            f"  {len(scored)}/{len(rows)} resolved... "
            + " ".join(f"{r}={v}" for r, (v, _) in rows.items())
        )
        if rows and all(v != "PENDING" for v, _ in rows.values()):
            break
        time.sleep(90)
    rows = poll()
    log("=== L19 RESULTS (ultra-lean Hermes) ===")
    for r, (v, line) in sorted(rows.items()):
        lbl = re.search(r"(L19 [^S]+?)\s{2,}", line)
        log(f"  {r}  {v:>8}  {lbl.group(1).strip() if lbl else ''}")
    log("done")


if __name__ == "__main__":
    main()
