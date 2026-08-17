"""Tests for BeliefStateMachine transitions and edge creation."""

from datetime import datetime, timezone
import pytest

from app.engine.state_machine import BeliefStateMachine
from app.engine.store import ChronoGraphStore
from app.models.domain import (
    BeliefState,
    EdgeType,
    LifecycleStatus,
    Observation,
)


@pytest.fixture
def store_and_sm():
    store = ChronoGraphStore()
    sm = BeliefStateMachine(store)
    return store, sm


def test_activate_belief(store_and_sm):
    store, sm = store_and_sm
    t = datetime(2025, 1, 1, tzinfo=timezone.utc)
    b = BeliefState(
        id="b1",
        subject_id="user",
        predicate="lives_in",
        object_value="Delhi",
        lifecycle_status=LifecycleStatus.OBSERVED,
        confidence=0.9,
        observed_at=t,
        valid_from=t,
        version=1,
    )
    activated = sm.activate_belief(b)
    assert activated.lifecycle_status == LifecycleStatus.ACTIVE
    assert store.get_belief("b1") == activated


def test_supersede_belief(store_and_sm):
    """Scenario A: Simple supersession (VS Code -> Cursor)."""
    store, sm = store_and_sm
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 1, tzinfo=timezone.utc)

    b1 = BeliefState(
        id="b1_vscode",
        subject_id="user",
        predicate="favorite_editor",
        object_value="VS Code",
        lifecycle_status=LifecycleStatus.ACTIVE,
        confidence=0.9,
        observed_at=t1,
        valid_from=t1,
        valid_until=None,
        version=1,
    )
    store.add_belief(b1)

    b2 = BeliefState(
        id="b2_cursor",
        subject_id="user",
        predicate="favorite_editor",
        object_value="Cursor",
        lifecycle_status=LifecycleStatus.OBSERVED,
        confidence=0.95,
        observed_at=t2,
        valid_from=t2,
        valid_until=None,
        version=1,
    )

    new_b, old_b, edge = sm.supersede_belief(b2, b1.id)

    assert new_b.lifecycle_status == LifecycleStatus.ACTIVE
    assert old_b.lifecycle_status == LifecycleStatus.SUPERSEDED
    assert old_b.valid_until == t2
    assert edge.edge_type == EdgeType.SUPERSEDES
    assert edge.source_id == b2.id
    assert edge.target_id == b1.id


def test_cancel_planned_belief(store_and_sm):
    """Scenario E: Planned cancellation."""
    store, sm = store_and_sm
    t2 = datetime(2025, 6, 1, tzinfo=timezone.utc)
    t3 = datetime(2025, 7, 1, tzinfo=timezone.utc)

    planned = BeliefState(
        id="b_planned",
        subject_id="user",
        predicate="planned_move",
        object_value="Bangalore",
        lifecycle_status=LifecycleStatus.PLANNED,
        confidence=0.85,
        observed_at=t2,
        valid_from=t2,
        version=1,
    )
    store.add_belief(planned)

    cancel_obs = BeliefState(
        id="b_cancel",
        subject_id="user",
        predicate="move_cancellation",
        object_value="Bangalore",
        lifecycle_status=LifecycleStatus.OBSERVED,
        confidence=0.95,
        observed_at=t3,
        valid_from=t3,
        version=1,
    )

    c_belief, p_belief, edge = sm.cancel_belief(cancel_obs, planned.id)

    assert p_belief.lifecycle_status == LifecycleStatus.CANCELLED
    assert p_belief.valid_until == t3
    assert edge.edge_type == EdgeType.INVALIDATES
    assert edge.source_id == c_belief.id
    assert edge.target_id == p_belief.id


def test_nonsensical_transitions_raise_error(store_and_sm):
    store, sm = store_and_sm
    t = datetime(2025, 1, 1, tzinfo=timezone.utc)
    b_superseded = BeliefState(
        id="b_sup",
        subject_id="user",
        predicate="lives_in",
        object_value="Delhi",
        lifecycle_status=LifecycleStatus.SUPERSEDED,
        confidence=0.9,
        observed_at=t,
        valid_from=t,
        version=1,
    )
    
    with pytest.raises(ValueError) as exc:
        sm.activate_belief(b_superseded)
    assert "invalid terminal state" in str(exc.value)
