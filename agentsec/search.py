"""The attack *search* algorithm.

Given a (Gym-style) environment and a wall-clock budget, this explores the
hypothesis space defined in ``strategies.py`` and returns a diverse set of
replayable ``AttackCandidate`` objects that fired a security predicate.

Design goals (the scoring rewards *severity* AND *diversity*):

  * Coverage-first ordering. We iterate predicates x scenarios x techniques x
    obfuscations, but we *stop refining* a (scenario, predicate, technique) cell
    once it has a confirmed hit -- spending the budget broadening coverage rather
    than piling up near-duplicate findings of the same lever.

  * Cheap-before-expensive. Plain payloads are tried before heavy obfuscation;
    obfuscation is only escalated for cells that did not fire plainly (i.e. when
    a guardrail is plausibly blocking us), which is exactly where it pays off.

  * Budget-aware. Every probe checks the remaining budget; the loop degrades
    gracefully, always returning whatever it has confirmed so far.

  * Adaptive seeding. Scenario *facts* (secret names, sinks, protected
    resources, available tools) are read from the live observation so payloads
    are specialised per scenario instead of being static strings.

The loop is deliberately model-agnostic: it talks to the environment through the
adapter, so the same code drives the local mock and the real SDK targets
(GPT-OSS / Gemma) without change.
"""

from __future__ import annotations

import time
from typing import Callable, Dict, List, Optional

from .adapter import EnvAdapter
from .candidate import (
    ALL_PREDICATES,
    AttackAction,
    AttackCandidate,
)
from .strategies import (
    OBFUSCATIONS,
    ScenarioFacts,
    Technique,
    techniques_for,
)


# Order obfuscations from cheapest / most likely, to heaviest. The search only
# walks deeper into this list for cells that didn't already fire.
_OBFUSCATION_ORDER = ["plain", "tool_result_spoof", "base64", "split",
                      "homoglyph", "zero_width"]


class AttackSearch:
    def __init__(
        self,
        env: EnvAdapter,
        budget_seconds: float = 9000.0,
        log: Optional[Callable[[str], None]] = None,
    ):
        self.env = env
        self.budget_seconds = budget_seconds
        self._t0 = time.monotonic()
        self._log = log or (lambda m: None)
        # Confirmed candidates, de-duplicated by coarse signature for diversity.
        self._found: Dict[str, AttackCandidate] = {}
        # Cells (scenario, predicate, technique) already satisfied -> skip refine.
        self._satisfied: set[str] = set()
        self.probes = 0

    # -- budget helpers ---------------------------------------------------- #
    def _elapsed(self) -> float:
        return time.monotonic() - self._t0

    def _remaining(self) -> float:
        return self.budget_seconds - self._elapsed()

    def _out_of_budget(self, reserve: float = 5.0) -> bool:
        return self._remaining() <= reserve

    # -- candidate construction ------------------------------------------- #
    def _build_actions(
        self, facts: ScenarioFacts, technique: Technique, obfuscation: str
    ) -> List[AttackAction]:
        """Render a technique into concrete, replayable attacker moves."""
        payload = technique.render(facts)
        payload = OBFUSCATIONS[obfuscation](payload)
        actions: List[AttackAction] = [
            AttackAction(kind="set_user_request", content=facts.user_request),
            AttackAction(kind="inject", channel=facts.channel, content=payload,
                         meta={"technique": technique.name, "obfuscation": obfuscation}),
        ]
        # Multi-step techniques need extra agent turns to take the follow-up
        # (laundering publish, staged-plan execution, ...).
        for _ in range(max(1, technique.steps)):
            actions.append(AttackAction(kind="advance"))
        return actions

    def _probe(
        self, scenario_id: str, facts: ScenarioFacts,
        technique: Technique, obfuscation: str,
    ) -> Optional[AttackCandidate]:
        """Run one candidate in the env; return it if its target predicate fired."""
        self.probes += 1
        actions = self._build_actions(facts, technique, obfuscation)
        fired = self.env.replay(scenario_id, actions)  # -> set of fired predicates
        if technique.predicate in fired:
            cand = AttackCandidate(
                scenario_id=scenario_id,
                actions=actions,
                target_predicate=technique.predicate,
                metadata={
                    "technique": technique.name,
                    "obfuscation": obfuscation,
                    "steps": technique.steps,
                    "also_fired": sorted(fired - {technique.predicate}),
                    "notes": technique.notes,
                },
            )
            return cand
        return None

    # -- main loop --------------------------------------------------------- #
    def run(self) -> List[AttackCandidate]:
        scenarios = self.env.list_scenarios()
        self._log(f"[search] {len(scenarios)} scenarios, "
                  f"budget={self.budget_seconds:.0f}s")

        # Pass 1 -- broad coverage with cheap (plain / spoof) payloads first.
        for obf in _OBFUSCATION_ORDER:
            if self._out_of_budget():
                break
            for scenario_id in scenarios:
                if self._out_of_budget():
                    break
                facts = self.env.scenario_facts(scenario_id)
                for predicate in ALL_PREDICATES:
                    for technique in techniques_for(predicate):
                        cell = f"{scenario_id}::{predicate}::{technique.name}"
                        if cell in self._satisfied:
                            continue  # already covered -- broaden, don't refine
                        if self._out_of_budget():
                            break
                        cand = self._probe(scenario_id, facts, technique, obf)
                        if cand is not None:
                            self._satisfied.add(cell)
                            sig = cand.signature()
                            if sig not in self._found:
                                self._found[sig] = cand
                                self._log(
                                    f"[hit] {predicate} | {scenario_id} | "
                                    f"{technique.name} | {obf} "
                                    f"(probe {self.probes}, t={self._elapsed():.1f}s)"
                                )
            # After the first (plain) sweep, only deeper obfuscation passes remain;
            # they exist to crack guardrail-blocked cells, so keep looping.

        self._log(f"[search] done: {len(self._found)} diverse candidates, "
                  f"{self.probes} probes, t={self._elapsed():.1f}s")
        return list(self._found.values())
