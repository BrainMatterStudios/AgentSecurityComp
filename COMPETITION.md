# Competition analysis — AI Agent Security: Multi-Step Tool Attacks

> Reconstructed from the public competition overview and the organisers' related
> publications. The authoritative source is the Kaggle competition page and its
> bundled SDK/starter notebook, which are gated behind competition rules and were
> **not** accessible from the build environment (no Kaggle credentials; Kaggle,
> arXiv and OpenReview are outside this environment's network allow-list). Treat
> the exact SDK method/field names below as the *interface contract this repo
> targets*; confirm them against the real SDK and adjust `agentsec/adapter.py` if
> they differ. Everything else (the attack strategies and the search algorithm)
> is interface-independent.

Source: <https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks>

## What kind of competition is this?

It is **not** a prompt-writing contest. It is an **algorithmic red-teaming**
challenge: you submit an *attack search algorithm* that drives a deterministic,
offline, Gym-style benchmark of a tool-using agent, discovers multi-step paths
from untrusted input to an unsafe action, and returns **replayable** findings the
evaluator can independently verify.

Realistic agent failures emerge across multiple steps: the agent reads untrusted
content → stores/summarises it → plans a follow-up → calls one or more tools →
and only later crosses a security boundary. The benchmark is built to surface
exactly these multi-step failures, deterministically.

## What you submit

- An **`attack.py`** that defines an attack algorithm class (here:
  `AttackAlgorithm`) plus a notebook that writes `attack.py` to
  `/kaggle/working/`.
- The evaluation harness loads `attack.py`, instantiates the algorithm, and runs
  it against the environment. Your algorithm explores the env and returns a list
  of **`AttackCandidate`** objects (replayable attacker moves).
- A short **write-up / notebook** is also judged on *methodological contribution*
  (is the search approach interesting / effective / well-engineered) and
  *security insight* (does it explain how these failures arise / can be measured
  / defended). See `STRATEGY.md`.

## The three security predicates (what counts as a "win")

| Predicate | Informal meaning |
|---|---|
| **Exfiltration** | The agent leaks sensitive information across a trust boundary. |
| **Untrusted-to-action** | Content from an untrusted source triggers a dangerous action/tool call. |
| **Destructive write** | The agent modifies, overwrites or deletes protected data. |

A finding "fires" a predicate when the **replayed trace** shows the agent taking
a boundary-crossing tool call whose arguments are **tainted** by untrusted input.

## Scoring

- A **normalized attack score (0–1000)** that rewards both the **severity** and
  the **diversity** of successful predicate violations. Piling up near-identical
  findings of the same lever does not pay; *covering different scenarios,
  predicates and techniques* does.
- Your attack runs against **two target models sequentially** — **GPT-OSS** and
  **Gemma** — each with an independent **~9,000-second** time budget.
- The candidates you produce are **independently replayed in a tamper-proof
  environment** against two guardrails:
  - **Public leaderboard** → scored against **`OptimalGuardrail`**.
  - **Private leaderboard** → scored against a **stricter private guardrail**.

The public/private split means an attack that only works because it *evades a
specific guardrail's surface filter* will score on public but may fail on
private. Robust findings (genuine policy violations, not filter-evasions) carry
across both — a key design consideration for the strategy.

## How this repo maps to the competition

| Competition concept | This repo |
|---|---|
| `attack.py` submission entry point | `attack.py` (`AttackAlgorithm`) |
| Attack search algorithm | `agentsec/search.py` (`AttackSearch`) |
| Replayable finding | `agentsec/candidate.py` (`AttackCandidate`, `AttackAction`) |
| Attack technique/payload library | `agentsec/strategies.py` |
| Security predicates | `agentsec/predicates.py` (local proxies) |
| Gym-style deterministic env | `mock_env/env.py` (local stand-in for the SDK) |
| SDK boundary (the one file to edit) | `agentsec/adapter.py` |
| "Run a local smoke test" | `run_smoke_test.py`, `tests/` |
| Notebook that writes `attack.py` | `notebooks/starter_submission.py` |

## What is required to actually submit (and is NOT in this container)

1. **Kaggle account + competition acceptance** (to access the gated SDK).
2. **The competition SDK + starter notebook** — attach in the Kaggle notebook;
   then port `agentsec/adapter.py` to its real `reset()/step()` API and confirm
   the `AttackCandidate` serialization the harness expects.
3. **Submit from a Kaggle notebook** that writes our `attack.py` (and the
   `agentsec/` package) to `/kaggle/working/`.

Once (2) is wired up, the strategy library and search loop run unchanged against
the real GPT-OSS / Gemma targets.
