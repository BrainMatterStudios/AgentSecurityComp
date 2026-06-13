"""Kaggle submission notebook (as a plain script).

Paste these cells into a Kaggle notebook attached to the competition. It writes
the attack package + `attack.py` to `/kaggle/working/` (what the evaluation
harness loads), runs the bundled local smoke test, then -- once the real SDK is
attached -- runs the attack against the live environment.

Convert to a notebook with e.g. `jupytext --to notebook starter_submission.py`,
or copy each `# %% [cell]` block manually.
"""

# %% [markdown]
# # AI Agent Security — Multi-Step Tool Attacks: submission
# Coverage-guided, budget-aware multi-step tool-attack search.
# See `STRATEGY.md` for the method and `COMPETITION.md` for the analysis.

# %% [code]
# --- 1. Materialise the attack code into /kaggle/working ---------------------
# In a real submission, commit the `agentsec/` package + `attack.py` as a Kaggle
# Dataset/Utility script and import it, OR write them out here. The simplest
# robust path is to attach this repo as a utility dataset and copy it:
import os, shutil, sys

WORKING = "/kaggle/working"
os.makedirs(WORKING, exist_ok=True)

# If the repo is attached as an input dataset, copy the package + entrypoint.
REPO_SRC = "/kaggle/input/agent-security-comp"  # adjust to your dataset slug
if os.path.isdir(REPO_SRC):
    for item in ("agentsec", "attack.py"):
        src = os.path.join(REPO_SRC, item)
        dst = os.path.join(WORKING, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        elif os.path.isfile(src):
            shutil.copy2(src, dst)
    print("Copied agentsec/ and attack.py into", WORKING)
else:
    print("Attach the repo as an input dataset, or write the files inline here.")

sys.path.insert(0, WORKING)

# %% [code]
# --- 2. Local smoke test against the bundled mock environment ----------------
# Proves the pipeline runs before we spend the (expensive) real-target budget.
if os.path.isdir(os.path.join(REPO_SRC, "mock_env")):
    shutil.copytree(os.path.join(REPO_SRC, "mock_env"),
                    os.path.join(WORKING, "mock_env"), dirs_exist_ok=True)
from agentsec import AttackSearch, build_default_adapter  # noqa: E402
cands = AttackSearch(build_default_adapter(), budget_seconds=60).run()
print(f"Smoke test: {len(cands)} diverse candidates across",
      {c.target_predicate for c in cands})

# %% [code]
# --- 3. Wire up the REAL competition SDK -------------------------------------
# Attach the competition SDK (from the competition page) and adapt
# `agentsec/adapter.py` to its reset()/step() API. Then:
#
#   from competition_sdk import make_env          # name per the SDK
#   from agentsec import EnvAdapter
#   from attack import AttackAlgorithm
#
#   env = make_env()                              # the deterministic benchmark
#   algo = AttackAlgorithm(budget_seconds=8700)   # < 9000s per-target cap
#   candidates = algo.run(EnvAdapter(env))        # or algo.run(env)
#
# The harness then replays `candidates` against OptimalGuardrail (public) and the
# private guardrail. `attack.py` already exposes AttackAlgorithm / run / attack
# so most harness conventions are covered.
print("Ready. Adapt agentsec/adapter.py to the real SDK and run the attack.")
