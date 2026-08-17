"""Abstention engine for ChronoGraph.

Provides deterministic checking for absent facts, returning explicit UNKNOWN
resolution status when no grounded belief or evidence exists.
"""

from datetime import datetime

from app.engine.store import ChronoGraphStore
from app.models.domain import ResolutionResult, ResolutionStatus


def check_abstention(
    store: ChronoGraphStore,
    subject_id: str,
    predicate: str,
    timestamp: datetime,
) -> ResolutionResult | None:
    """Checks whether the system must abstain due to absence of belief or evidence.

    Returns a ResolutionResult with status UNKNOWN if no beliefs exist for the
    subject and predicate, or None if candidate beliefs are present.
    """
    beliefs = store.get_beliefs(subject_id, predicate)
    
    if not beliefs:
        return ResolutionResult(
            status=ResolutionStatus.UNKNOWN,
            beliefs=[],
            confidence=0.0,
            reason=(
                f"No recorded evidence or belief states exist for subject '{subject_id}' "
                f"and predicate '{predicate}' at timestamp {timestamp.isoformat()}."
            ),
            evidence_ids=[],
        )

    return None
