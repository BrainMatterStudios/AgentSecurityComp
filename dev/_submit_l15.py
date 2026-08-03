#!/usr/bin/env python3
"""Submit the 5 L15 per-model-FRAC kernels using versions recorded by _push_l15.py.
Reads logs/l15_versions.json. Logs each submit result to logs/l15_submit.log.
Run AFTER _push_l15.py completes (all 5 versions present, save-runs COMPLETE)."""
import os, json, subprocess, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "logs", "l15_submit.log")
VJSON = os.path.join(ROOT, "logs", "l15_versions.json")
COMP = "ai-agent-security-multi-step-tool-attacks"

MSG = {
    "ahmedmobasher86/jed-public-pt-safe":   "L15 ANCHOR single-post shared FRAC=97 (~89.6 floor/canary)",
    "ahmedmobasher86/jed-public-pt-probe":  "L15 ASYM gpt97/gemma99 (isolate gemma FRAC headroom; aim-higher A/B)",
    "ahmedmobasher86/jed-public-k1nx-1000": "L15 ASYM gpt98/gemma99 (aggressive climb toward the wall)",
    "ahmedmobasher86/jed-public-k1nx-1200": "L15 DEPUTY clean CONFUSED_DEPUTY FRAC=95 (private $50k hedge)",
    "ahmedmobasher86/jed-public-k1nx-800":  "L15 SHARED FRAC=98 (single-knob climb, code-independent)",
}
ORDER = list(MSG.keys())


def log(m):
    line = f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}Z  {m}"
    print(line, flush=True); open(LOG, "a").write(line + "\n")


def main():
    if not os.path.exists(VJSON):
        log("ERROR: no versions file. Run _push_l15.py first."); return
    versions = json.load(open(VJSON))
    log(f"submitting {len(versions)} kernels: " + ", ".join(f"{k.split('/')[-1]}=v{v}" for k, v in versions.items()))
    for slug in ORDER:
        v = versions.get(slug)
        if v is None:
            log(f"SKIP {slug}: no version recorded"); continue
        out = subprocess.run(
            ["python3", "-m", "kaggle", "competitions", "submit", COMP,
             "-k", slug, "-v", str(v), "-f", "submission.csv", "-m", MSG[slug]],
            capture_output=True, text=True, timeout=180)
        txt = (out.stdout + out.stderr).strip().splitlines()
        log(f"{slug.split('/')[-1]} v{v}: {txt[-1] if txt else '(no output)'}")
    log("L15 submit complete. Poll: python3 -m kaggle competitions submissions %s" % COMP)


if __name__ == "__main__":
    main()
