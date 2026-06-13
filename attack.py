"""attack.py -- the competition submission entry point.

The evaluation harness loads this file from ``/kaggle/working/`` and runs the
attack algorithm against each target model (GPT-OSS, then Gemma) within a
per-target time budget, replaying the returned candidates against the guardrails.

This file exposes the conventional shapes the harness may look for and keeps the
actual logic in the ``agentsec`` package:

    class AttackAlgorithm:        # instantiated by the harness
        def run(self, env, budget_seconds=...) -> list[AttackCandidate]

We also expose a module-level ``run(env, ...)`` and an ``attack(env, ...)`` alias
so the file is robust to small differences in how the harness invokes it. The
returned objects are ``AttackCandidate``s; ``.to_dict()`` is available if the
harness expects plain dicts.

To run against the REAL SDK environment, the only change needed is in
``agentsec/adapter.py`` (translate AttackAction <-> env.step). Everything here
stays the same.
"""

from __future__ import annotations

import os
from typing import Any, List, Optional

from agentsec import AttackCandidate, AttackSearch, EnvAdapter

# Per-target wall-clock budget. The competition allots ~9000s per target model;
# we leave a safety margin so we always return before the harness times us out.
DEFAULT_BUDGET_SECONDS = float(os.environ.get("ATTACK_BUDGET_SECONDS", "8700"))


def _wrap(env: Any) -> EnvAdapter:
    """Accept either a raw SDK/mock env or an already-built EnvAdapter."""
    return env if isinstance(env, EnvAdapter) else EnvAdapter(env)


class AttackAlgorithm:
    """Coverage-guided, budget-aware multi-step tool-attack search.

    Strategy (see STRATEGY.md and agentsec/search.py for detail):
      * Enumerate untrusted-channel injections crossed with a library of
        multi-step injection techniques and obfuscation transforms.
      * Target all three predicate families (exfiltration, untrusted->action,
        destructive write), seeding payloads from live scenario facts.
      * Reward diversity: stop refining a (scenario, predicate, technique) cell
        once it fires; spend remaining budget broadening coverage and escalating
        obfuscation only where a guardrail is blocking us.
    """

    def __init__(self, budget_seconds: float = DEFAULT_BUDGET_SECONDS,
                 verbose: bool = True):
        self.budget_seconds = budget_seconds
        self.verbose = verbose

    def run(self, env: Any,
            budget_seconds: Optional[float] = None) -> List[AttackCandidate]:
        log = print if self.verbose else (lambda m: None)
        search = AttackSearch(
            _wrap(env),
            budget_seconds=budget_seconds or self.budget_seconds,
            log=log,
        )
        return search.run()

    # Some harness variants call ``search`` or ``attack``; alias them.
    search = run
    attack = run


# Module-level conveniences (harness-agnostic).
def run(env: Any, budget_seconds: float = DEFAULT_BUDGET_SECONDS,
        **_: Any) -> List[AttackCandidate]:
    return AttackAlgorithm(budget_seconds=budget_seconds).run(env)


attack = run


if __name__ == "__main__":
    # Local self-test against the mock environment.
    from agentsec import build_default_adapter

    adapter = build_default_adapter()
    candidates = AttackAlgorithm(budget_seconds=60).run(adapter)
    print(f"\nProduced {len(candidates)} candidates:")
    for c in candidates:
        print(f"  - {c.target_predicate:20s} {c.scenario_id:16s} "
              f"{c.metadata.get('technique')}/{c.metadata.get('obfuscation')}")
