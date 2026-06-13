# HANDOFF — instructions for the next session

You are picking up an in-progress entry for the Kaggle competition
**AI Agent Security: Multi-Step Tool Attacks**
(<https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks>).
This document is the single source of truth for what exists, what's blocked, and
exactly what to do next.

## 1. Current status (what's already done)

A complete, tested, **submission-ready solution scaffold** is in this repo. It
runs green end-to-end against a local mock environment. Read these first:

- `README.md` — orientation + quick start.
- `COMPETITION.md` — full competition analysis + submission checklist.
- `STRATEGY.md` — the method & security-insight write-up (this is judged).

Verify it still works:

```bash
python run_smoke_test.py     # ~30+ diverse findings, all replay deterministically
python tests/test_attack.py  # 6/6 pass, stdlib only
python attack.py             # submission self-test
```

Key code:
- `attack.py` — submission entry point (`AttackAlgorithm`).
- `agentsec/strategies.py` — attack library (techniques × obfuscations × channels).
- `agentsec/search.py` — coverage-guided, budget-aware search loop.
- `agentsec/adapter.py` — **the one file to edit to target the real SDK.**
- `mock_env/env.py` — deterministic stand-in for the SDK env (dev/test only).

## 2. The one thing that was blocking the previous session

**Network egress.** The previous (web) environment's proxy blocked
`www.kaggle.com` (`x-deny-reason: host_not_allowed`), so the Kaggle API/SDK could
not be reached even with valid credentials. `github.com`, `pypi.org` and
`storage.googleapis.com` were open; `www.kaggle.com` was not.

**If you are running from the user's local CLI, this is probably already solved**
(normal machine has Kaggle access). Confirm first:

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://www.kaggle.com
```

A `200`/`301`/`401` means you can reach Kaggle — proceed. A `403` with
`host_not_allowed` means egress is still blocked and the environment's network
policy must allow `www.kaggle.com` before anything else will work.

## 3. Credentials

Kaggle auth needs a `username` + `key` pair at `~/.kaggle/kaggle.json`
(chmod 600), or the env vars `KAGGLE_USERNAME` / `KAGGLE_KEY`. The user has a
valid pair (username `ahmedmobasher86`). It is **not** committed to the repo
(secrets must never be committed). Ensure it's present:

```bash
mkdir -p ~/.kaggle && chmod 600 ~/.kaggle/kaggle.json   # after placing the file
python -c "import json,os;print(json.load(open(os.path.expanduser('~/.kaggle/kaggle.json')))['username'])"
```

## 4. Step-by-step to finish and submit

```bash
# (a) Tooling
pip install kaggle

# (b) Accept the rules on the competition page in a browser ONCE, then:
kaggle competitions download -c ai-agent-security-multi-step-tool-attacks -p ./comp
unzip -o ./comp/*.zip -d ./comp

# (c) Locate the SDK + starter notebook in ./comp. Read them to learn the REAL:
#       - environment construction (make_env / reset / step signatures)
#       - AttackCandidate / action serialization the harness expects
#       - how attack.py is invoked (class name, method name, return type)
```

Then **port `agentsec/adapter.py`** (only this file should need changing). The
search and strategy library are written against its 3-method surface:
`list_scenarios()`, `scenario_facts(id)`, `replay(id, actions)`. Map:
- `reset(scenario_id)` → real env reset; pull scenario facts from the real
  observation (fill `ScenarioFacts` in `scenario_facts`).
- each `AttackAction` (`inject` / `advance` / `set_user_request`) → the real
  `env.step(...)` call(s).
- read the fired predicates back from the real scored trace in `replay`.

If the real harness expects a different entry-point shape than
`AttackAlgorithm.run(env) -> list[AttackCandidate]`, adapt `attack.py` (it already
aliases `run`/`attack`/`search` and exposes `.to_dict()` on candidates).

```bash
# (d) Smoke-test against the REAL env (small budget first), then full run:
#     adapt notebooks/starter_submission.py, or drive it directly:
python -c "from <sdk> import make_env; from agentsec import EnvAdapter; \
from attack import AttackAlgorithm; \
print(len(AttackAlgorithm(budget_seconds=300).run(EnvAdapter(make_env()))))"

# (e) Submit via a Kaggle notebook that writes attack.py + agentsec/ to
#     /kaggle/working/ (see notebooks/starter_submission.py), or per the
#     competition's documented submission flow.
```

## 5. Where to push improvements (if the SDK isn't reachable yet)

The scoring rewards **severity + diversity** across scenarios/predicates/
techniques. High-value, interface-independent improvements to make against the
mock now:
- More technique classes per predicate (esp. multi-step / cross-tool chains).
- A light mutation / hill-climbing pass on *near-misses* (cells that didn't fire)
  before escalating obfuscation — `agentsec/search.py` is the place.
- Smarter `ScenarioFacts` extraction so payloads specialise harder per scenario.
- Keep the diversity de-dup (`AttackCandidate.signature`) honest.

## 6. Git

Work is on branch `claude/ai-agent-security-challenge-dcdgzz` and mirrored to
`main`. Develop on whichever the user prefers; **do not commit secrets**
(`~/.kaggle/kaggle.json`, tokens). `.gitignore` already excludes
`candidates*.json` and caches.

## 7. The honest bar for "solved"

The competition's success metric is a leaderboard score (normalized 0–1000,
public=OptimalGuardrail, private=stricter). You cannot claim "solved" until
candidates have actually been produced against the real GPT-OSS/Gemma targets and
submitted. Everything up to that point (algorithm, library, tests, write-up) is
done; the finish line is steps (a)–(e) above once Kaggle is reachable.
