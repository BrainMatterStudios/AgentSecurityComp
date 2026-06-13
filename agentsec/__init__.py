"""agentsec -- a multi-step tool-attack search toolkit for the AI Agent Security
competition.

Public surface:
    AttackCandidate, AttackAction      -- replayable findings (candidate.py)
    AttackSearch                       -- the search algorithm (search.py)
    EnvAdapter, build_default_adapter  -- environment bridge (adapter.py)
"""

from .candidate import (
    ALL_PREDICATES,
    PREDICATE_DESTRUCTIVE_WRITE,
    PREDICATE_EXFILTRATION,
    PREDICATE_UNTRUSTED_TO_ACTION,
    AttackAction,
    AttackCandidate,
)
from .adapter import EnvAdapter, build_default_adapter
from .search import AttackSearch

__all__ = [
    "AttackCandidate",
    "AttackAction",
    "AttackSearch",
    "EnvAdapter",
    "build_default_adapter",
    "ALL_PREDICATES",
    "PREDICATE_EXFILTRATION",
    "PREDICATE_UNTRUSTED_TO_ACTION",
    "PREDICATE_DESTRUCTIVE_WRITE",
]
