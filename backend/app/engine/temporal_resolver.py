"""Temporal state resolver and lineage tracking engine for ChronoGraph.

Executes point-in-time state queries (T), current state resolution, conflict checking,
and evidence/lineage traversal while avoiding graph cycle deadlocks.
"""

from datetime import datetime
from typing import Any

from app.engine.abstention import check_abstention
from app.engine.contradiction import detect_conflicts
from app.engine.store import ChronoGraphStore
from app.models.domain import (
    BeliefState,
    EdgeType,
    LifecycleStatus,
    Observation,
    ResolutionResult,
    ResolutionStatus,
)


def resolve_at_time(
    store: ChronoGraphStore,
    subject_id: str,
    predicate: str,
    timestamp: datetime,
) -> list[BeliefState]:
    """Resolves all belief states valid at exact timestamp T.

    Temporal Validity Rule:
        valid_from <= T AND (valid_until is None OR T < valid_until)
    
    Excludes CANCELLED beliefs. Results are sorted deterministically by
    observed_at descending, then version descending.
    """
    all_beliefs = store.get_beliefs(subject_id, predicate)
    
    valid_beliefs: list[BeliefState] = []
    for b in all_beliefs:
        if b.lifecycle_status in {LifecycleStatus.CANCELLED, LifecycleStatus.OBSERVED}:
            continue

        is_started = b.valid_from <= timestamp
        is_not_ended = (b.valid_until is None) or (timestamp < b.valid_until)

        if is_started and is_not_ended:
            valid_beliefs.append(b)

    # Sort deterministically by observed_at desc, version desc
    valid_beliefs.sort(key=lambda b: (b.observed_at, b.version), reverse=True)
    return valid_beliefs


def get_evidence_for_belief(
    store: ChronoGraphStore,
    belief_id: str,
) -> list[Observation]:
    """Retrieves grounded Observations for a BeliefState in deterministic order."""
    belief = store.get_belief(belief_id)
    if not belief:
        return []

    evidence_set: set[str] = set(belief.observation_ids)

    # Also check explicit GROUNDED_IN edges in store
    edges = store.get_edges_for_belief(belief_id)
    for edge in edges:
        if edge.edge_type == EdgeType.GROUNDED_IN and edge.source_id == belief_id:
            evidence_set.add(edge.target_id)

    observations: list[Observation] = []
    for obs_id in evidence_set:
        obs = store.get_observation(obs_id)
        if obs:
            observations.append(obs)

    # Sort deterministically by observed_at asc, then id asc
    observations.sort(key=lambda o: (o.observed_at, o.id))
    return observations


def resolve_current(
    store: ChronoGraphStore,
    subject_id: str,
    predicate: str,
    now: datetime,
) -> ResolutionResult:
    """Resolves current state for (subject_id, predicate) at timestamp `now`.

    Checks abstention, temporal validity, planned/cancelled states, and active conflicts.
    """
    # 1. Abstention check
    ab_result = check_abstention(store, subject_id, predicate, now)
    if ab_result is not None:
        return ab_result

    # 2. Check for conflicts among active/conflicted beliefs
    detect_conflicts(store, subject_id, predicate)

    # 3. Resolve temporally valid beliefs at timestamp `now`
    valid_beliefs = resolve_at_time(store, subject_id, predicate, now)

    if not valid_beliefs:
        # Check if stored beliefs were cancelled or superseded
        all_beliefs = store.get_beliefs(subject_id, predicate)
        if all_beliefs and any(b.lifecycle_status == LifecycleStatus.CANCELLED for b in all_beliefs):
            ev_ids: list[str] = []
            for b in all_beliefs:
                ev_ids.extend(b.observation_ids)
            return ResolutionResult(
                status=ResolutionStatus.CANCELLED,
                beliefs=all_beliefs,
                confidence=0.0,
                reason=f"All recorded beliefs for '{subject_id}' predicate '{predicate}' have been CANCELLED.",
                evidence_ids=sorted(list(set(ev_ids))),
            )

        return ResolutionResult(
            status=ResolutionStatus.UNKNOWN,
            beliefs=[],
            confidence=0.0,
            reason=f"No active belief valid at timestamp {now.isoformat()} for predicate '{predicate}'.",
            evidence_ids=[],
        )

    # 4. Check if any valid belief is CONFLICTED or multiple valid beliefs disagree on object_value
    has_conflicted_status = any(b.lifecycle_status == LifecycleStatus.CONFLICTED for b in valid_beliefs)
    unique_values = set(b.object_value or b.object_id for b in valid_beliefs)
    
    if has_conflicted_status or len(unique_values) > 1:
        ev_ids = []
        for b in valid_beliefs:
            ev_ids.extend(b.observation_ids)
        return ResolutionResult(
            status=ResolutionStatus.CONFLICTED,
            beliefs=valid_beliefs,
            confidence=0.5,
            reason=f"Conflicting simultaneous active beliefs detected for '{predicate}'.",
            evidence_ids=sorted(list(set(ev_ids))),
        )

    # 5. Supported single/consistent active belief state
    active_belief = valid_beliefs[0]
    ev_obs = get_evidence_for_belief(store, active_belief.id)
    ev_ids = [o.id for o in ev_obs]

    return ResolutionResult(
        status=ResolutionStatus.SUPPORTED,
        beliefs=[active_belief],
        confidence=active_belief.confidence,
        reason=f"Active belief supported for '{subject_id}' predicate '{predicate}' value '{active_belief.object_value}'.",
        evidence_ids=ev_ids,
    )


def get_lineage(
    store: ChronoGraphStore,
    belief_id: str,
) -> dict[str, Any]:
    """Traverses belief state transitions (SUPERSEDES, INVALIDATES, GROUNDED_IN)
    
    Prevents infinite cycles by maintaining a visited set of belief IDs.
    """
    root_belief = store.get_belief(belief_id)
    if not root_belief:
        return {"root_belief_id": belief_id, "history": []}

    history: list[dict[str, Any]] = []
    visited: set[str] = set()

    queue: list[tuple[BeliefState, str]] = [(root_belief, "ROOT")]

    while queue:
        current_belief, rel_type = queue.pop(0)
        if current_belief.id in visited:
            continue
        visited.add(current_belief.id)

        evidence = get_evidence_for_belief(store, current_belief.id)
        history.append({
            "belief": current_belief,
            "relationship": rel_type,
            "observations": evidence,
        })

        # Find outgoing/incoming SUPERSEDES or INVALIDATES edges
        edges = store.get_edges_for_belief(current_belief.id)
        for edge in edges:
            if edge.edge_type == EdgeType.SUPERSEDES:
                # If current_belief is source, target is superseded (older)
                if edge.source_id == current_belief.id and edge.target_id not in visited:
                    target_b = store.get_belief(edge.target_id)
                    if target_b:
                        queue.append((target_b, "SUPERSEDES"))
                # If current_belief is target, source is superseding (newer)
                elif edge.target_id == current_belief.id and edge.source_id not in visited:
                    source_b = store.get_belief(edge.source_id)
                    if source_b:
                        queue.append((source_b, "SUPERSEDED_BY"))

            elif edge.edge_type == EdgeType.INVALIDATES:
                if edge.source_id == current_belief.id and edge.target_id not in visited:
                    target_b = store.get_belief(edge.target_id)
                    if target_b:
                        queue.append((target_b, "INVALIDATES"))
                elif edge.target_id == current_belief.id and edge.source_id not in visited:
                    source_b = store.get_belief(edge.source_id)
                    if source_b:
                        queue.append((source_b, "INVALIDATED_BY"))

    return {
        "root_belief_id": belief_id,
        "history": history,
    }
