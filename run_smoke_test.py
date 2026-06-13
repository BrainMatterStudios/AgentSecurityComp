#!/usr/bin/env python3
"""Local smoke test -- mirrors the competition's "run a local smoke test against
the deterministic environment" step, but using the bundled mock environment.

Runs the full attack algorithm, prints the diverse findings it produced, and
verifies every candidate replays in a fresh environment.
"""

import sys

from agentsec import ALL_PREDICATES, AttackSearch, EnvAdapter, build_default_adapter
from mock_env.env import MockAgentEnv


def main() -> int:
    print("=" * 70)
    print("AI Agent Security -- Multi-Step Tool Attacks : local smoke test")
    print("=" * 70)

    adapter = build_default_adapter()
    candidates = AttackSearch(adapter, budget_seconds=120, log=print).run()

    print(f"\n--- {len(candidates)} diverse candidates ---")
    by_pred = {p: 0 for p in ALL_PREDICATES}
    for c in candidates:
        by_pred[c.target_predicate] += 1
        print(f"  [{c.target_predicate:18s}] {c.scenario_id:16s} "
              f"technique={c.metadata.get('technique'):16s} "
              f"obf={c.metadata.get('obfuscation')}")
    print("\nCoverage by predicate:")
    for p, n in by_pred.items():
        print(f"  {p:20s} {n}")

    # Replay verification in a brand-new environment.
    print("\nVerifying deterministic replay in a fresh environment...")
    fresh = EnvAdapter(MockAgentEnv())
    ok = 0
    for c in candidates:
        if c.target_predicate in fresh.replay(c.scenario_id, c.actions):
            ok += 1
    print(f"  {ok}/{len(candidates)} candidates replayed successfully")

    if ok != len(candidates) or not candidates:
        print("\nSMOKE TEST FAILED")
        return 1
    print("\nSMOKE TEST PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
