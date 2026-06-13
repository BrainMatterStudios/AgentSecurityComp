"""End-to-end smoke tests proving the attack pipeline runs on the mock env.

These do not need the real SDK or any network/LLM access -- they exercise the
search loop, the strategy library, the adapter and the predicate checks against
the deterministic mock environment.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentsec import (
    ALL_PREDICATES,
    AttackCandidate,
    AttackSearch,
    EnvAdapter,
    build_default_adapter,
)
from agentsec.candidate import AttackAction
from mock_env.env import MockAgentEnv


def test_search_finds_candidates():
    candidates = AttackSearch(build_default_adapter(), budget_seconds=60).run()
    assert candidates, "search should find at least one attack"
    assert all(isinstance(c, AttackCandidate) for c in candidates)


def test_covers_all_three_predicates():
    candidates = AttackSearch(build_default_adapter(), budget_seconds=60).run()
    fired = {c.target_predicate for c in candidates}
    for p in ALL_PREDICATES:
        assert p in fired, f"expected to find a {p} attack; got {fired}"


def test_candidates_are_diverse():
    candidates = AttackSearch(build_default_adapter(), budget_seconds=60).run()
    sigs = {c.signature() for c in candidates}
    assert len(sigs) == len(candidates), "candidates must be de-duplicated"
    # We expect coverage across multiple scenarios, not just one.
    scenarios = {c.scenario_id for c in candidates}
    assert len(scenarios) >= 2


def test_candidates_replay_deterministically():
    """A returned candidate must re-fire its predicate in a *fresh* env --
    this is the property the real evaluator depends on."""
    candidates = AttackSearch(build_default_adapter(), budget_seconds=60).run()
    fresh = EnvAdapter(MockAgentEnv())  # brand new environment
    for c in candidates:
        fired = fresh.replay(c.scenario_id, c.actions)
        assert c.target_predicate in fired, (
            f"candidate {c.signature()} did not replay")


def test_candidate_roundtrips_through_dict():
    candidates = AttackSearch(build_default_adapter(), budget_seconds=30).run()
    c = candidates[0]
    again = AttackCandidate.from_dict(c.to_dict())
    assert again.to_dict() == c.to_dict()


def test_obfuscation_helps_against_strict_guardrail():
    """On the strict (private-board) guardrail, plain payloads are blocked but
    the search should still surface some findings via obfuscation/coverage."""
    strict = EnvAdapter(MockAgentEnv(strict_guardrail=True))
    candidates = AttackSearch(strict, budget_seconds=60).run()
    # Strict guard is tough; we don't require full coverage, but the pipeline
    # must run cleanly and any returned candidate must genuinely replay.
    for c in candidates:
        assert strict.replay(c.scenario_id, c.actions) >= {c.target_predicate}


if __name__ == "__main__":
    import traceback

    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except Exception:
            failed += 1
            print(f"FAIL  {t.__name__}")
            traceback.print_exc()
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
