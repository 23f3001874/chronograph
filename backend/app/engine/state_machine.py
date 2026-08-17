"""Belief state machine for managing epistemic lifecycle transitions.

Enforces valid state transitions (OBSERVED -> ACTIVE, ACTIVE -> SUPERSEDED,
PLANNED -> CANCELLED, ACTIVE -> CONFLICTED) and creates explicit relationship edges
without silently mutating unrelated beliefs.
"""

from datetime import datetime, timezone

from app.engine.store import ChronoGraphStore
from app.models.domain import (
    BeliefState,
    EdgeType,
    GraphEdge,
    LifecycleStatus,
)


class BeliefStateMachine:
    """Manages state transitions and edge creation for belief states."""

    def __init__(self, store: ChronoGraphStore) -> None:
        self.store = store

    def activate_belief(self, belief: BeliefState) -> BeliefState:
        """Activates an OBSERVED or PLANNED belief, placing it into the ACTIVE state."""
        invalid_previous_states = {LifecycleStatus.SUPERSEDED, LifecycleStatus.CANCELLED}
        if belief.lifecycle_status in invalid_previous_states:
            raise ValueError(
                f"Cannot activate belief {belief.id} from invalid terminal state '{belief.lifecycle_status}'."
            )

        belief.lifecycle_status = LifecycleStatus.ACTIVE
        self.store.add_belief(belief)
        return belief

    def supersede_belief(
        self,
        new_belief: BeliefState,
        old_belief_id: str,
        edge_id: str | None = None,
    ) -> tuple[BeliefState, BeliefState, GraphEdge]:
        """Supersedes an old belief state with a new active belief state.

        1. Sets new_belief status to ACTIVE.
        2. Sets old_belief status to SUPERSEDED.
        3. Updates old_belief.valid_until to new_belief.valid_from.
        4. Creates a SUPERSEDES edge from new_belief to old_belief.
        """
        old_belief = self.store.get_belief(old_belief_id)
        if not old_belief:
            raise KeyError(f"Target belief for supersession not found: {old_belief_id}")

        if old_belief.lifecycle_status in {LifecycleStatus.SUPERSEDED, LifecycleStatus.CANCELLED}:
            raise ValueError(
                f"Cannot supersede belief {old_belief_id} which is already '{old_belief.lifecycle_status}'."
            )

        # Update lifecycle statuses
        new_belief.lifecycle_status = LifecycleStatus.ACTIVE
        old_belief.lifecycle_status = LifecycleStatus.SUPERSEDED

        # Update temporal bounds
        if old_belief.valid_until is None or old_belief.valid_until > new_belief.valid_from:
            old_belief.valid_until = new_belief.valid_from

        # Persist updated states
        self.store.add_belief(new_belief)
        self.store.add_belief(old_belief)

        # Create SUPERSEDES relationship edge
        e_id = edge_id or f"edge_sup_{new_belief.id}_{old_belief.id}"
        created = new_belief.observed_at or datetime.now(timezone.utc)
        edge = GraphEdge(
            id=e_id,
            source_id=new_belief.id,
            target_id=old_belief.id,
            edge_type=EdgeType.SUPERSEDES,
            created_at=created,
            metadata={"transition": "SUPERSEDES"},
        )
        self.store.add_edge(edge)

        return new_belief, old_belief, edge

    def cancel_belief(
        self,
        cancellation_belief: BeliefState,
        planned_belief_id: str,
        edge_id: str | None = None,
    ) -> tuple[BeliefState, BeliefState, GraphEdge]:
        """Cancels a PLANNED or ACTIVE belief via explicit cancellation.

        1. Sets planned_belief status to CANCELLED.
        2. Updates planned_belief.valid_until to cancellation_belief.valid_from.
        3. Creates an INVALIDATES edge from cancellation_belief to planned_belief.
        """
        planned_belief = self.store.get_belief(planned_belief_id)
        if not planned_belief:
            raise KeyError(f"Target planned belief for cancellation not found: {planned_belief_id}")

        if planned_belief.lifecycle_status in {LifecycleStatus.CANCELLED, LifecycleStatus.SUPERSEDED}:
            raise ValueError(
                f"Cannot cancel belief {planned_belief_id} which is already '{planned_belief.lifecycle_status}'."
            )

        planned_belief.lifecycle_status = LifecycleStatus.CANCELLED
        if planned_belief.valid_until is None or planned_belief.valid_until > cancellation_belief.valid_from:
            planned_belief.valid_until = cancellation_belief.valid_from

        # Persist cancellation assertion and updated planned state
        self.store.add_belief(cancellation_belief)
        self.store.add_belief(planned_belief)

        e_id = edge_id or f"edge_inv_{cancellation_belief.id}_{planned_belief.id}"
        created = cancellation_belief.observed_at or datetime.now(timezone.utc)
        edge = GraphEdge(
            id=e_id,
            source_id=cancellation_belief.id,
            target_id=planned_belief.id,
            edge_type=EdgeType.INVALIDATES,
            created_at=created,
            metadata={"transition": "INVALIDATES"},
        )
        self.store.add_edge(edge)

        return cancellation_belief, planned_belief, edge

    def mark_conflicted(
        self,
        belief_1: BeliefState,
        belief_2: BeliefState,
        edge_id: str | None = None,
    ) -> tuple[BeliefState, BeliefState, GraphEdge]:
        """Marks two overlapping contradictory active beliefs as CONFLICTED.

        Creates a CONTRADICTS relationship edge between them.
        """
        belief_1.lifecycle_status = LifecycleStatus.CONFLICTED
        belief_2.lifecycle_status = LifecycleStatus.CONFLICTED

        self.store.add_belief(belief_1)
        self.store.add_belief(belief_2)

        e_id = edge_id or f"edge_con_{belief_1.id}_{belief_2.id}"
        created = belief_1.observed_at or datetime.now(timezone.utc)
        edge = GraphEdge(
            id=e_id,
            source_id=belief_1.id,
            target_id=belief_2.id,
            edge_type=EdgeType.CONTRADICTS,
            created_at=created,
            metadata={"transition": "CONTRADICTS"},
        )
        self.store.add_edge(edge)

        return belief_1, belief_2, edge
