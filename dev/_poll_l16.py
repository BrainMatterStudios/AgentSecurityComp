#!/usr/bin/env python3
"""Poll L16 deputy-fix results until they score. Matches on 'L16' in the description (no refs
needed pre-submit). Logs to logs/l16_results.log. COMPLETE-with-blank-score = VOID.
Run after the reset submit fires."""
import re, time, subprocess, os, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "logs", "l16_results.log")
COMP = "ai-agent-security-multi-step-tool-attacks"


def log(m):
    line = f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}Z  {m}"
    print(line, flush=True); open(LOG, "a").write(line + "\n")


def poll():
    out = subprocess.run(["python3", "-m", "kaggle", "competitions", "submissions", COMP],
                         capture_output=True, text=True, timeout=90).stdout
    rows = {}
    for line in out.splitlines():
        if "L16 " not in line:
            continue
        ref = line.split()[0]
        desc = re.search(r"(L16[^A-Z]*[A-Z-]*[^(]*)", line)
        label = (re.search(r"L16 ([A-Z0-9=/ -]+?) ", line) or [None, ref]).group(1) if False else ref
        complete = "COMPLETE" in line
        m = re.search(r"COMPLETE\s+([0-9]+\.[0-9]+)", line)
        rows[ref] = ("VOID" if (complete and not m) else (m.group(1) if m else "PENDING"), line.strip())
    return rows


def main():
    log("polling L16 (deputy-fix) results…")
    for _ in range(300):
        rows = poll()
        scored = {r: v for r, (v, _) in rows.items() if v not in ("PENDING",)}
        log(f"  {len(scored)}/{len(rows)} resolved… " + " ".join(f"{r}={v}" for r, (v, _) in rows.items()))
        if rows and all(v != "PENDING" for v, _ in rows.values()):
            break
        time.sleep(90)
    rows = poll()
    log("=== L16 RESULTS (deputy-fix validation) ===")
    for r, (v, line) in sorted(rows.items()):
        # pull the human label out of the description
        lbl = re.search(r"(L16 [^S]+?)\s{2,}", line)
        log(f"  {r}  {v:>8}  {lbl.group(1).strip() if lbl else ''}")
    dep = [v for r, (v, line) in rows.items() if "DEPUTY" in line]
    valid_dep = [v for v in dep if v not in ("VOID", "PENDING")]
    if valid_dep:
        log(f"FIX WORKS: {len(valid_dep)}/{len(dep)} deputy rungs scored (best {max(valid_dep)}) -> selectable private hedge.")
    else:
        log("DEPUTY STILL VOIDS -> fix insufficient; re-diagnose before another slot.")
    log("done")


if __name__ == "__main__":
    main()
