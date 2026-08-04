# L17 Gemma Forge Submission Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, validate, push, and arm five L17 Kaggle submissions testing the locally successful Gemma special-token forge while preserving the proven gpt/exfil fallback.

**Architecture:** Add a dedicated `JED_GEMMA_FORGE` branch to `attack.py` that fingerprints the live model. On gemma it emits validated special-token forged multi-post candidates; on gpt it emits the proven single-post `close_ok` replay-safe branch. Generate five Kaggle notebooks with distinct L17 configs and a reset submitter that is marker-idempotent.

**Tech Stack:** Python stdlib, existing `aicomp_sdk` contract, existing Kaggle CLI scripts, pytest.

## Global Constraints

- Do not submit before explicit approval; the user has now approved arming the reset submitter for tonight.
- Quota is 5 submissions per UTC day, reset at 00:00 UTC.
- Reuse the five rotation slugs: `jed-public-pt-safe`, `jed-public-pt-probe`, `jed-public-k1nx-1000`, `jed-public-k1nx-1200`, `jed-public-k1nx-800`.
- Keep `enable_gpu: true`, `machine_shape: "NvidiaTeslaT4"`, `enable_internet: false`, and competition source `ai-agent-security-multi-step-tool-attacks`.
- Stop before merging/pushing git. Kaggle kernel push and reset arming are allowed by the user's explicit request.

---

### Task 1: Gemma Forge Mode

**Files:**
- Modify: `attack.py`
- Test: `tests/test_l17_gemma_forge.py`

**Interfaces:**
- Consumes: `AttackAlgorithm._FP_PROBES`, `AttackCandidate.from_messages`, `EXFIL_PAYLOAD`, `_rs_url`.
- Produces: `JED_GEMMA_FORGE=1`, `JED_GEMMA_FORGE_K`, `JED_GEMMA_FORGE_N`, `JED_GEMMA_FORGE_GPT_FRAC`.

- [x] Write failing tests for forged message content, length, and gpt fallback behavior.
- [x] Run pytest and confirm tests fail because the mode is missing.
- [x] Implement `_gemma_forge_msg`, `_run_gemma_forge`, and a run-dispatch hook.
- [x] Run pytest and confirm tests pass.

### Task 2: L17 Notebook Tooling

**Files:**
- Create: `dev/_build_l17.py`
- Create: `dev/_push_l17.py`
- Create: `dev/_submit_l17_at_reset.py`
- Create: `dev/_poll_l17.py`
- Test: `tests/test_l17_build.py`

**Interfaces:**
- Consumes: `attack.py` bytes embedded as base64.
- Produces: `submission_kernel_l17_*` directories, `logs/l17_versions.json`, `logs/l17_submitted.marker`.

- [x] Write failing tests asserting L17 run configs, metadata, notebook env cells, and submit messages.
- [x] Run pytest and confirm tests fail because builder is missing.
- [x] Implement builder and submit/push/poll scripts following the L16 pattern.
- [x] Run pytest and confirm tests pass.

### Task 3: Local Preflight

**Files:**
- Modify only if tests expose defects.

**Interfaces:**
- Consumes: local gpt/gemma GGUF replicas when available.
- Produces: model-mechanic confidence and built notebooks.

- [x] Run focused pytest: `python3 -m pytest tests/test_l17_gemma_forge.py tests/test_l17_build.py -q`.
- [x] Run existing adaptive tests: `python3 -m pytest tests/test_adaptive_profiles.py -q`.
- [x] Run gemma forge local probe or an equivalent smoke check on the exact message shape. Distinct-host local result is 3 posts/candidate for K=8 and K=4, so L17 uses `JED_GEMMA_FORGE_MIN_POSTS=3` rather than self-disabling at 4.
- [x] Build L17 notebooks and run JSON/metadata preflight.

### Task 4: Kaggle Push and Arm

**Files:**
- Generate: `submission_kernel_l17_*`
- Generate: `logs/l17_versions.json`
- Generate after arming fires: `logs/l17_submitted.marker`

**Interfaces:**
- Consumes: Kaggle CLI credentials and five rotation kernel slugs.
- Produces: saved kernel versions and a reset submitter process.

- [x] Run `python3 dev/_build_l17.py`.
- [ ] Run `python3 dev/_push_l17.py` and verify every save-run completes.
- [ ] Arm with `nohup caffeinate -i python3 dev/_submit_l17_at_reset.py > logs/l17_reset_run.log 2>&1 &`.
- [ ] Report PID, versions, and exact submissions that will fire at reset.

## Self-Review

- Coverage: The plan covers attack mode, notebook generation, preflight, push, and arming.
- Placeholder scan: No TBD/TODO placeholders remain.
- Type consistency: New env names are consistently prefixed `JED_GEMMA_FORGE`.
