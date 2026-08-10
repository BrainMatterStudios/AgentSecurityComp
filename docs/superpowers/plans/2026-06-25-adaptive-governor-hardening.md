# Adaptive Governor Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the adaptive candidate governor and profile wiring so generated Kaggle kernels honor configured bounds, fail safely, and stay testable.

**Architecture:** Add regression tests around `attack.py` adaptive sizing and `dev/build_notebook.py` profile generation, then make the governor clamp safely, give private-chain its own sizing path, and regenerate the affected submission kernels from the source builder. Keep the current public/private strategy split, but harden it with explicit invariants instead of relying on handoff assumptions.

**Tech Stack:** Python 3, `pytest`, Kaggle notebook generator in `dev/build_notebook.py`

## Global Constraints

- Do not change the Kaggle gateway CSV contract.
- Keep changes minimal and focused on adaptive sizing, profile correctness, and generated-kernel consistency.
- Add tests before production code changes and verify red/green locally.
- Regenerate only the kernels affected by the changed profile logic.

---

### Task 1: Lock down adaptive sizing invariants

**Files:**
- Create: `tests/test_adaptive_profiles.py`
- Modify: `attack.py`

**Interfaces:**
- Consumes: `AttackAlgorithm._adaptive_n(env, budget, max_hops, prompt) -> int`
- Produces: bounded adaptive candidate counts for `_run_k1_short()` and `_run_private_chain()`

- [ ] Add failing tests for max clamp, safe fallback, and private-chain sizing.
- [ ] Run `pytest tests/test_adaptive_profiles.py -q` and verify the expected failures.
- [ ] Patch `attack.py` to clamp adaptive output to `MAX_CANDIDATES`, use a conservative fallback, and size private chains with their own bounded estimate.
- [ ] Re-run `pytest tests/test_adaptive_profiles.py -q` until green.

### Task 2: Lock down notebook profile generation

**Files:**
- Modify: `tests/test_adaptive_profiles.py`
- Modify: `dev/build_notebook.py`

**Interfaces:**
- Consumes: `PROFILES` in `dev/build_notebook.py`
- Produces: explicit adaptive env knobs for generated kernels

- [ ] Add failing tests asserting adaptive profiles emit their intended bounds and carry required env knobs.
- [ ] Run targeted pytest again and verify failures are caused by current profile wiring.
- [ ] Patch `dev/build_notebook.py` profile env maps to match the corrected governor behavior.
- [ ] Re-run targeted pytest until green.

### Task 3: Regenerate affected kernels and verify artifacts

**Files:**
- Modify: `submission_kernel_k1_adaptive/jed-multistep-tool-attack.ipynb`
- Modify: `submission_kernel_private_chain_400/jed-multistep-tool-attack.ipynb`
- Modify: `submission_kernel_k1_640/jed-multistep-tool-attack.ipynb`
- Modify: `submission_kernel_k1_680/jed-multistep-tool-attack.ipynb`
- Modify: `submission_kernel_k1_720/jed-multistep-tool-attack.ipynb`

**Interfaces:**
- Consumes: `python3 dev/build_notebook.py <profile>`
- Produces: regenerated notebooks aligned with source-of-truth profile config

- [ ] Regenerate the affected notebooks from `dev/build_notebook.py`.
- [ ] Run targeted tests plus a lightweight generation check to confirm the notebooks embed the corrected env settings.
- [ ] Summarize exact behavior changes and residual risks.
