#!/usr/bin/env python3
"""Poll the 5 L15 per-model-FRAC submissions until all score, then write the read + verdict.
Logs to logs/l15_results.log. (L14's poller was never launched -> empty log; don't repeat that.)"""
import os, re, time, subprocess, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "logs", "l15_results.log")
COMP = "ai-agent-security-multi-step-tool-attacks"
REFS = {
    "55198318": "anchor shared FRAC97",
    "55198319": "ASYM gpt97/gemma99",
    "55198321": "ASYM gpt98/gemma99",
    "55198324": "DEPUTY FRAC95 (private hedge)",
    "55198325": "SHARED FRAC98",
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
    log("polling L15 scores…")
    for _ in range(240):  # up to ~6h at 90s
        s = poll()
        log(f"  {len(s)}/5 scored… " + " ".join(f"{REFS[r].split()[0]}={s[r]}" for r in REFS if r in s))
        if len(s) == 5:
            break
        time.sleep(90)
    s = poll()
    log("=== L15 RESULTS ===")
    for r, name in REFS.items():
        log(f"  {name:30s} = {s.get(r, 'PENDING/VOID')}")
    anc = s.get("55198318")
    a1 = s.get("55198319"); a2 = s.get("55198321"); sh = s.get("55198325")
    if anc:
        best = max(x for x in (a1, a2, sh) if x is not None) if any(x is not None for x in (a1, a2, sh)) else None
        if best is not None:
            delta = best - anc
            log(f"AIM-HIGHER: best climb {best} vs anchor {anc}  =>  {delta:+.2f}")
            log("  gemma/FRAC headroom EXISTS -> push further next night" if delta > 2 else
                "  flat/neg -> public plateau confirmed at the void wall; weight to private hedge + write-up")
    dep = s.get("55198324")
    log(f"DEPUTY (private hedge) public read = {dep if dep is not None else 'PENDING/VOID'}"
        + ("  [valid -> selectable private hedge]" if dep else "  [check void]"))
    log("done")


if __name__ == "__main__":
    main()
