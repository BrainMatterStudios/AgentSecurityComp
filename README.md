# AI Agent Security — Multi-Step Tool Attacks

A submission-ready solution for the Kaggle competition
[**AI Agent Security: Multi-Step Tool Attacks**](https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks):
an **algorithmic red-teaming** attack that searches a deterministic, offline,
Gym-style benchmark for multi-step paths driving a tool-using agent from
*untrusted input* to an *unsafe action*, and returns **replayable** findings the
evaluator can verify.

> **Status / honest scope.** The competition's SDK, starter notebook and live
> targets (GPT-OSS, Gemma) are gated behind Kaggle competition rules and were not
> reachable from the build environment (no Kaggle credentials; Kaggle/arXiv/
> OpenReview are outside its network allow-list). So this repo cannot itself
> submit to the leaderboard. What it **does** provide is the complete solution:
> a coverage-guided attack search, a rich multi-step attack library, a faithful
> local mock environment, passing end-to-end tests, and the judged strategy
> write-up — all behind a one-file adapter so dropping in the real SDK is a
> mechanical change. See `COMPETITION.md` for the full analysis and exactly
> what's needed to submit.

## Quick start

```bash
python run_smoke_test.py     # full pipeline on the bundled mock environment
python tests/test_attack.py  # end-to-end unit tests (no deps, stdlib only)
python attack.py             # the submission's self-test
```

Expected: ~30+ diverse candidates across all three predicates and multiple
scenarios, each verified to replay deterministically in a fresh environment.

## Layout

```
attack.py                  # SUBMISSION entry point: AttackAlgorithm
agentsec/
  candidate.py             # AttackCandidate / AttackAction (replayable findings)
  strategies.py            # attack library: techniques × obfuscations × channels
  search.py                # AttackSearch: coverage-guided, budget-aware loop
  predicates.py            # local proxies for the 3 security predicates
  adapter.py               # << the ONE file to edit for the real SDK >>
mock_env/env.py            # faithful deterministic stand-in for the SDK env
notebooks/starter_submission.py  # Kaggle notebook that writes attack.py
tests/test_attack.py       # end-to-end smoke tests
run_smoke_test.py          # local smoke-test entry point
COMPETITION.md             # competition analysis + submission checklist
STRATEGY.md                # method & security-insight write-up (judged)
```

## The approach in three lines

1. **Hypothesis space** (`strategies.py`): each attack = target-predicate×technique
   (incl. two-stage *laundering*/*staged* attacks) × obfuscation transform ×
   untrusted channel, parameterised by live scenario facts.
2. **Coverage-guided search** (`search.py`): stop refining a `(scenario,
   predicate, technique)` cell once it fires; spend budget broadening coverage
   and escalate obfuscation only where a guardrail is blocking — maximising the
   *severity + diversity* the score rewards while staying under the 9,000 s cap.
3. **One-file SDK boundary** (`adapter.py`): the search and library are written
   against a 3-method adapter, so the same code drives the mock and the real
   GPT-OSS / Gemma targets unchanged.

See **`STRATEGY.md`** for the full method and the defender takeaways
(taint/provenance tracking, whole-trace monitoring, trusted-frame spoofing,
semantic vs lexical guardrails).

## Submitting (requires Kaggle access + the SDK)

1. Accept the competition and obtain its SDK + starter notebook.
2. Port `agentsec/adapter.py` to the SDK's `reset()/step()` API (translation
   points are marked `# >>> SDK`) and confirm the `AttackCandidate` serialization
   the harness expects.
3. Use `notebooks/starter_submission.py` to write `attack.py` + `agentsec/` to
   `/kaggle/working/` and run against the live environment.
