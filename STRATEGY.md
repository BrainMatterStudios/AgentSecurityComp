# Strategy & method write-up

*Multi-step tool-attack search for the AI Agent Security competition.*

This is the document the competition judges on two axes — **methodological
contribution** (is the search interesting / effective / well-engineered) and
**security insight** (does it explain how the failures arise and how they might
be measured or defended). It describes the algorithm in `agentsec/` and the
reasoning behind it.

## 1. Threat model in one paragraph

A tool-using agent serves a benign user request, but along the way it ingests
content from an **untrusted channel** (an email, a web page, a file, a calendar
invite). A capable model treats instructions embedded in that content with more
deference than it should. The attacker never speaks to the agent directly; the
attacker only controls *what the untrusted channel says*. A successful attack is
a sequence of injected content (and the agent turns that process it) that ends
with the agent taking a **boundary-crossing tool call whose arguments are
tainted by the untrusted content** — exfiltration, an unauthorised dangerous
action, or a destructive write.

## 2. Why a *search* (not a clever prompt)

The competition is scored on **coverage and diversity** across scenarios,
predicates, and techniques — not on one perfect jailbreak. That reframes the
problem from "write the best payload" to "**efficiently search a structured
hypothesis space and keep the diverse subset that actually works**." So the
submission is an algorithm with three pieces:

1. A **structured hypothesis space** of attacks (`strategies.py`).
2. A **coverage-guided, budget-aware search** over it (`search.py`).
3. A **thin environment adapter** so the same search drives the mock and the real
   GPT-OSS / Gemma targets unchanged (`adapter.py`).

## 3. The hypothesis space (`strategies.py`)

Each candidate attack is the composition of three independent axes. Factoring the
space this way is what makes coverage tractable and the findings diverse by
construction.

**Axis A — target predicate × technique class.** For each of the three
predicates we encode several *levers* — the structural/psychological reason a
model crosses the boundary:

- *Exfiltration*: `direct` (system-notice framing), `authority` (impersonate IT
  Security), `launder` (**two-stage**: copy secret into an innocuous note now,
  publish the note later — defeats single-call predicates), `conditional` (tie
  the leak to completing the user's own task).
- *Untrusted→action*: `direct` (pre-approval framing), `data_disguise` (hide the
  imperative inside a data record the agent is parsing), `workflow` (present the
  dangerous call as "the next step").
- *Destructive write*: `cleanup` (maintenance pretext), `overwrite` ("the data is
  corrupt"), `staged` (**two-stage**: plant a deletion TODO, then trigger
  plan execution).

**Axis B — obfuscation transform.** Intent-preserving surface perturbations that
slip past keyword/pattern guardrails without changing meaning: `plain`,
`tool_result_spoof` (wrap the payload to look like a *trusted tool result*),
`base64` (decode-and-comply), `split` (reassemble fragments), `homoglyph`,
`zero_width`. These exist precisely because the public board scores against
`OptimalGuardrail` and the private board against a stricter one.

**Axis C — delivery channel.** Which untrusted channel the scenario exposes
(email / web / file / calendar), read from the live observation.

Payloads are **parameterised by live scenario facts** (the secret's name, where
it lives, a plausible attacker sink, the protected resource, the available
dangerous tool). The adapter reads these from the environment observation, so the
same technique specialises itself to each scenario rather than being a static
string.

## 4. The search algorithm (`search.py`)

`AttackSearch.run()` is **coverage-first and budget-aware**:

- **Stop refining a solved cell.** A "cell" is `(scenario, predicate,
  technique)`. As soon as a cell fires, it is marked satisfied and never retried
  with another obfuscation. Budget goes to *broadening coverage*, which is what
  the diversity term rewards — not to piling up duplicates.
- **Cheap before expensive.** A first sweep uses `plain` (and the cheap
  `tool_result_spoof`) payloads. Heavier obfuscation passes (`base64`, `split`,
  `homoglyph`, `zero_width`) run only over the cells that didn't already fire —
  i.e. exactly the cells where a guardrail is plausibly blocking us, which is
  where obfuscation has marginal value.
- **Diversity de-duplication.** Findings are keyed by a coarse signature
  (`scenario::predicate::technique`, deliberately *excluding* exact payload text)
  so trivial wording changes can't inflate the diversity score and we keep one
  representative per distinct lever.
- **Graceful degradation.** Every probe checks the remaining wall-clock budget
  (default 8,700 s, under the 9,000 s cap) and the loop always returns whatever
  it has confirmed — never risking a timeout that forfeits all findings.

This is intentionally model-agnostic. The same loop runs against GPT-OSS and
Gemma; differences in their robustness simply change *which* cells fire and which
need obfuscation — the algorithm adapts automatically.

## 5. Public vs private guardrail — designing for robustness

There is a tension the scoring makes explicit. Two ways to "fire" a predicate:

1. **Genuine policy violation** — the model really does take the unsafe action.
   Carries across *both* guardrails.
2. **Filter evasion** — the action would be blocked, but an obfuscation hid it
   from a *specific* guardrail's surface check. Scores on public, may die on
   private.

The search prefers (1) by trying `plain`/`tool_result_spoof` first and only
escalating to evasion-style obfuscation where needed — so the highest-value,
most transferable findings are discovered first, and the budget isn't spent
over-fitting the public guardrail. The two-stage `launder`/`staged` techniques
target a *structural* weakness (predicates that only inspect a single tool call),
which is robust to guardrail wording and a genuine insight for defenders.

## 6. Security insight for defenders

The findings this search produces point at concrete, measurable defences:

- **Provenance/taint tracking is the crux.** Every predicate here is "a
  boundary-crossing call whose args are tainted by untrusted content." Agents
  that propagate a taint label from untrusted channels to tool arguments — and
  require human confirmation when a *tainted* argument reaches an
  exfiltration/destructive/financial tool — neutralise the whole class.
- **Single-call predicates are insufficient.** The `launder`/`staged` techniques
  show that monitoring must reason over the *whole trace* (secret copied →
  note → published two turns later), not per-call.
- **Trusted-frame spoofing.** `tool_result_spoof` shows models over-trust content
  that *looks* like their own tool output; tool results must be cryptographically
  or structurally distinguishable from ingested data.
- **Keyword guardrails are brittle.** That `base64`/`split`/`homoglyph` flips
  blocked cells into hits is the empirical argument for semantic (not lexical)
  guardrails and for decoding/normalising content before policy checks.

## 7. How it's validated here

Without the gated SDK we cannot run the real GPT-OSS/Gemma targets, so the repo
ships a **faithful deterministic mock** (`mock_env/`) — a reactive agent + a
keyword guardrail (plus a `strict_guardrail` mode standing in for the private
board). `run_smoke_test.py` and `tests/` demonstrate the full pipeline:

- the search finds **diverse findings across all three predicates and multiple
  scenarios**;
- the guardrail/obfuscation dynamics behave as designed (robust scenarios only
  crack once obfuscation hides the payload from the guard);
- **every returned candidate replays deterministically in a fresh environment** —
  the exact property the real evaluator depends on.

Porting to the real benchmark is a single file (`agentsec/adapter.py`): translate
`AttackAction` ↔ `env.step(...)` and read the fired predicates back from the
SDK's scored trace.
