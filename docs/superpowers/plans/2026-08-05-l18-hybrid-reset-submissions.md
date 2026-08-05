# L18 Hybrid Reset Submissions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, verify, push, and arm a five-submission L18 hybrid set that includes a current replay-safe anchor, validation-gated exact Gemma `a.co/1..8` probes, one safer public-style split, and one bounded stretch rung.

**Architecture:** Keep the core attack in `attack.py` and add a selectable Gemma forge URL topology so the exact locally positive `http://a.co/1..8` probe can be shipped without changing existing L17 behavior. Add L18 build/push/submit/poll scripts parallel to L17, but make the submitter outcome-safe by confirming new Kaggle submission refs before writing the marker. Use CPU save-runs for notebook pushing so GPU quota does not block arming; competition hidden replay still runs the target model servers.

**Tech Stack:** Python, pytest, Kaggle CLI, local `aicomp_sdk` source.

## Global Constraints

- Do not submit immediately during implementation; arm only after explicit user approval, which was given in this turn.
- Do not write a submission marker unless all five Kaggle submission refs are confirmed.
- Exact Gemma forge experimental rungs must require `JED_GEMMA_FORGE_MIN_POSTS >= 6`, so hidden 3-post behavior falls back instead of repeating L17.
- Keep notebooks private, no internet, and competition source `ai-agent-security-multi-step-tool-attacks`.

---

### Task 1: Exact Gemma `a.co/1..8` Forge Mode

**Files:**
- Modify: `attack.py`
- Modify: `tests/test_l17_gemma_forge.py`

**Interfaces:**
- Consumes: existing `_gemma_forge_msg(marker, candidate_index, k)`.
- Produces: `JED_GEMMA_FORGE_REPEAT_A_PATHS=1`, which makes `_gemma_forge_msg` ignore `candidate_index` and emit the exact repeated `http://a.co/1..k` topology from `dev/_gemma_forge_probe.py`.

- [ ] Add failing test asserting the exact repeated `a.co` topology.
- [ ] Run `python3 -m pytest tests/test_l17_gemma_forge.py::test_gemma_forge_repeat_a_paths_matches_positive_probe_shape -q` and verify it fails.
- [ ] Implement the env-gated topology in `attack.py`.
- [ ] Run the focused test and the existing L17 forge tests.

### Task 2: L18 Builder

**Files:**
- Create: `dev/_build_l18.py`
- Create: `tests/test_l18_build.py`

**Interfaces:**
- Produces `RUNGS`, each tuple `(directory, slug, title, env, note)`.
- Produces five `submission_kernel_l18_*` directories with `k.ipynb` and `kernel-metadata.json`.

- [ ] Add failing tests for the five-rung hybrid layout.
- [ ] Implement `dev/_build_l18.py` by following the L17 builder skeleton.
- [ ] Run `python3 -m pytest tests/test_l18_build.py -q`.

### Task 3: L18 Push And Outcome-Safe Submitter

**Files:**
- Create: `dev/_push_l18.py`
- Create: `dev/_submit_l18_at_reset.py`
- Create: `dev/_poll_l18.py`
- Create: `tests/test_l18_submitter.py`

**Interfaces:**
- `dev/_push_l18.py` writes `logs/l18_versions.json`.
- `dev/_submit_l18_at_reset.py` writes `logs/l18_submitted.marker` only after five refs are confirmed.
- `dev/_poll_l18.py` filters submissions by `L18`.

- [ ] Add failing tests for marker refusal on incomplete confirmation and marker writing on five confirmed refs.
- [ ] Implement push/poll scripts and the ref-confirming submitter.
- [ ] Run `python3 -m pytest tests/test_l18_submitter.py -q`.

### Task 4: Build, Verify, Push, And Arm

**Files:**
- Generate: `submission_kernel_l18_*`
- Generate: `logs/l18_versions.json`
- Generate: `logs/l18_reset_run.log`

- [ ] Run focused tests: `python3 -m pytest tests/test_l17_gemma_forge.py tests/test_l18_build.py tests/test_l18_submitter.py -q`.
- [ ] Run `python3 dev/_build_l18.py`.
- [ ] JSON-validate generated notebooks and metadata.
- [ ] Run `python3 dev/_push_l18.py`.
- [ ] Verify all five saved versions exist.
- [ ] Arm reset submitter with `nohup caffeinate -i python3 dev/_submit_l18_at_reset.py > logs/l18_reset_run.log 2>&1 &`.
