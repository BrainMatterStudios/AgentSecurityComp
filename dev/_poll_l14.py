#!/usr/bin/env python3
"""Poll the 5 L14 hop-pack submissions until all score, then write the read + verdict.
Logs to logs/l14_results.log."""
import os, re, time, subprocess, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "logs", "l14_results.log")
COMP = "ai-agent-security-multi-step-tool-attacks"
REFS = {
    "55182081": "anchor single-post FRAC97",
    "55182082": "HOPPACK K8 FRAC97 (A/B)",
    "55182084": "HOPPACK K8 FRAC85",
    "55182086": "HOPPACK K8 FRAC93",
    "55182089": "HOPPACK K4 FRAC93",
}


def log(m):
    line = f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}Z  {m}"
    print(line, flush=True); open(LOG, "a").write(line + "\n")


def poll():
    out = subprocess.run(["python3", "-m", "kaggle", "competitions", "submissions", COMP],
                         capture_output=True, text=True, timeout=90)
    scores = {}
    for line in (out.stdout + out.stderr).splitlines():
        for ref in REFS:
            if line.strip().startswith(ref):
                m = re.search(r"COMPLETE\s+([\d.]+)", line)
                if m:
                    scores[ref] = float(m.group(1))
    return scores


def main():
    log("polling L14 scores…")
    for _ in range(240):  # up to ~6h at 90s
        s = poll()
        log(f"  {len(s)}/5 scored… " + " ".join(f"{REFS[r].split()[0]}={s[r]}" for r in REFS if r in s))
        if len(s) == 5:
            break
        time.sleep(90)
    s = poll()
    log("=== L14 RESULTS ===")
    for r, name in REFS.items():
        log(f"  {name:28s} = {s.get(r, 'PENDING')}")
    anc = s.get("55182081"); hp97 = s.get("55182082")
    if anc and hp97:
        delta = hp97 - anc
        log(f"A/B: HOPPACK-K8-FRAC97 {hp97} vs anchor {anc}  =>  {delta:+.2f}")
        log("  reset-overhead-bound (hop-pack WINS -> 112 path)" if delta > 3 else
            "  decode-bound (hop-pack flat/neg -> packing dead, pivot to private)")
    log("done")


if __name__ == "__main__":
    main()
