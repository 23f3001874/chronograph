"""Contradiction and conflict detection engine for ChronoGraph.

Identifies overlapping, un-superseded active beliefs with different values for the
same subject-predicate pair and marks them CONFLICTED.
"""

from app.engine.state_machine import BeliefStateMachine
from app.engine.store import ChronoGraphStore
from app.models.domain import (
    BeliefState,
    EdgeType,
    GraphEdge,
    LifecycleStatus,
)


def _validity_overlaps(b1: BeliefState, b2: BeliefState) -> bool:
    """Checks if the temporal validity intervals of two belief states overlap."""
    b1_end = b1.valid_until
    b2_end = b2.valid_until

    cond1 = b2_end is None or b1.valid_from < b2_end
    cond2 = b1_end is None or b2.valid_from < b1_end

    return cond1 and cond2


def _has_supersedes_or_invalidates_link(store: ChronoGraphStore, b1_id: str, b2_id: str) -> bool:
    """Checks if a SUPERSEDES or INVALIDATES edge exists between two beliefs."""
    edges_b1 = store.get_edges_for_belief(b1_id)
    for edge in edges_b1:
        if edge.edge_type in {EdgeType.SUPERSEDES, EdgeType.INVALIDATES}:
            if (edge.source_id == b1_id and edge.target_id == b2_id) or (
                edge.source_id == b2_id and edge.target_id == b1_id
            ):
                return True
    return False


def detect_conflicts(
    store: ChronoGraphStore,
    subject_id: str,
    predicate: str,
) -> list[tuple[BeliefState, BeliefState, GraphEdge]]:
    """Detects overlapping contradictory active beliefs for a subject-predicate pair.

    Returns a list of tuples containing (belief_1, belief_2, contradiction_edge).
    """
    beliefs = store.get_beliefs(subject_id, predicate)
    
    # Filter candidate beliefs (must be ACTIVE or already CONFLICTED)
    candidates = [
        b
        for b in beliefs
        if b.lifecycle_status in {LifecycleStatus.ACTIVE, LifecycleStatus.CONFLICTED}
    ]

    conflicts: list[tuple[BeliefState, BeliefState, GraphEdge]] = []
    state_machine = BeliefStateMachine(store)

    for i in range(len(candidates)):
        for j in range(i + 1, len(candidates)):
            b1 = candidates[i]
            b2 = candidates[j]

            # 1. Must have different values (same value is a reassertion, not a contradiction)
            same_object_id = b1.object_id and b1.object_id == b2.object_id
            same_object_val = b1.object_value and b1.object_value == b2.object_value
            if same_object_id or same_object_val:
                continue

            # 2. Must have overlapping validity intervals
            if not _validity_overlaps(b1, b2):
                continue

            # 3. Neither must supersede or invalidate the other
            if _has_supersedes_or_invalidates_link(store, b1.id, b2.id):
                continue

            # Mark conflicted and record conflict tuple
            b1, b2, edge = state_machine.mark_conflicted(b1, b2)
            conflicts.append((b1, b2, edge))

    return conflicts
