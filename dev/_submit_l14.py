#!/usr/bin/env python3
"""Submit the 5 L14 hop-pack kernels using the versions recorded by _push_l14.py.
Reads logs/l14_versions.json. Idempotent-ish: logs each submit result to logs/l14_submit.log.
Run AFTER _push_l14.py completes (all 5 versions present)."""
import os, json, subprocess, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "logs", "l14_submit.log")
VJSON = os.path.join(ROOT, "logs", "l14_versions.json")
COMP = "ai-agent-security-multi-step-tool-attacks"

MSG = {
    "ahmedmobasher86/jed-public-pt-safe":   "L14 ANCHOR single-post FRAC=97 (~89.55 floor/canary)",
    "ahmedmobasher86/jed-public-pt-probe":  "L14 HOPPACK K=8 FRAC=97 (direct A/B vs anchor)",
    "ahmedmobasher86/jed-public-k1nx-1000": "L14 HOPPACK K=8 FRAC=85 (void insurance)",
    "ahmedmobasher86/jed-public-k1nx-1200": "L14 HOPPACK K=8 FRAC=93 (FRAC curve)",
    "ahmedmobasher86/jed-public-k1nx-800":  "L14 HOPPACK K=4 FRAC=93 (K-slope)",
}
ORDER = list(MSG.keys())


def log(m):
    line = f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}Z  {m}"
    print(line, flush=True); open(LOG, "a").write(line + "\n")


def main():
    if not os.path.exists(VJSON):
        log("ERROR: no versions file. Run _push_l14.py first."); return
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
    log("L14 submit complete. Poll: python3 -m kaggle competitions submissions %s" % COMP)


if __name__ == "__main__":
    main()
