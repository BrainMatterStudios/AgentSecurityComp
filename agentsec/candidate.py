"""Core data structures shared by the attack algorithm, the search loop and the
mock environment.

These mirror the *documented* shape of the competition SDK (an attacker submits
replayable ``AttackCandidate`` objects that the evaluator re-runs in a fresh,
deterministic environment and scores against security predicates). The concrete
field names are kept deliberately small and explicit so that mapping onto the
real SDK is a thin, mechanical change -- see ``agentsec/adapter.py``.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


# The three security-predicate families the competition scores against.
PREDICATE_EXFILTRATION = "exfiltration"
PREDICATE_UNTRUSTED_TO_ACTION = "untrusted_to_action"
PREDICATE_DESTRUCTIVE_WRITE = "destructive_write"

ALL_PREDICATES = (
    PREDICATE_EXFILTRATION,
    PREDICATE_UNTRUSTED_TO_ACTION,
    PREDICATE_DESTRUCTIVE_WRITE,
)


@dataclass
class AttackAction:
    """A single replayable attacker *move*.

    The attacker does not impersonate the agent. Instead it (a) seeds untrusted
    channels the agent will later read (``inject``) and (b) advances the agent so
    it processes that content and decides which tools to call (``advance``).

    Keeping moves declarative (channel + content, no live handles) is what makes
    a candidate deterministically replayable in a fresh environment.
    """

    kind: str                      # "inject" | "advance" | "set_user_request"
    channel: Optional[str] = None  # e.g. "email", "web", "file", "calendar"
    content: Optional[str] = None  # payload text for an injection / user request
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "AttackAction":
        return cls(
            kind=d["kind"],
            channel=d.get("channel"),
            content=d.get("content"),
            meta=d.get("meta", {}) or {},
        )


@dataclass
class AttackCandidate:
    """A replayable attack the evaluator can verify.

    A candidate is *self-contained*: given ``scenario_id`` and ``actions`` the
    evaluator can rebuild the exact environment state, replay the moves and
    recompute the trace, then test which security predicates fired.
    """

    scenario_id: str
    actions: List[AttackAction]
    target_predicate: str
    # Free-form, ignored by the evaluator but invaluable for analysis / writeup:
    # which technique class produced this, what obfuscation was applied, etc.
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "actions": [a.to_dict() for a in self.actions],
            "target_predicate": self.target_predicate,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "AttackCandidate":
        return cls(
            scenario_id=d["scenario_id"],
            actions=[AttackAction.from_dict(a) for a in d["actions"]],
            target_predicate=d["target_predicate"],
            metadata=d.get("metadata", {}) or {},
        )

    def signature(self) -> str:
        """Coarse identity used for diversity de-duplication.

        Scoring rewards *diverse* violations, so we treat two candidates as
        "the same finding" when they hit the same predicate in the same scenario
        using the same technique class. We deliberately do NOT include the exact
        payload text, so trivial wording changes don't inflate diversity.
        """
        technique = self.metadata.get("technique", "unknown")
        return f"{self.scenario_id}::{self.target_predicate}::{technique}"
