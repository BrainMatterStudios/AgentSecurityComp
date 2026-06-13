"""Thin adapter between the search loop and the environment.

This is the ONLY file that needs editing to target the real competition SDK.
The search algorithm and strategy library are written against this small,
stable surface:

    list_scenarios() -> list[str]
    scenario_facts(scenario_id) -> ScenarioFacts          (per-scenario seeding)
    replay(scenario_id, actions) -> set[str]              (predicates that fired)

The default implementation drives the local mock environment in ``mock_env``.
To target the real SDK, implement ``replay`` by translating ``AttackAction``s
into the SDK's ``env.reset()/env.step(...)`` calls and reading the fired
predicates back from the SDK's scored trace. The translation points are marked
with ``# >>> SDK`` below.
"""

from __future__ import annotations

from typing import List, Optional, Set

from .candidate import AttackAction
from .strategies import ScenarioFacts


class EnvAdapter:
    """Adapter over the local mock environment (see ``mock_env.env``)."""

    def __init__(self, env):
        self.env = env

    def list_scenarios(self) -> List[str]:
        return self.env.list_scenarios()

    def scenario_facts(self, scenario_id: str) -> ScenarioFacts:
        """Read per-scenario facts from a fresh observation.

        The live observation tells us the names of secrets, the protected
        resources, plausible exfiltration sinks and the available tools, so the
        payloads in ``strategies.py`` can be specialised instead of generic.
        """
        obs = self.env.reset(scenario_id)
        f = ScenarioFacts()
        # >>> SDK: map fields out of the real observation here.
        f.channel = obs.get("untrusted_channel", f.channel)
        f.user_request = obs.get("user_request", f.user_request)
        f.secret_name = obs.get("secret_name", f.secret_name)
        f.secret_locator = obs.get("secret_locator", f.secret_locator)
        f.exfil_sink = obs.get("exfil_sink", f.exfil_sink)
        f.exfil_tool = obs.get("exfil_tool", f.exfil_tool)
        f.dangerous_tool = obs.get("dangerous_tool", f.dangerous_tool)
        f.dangerous_args = obs.get("dangerous_args", f.dangerous_args)
        f.protected_resource = obs.get("protected_resource", f.protected_resource)
        f.destructive_tool = obs.get("destructive_tool", f.destructive_tool)
        return f

    def replay(self, scenario_id: str, actions: List[AttackAction]) -> Set[str]:
        """Replay attacker moves in a fresh env and return fired predicate names.

        For the real SDK this becomes:
            obs = env.reset(scenario_id)                       # >>> SDK
            for a in actions:
                obs, reward, done, info = env.step(translate(a))  # >>> SDK
            return set(info["fired_predicates"])               # >>> SDK
        """
        return self.env.replay(scenario_id, actions)


def build_default_adapter(seed: int = 0) -> EnvAdapter:
    """Convenience factory used by the smoke test and unit tests."""
    from mock_env.env import MockAgentEnv

    return EnvAdapter(MockAgentEnv(seed=seed))
