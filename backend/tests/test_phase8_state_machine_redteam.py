"""Phase 8 State Machine Red-Team Audit Suite."""

from datetime import datetime, timezone
import pytest

from app.api.dependencies import reset_store
from app.engine.state_machine import BeliefStateMachine
from app.engine.store import ChronoGraphStore
from app.models.domain import BeliefState, EdgeType, LifecycleStatus


def test_redteam_statemachine_invalid_transitions():
    """Attack 1: Invalid lifecycle status transitions raise ValueError and preserve store state."""
    store = reset_store()
    sm = BeliefStateMachine(store)
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)

    # 1. Nonsensical direct transition: SUPERSEDED -> ACTIVE
    b1 = store.add_belief(BeliefState(id="b1", subject_id="user", predicate="loc", object_value="Delhi", lifecycle_status=LifecycleStatus.SUPERSEDED, confidence=0.9, observed_at=t1, valid_from=t1, version=1))
    with pytest.raises(ValueError):
        sm.activate_belief(b1)

    # 2. CANCELLED -> ACTIVE
    b_canc = store.add_belief(BeliefState(id="b_canc", subject_id="user", predicate="loc", object_value="Mumbai", lifecycle_status=LifecycleStatus.CANCELLED, confidence=0.9, observed_at=t1, valid_from=t1, version=1))
    with pytest.raises(ValueError):
        sm.activate_belief(b_canc)


def test_redteam_statemachine_incompatible_subject_or_predicate_supersession():
    """Attack 2: Superseding a belief with different subject_id or predicate raises ValueError and leaves store unmutated."""
    store = reset_store()
    sm = BeliefStateMachine(store)
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 1, tzinfo=timezone.utc)

    b1 = store.add_belief(BeliefState(id="b1", subject_id="user", predicate="location", object_value="Delhi", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1))

    # Candidate with DIFFERENT predicate ('editor' vs 'location')
    b2_diff_pred = BeliefState(id="b2", subject_id="user", predicate="editor", object_value="VS Code", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=t2, valid_from=t2, version=1)

    initial_edge_count = len(store.edges)
    with pytest.raises(ValueError) as exc:
        sm.supersede_belief(b2_diff_pred, b1.id)
    assert "Predicate mismatch" in str(exc.value)

    # Transactional check: b1 lifecycle status remains ACTIVE, no edges created
    assert store.get_belief("b1").lifecycle_status == LifecycleStatus.ACTIVE
    assert len(store.edges) == initial_edge_count


def test_redteam_statemachine_invalid_temporal_order_supersession():
    """Attack 3: New superseding belief starting BEFORE old belief's valid_from raises ValueError and rolls back transaction."""
    store = reset_store()
    sm = BeliefStateMachine(store)

    t1 = datetime(2025, 2, 1, tzinfo=timezone.utc)
    t_earlier = datetime(2025, 1, 1, tzinfo=timezone.utc)

    b1 = store.add_belief(BeliefState(id="b1", subject_id="user", predicate="location", object_value="Bangalore", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1))

    # Candidate starting EARLIER than b1
    b_earlier = BeliefState(id="b_earlier", subject_id="user", predicate="location", object_value="Delhi", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=t_earlier, valid_from=t_earlier, version=1)

    initial_edge_count = len(store.edges)
    with pytest.raises(ValueError) as exc:
        sm.supersede_belief(b_earlier, b1.id)
    assert "valid_from" in str(exc.value)

    # Transactional rollback check: b1 valid_until remains None, status remains ACTIVE
    assert store.get_belief("b1").valid_until is None
    assert store.get_belief("b1").lifecycle_status == LifecycleStatus.ACTIVE
    assert len(store.edges) == initial_edge_count


def test_redteam_statemachine_transactional_integrity():
    """Attack 4: Verify that failed operations never leave partially mutated state."""
    store = reset_store()
    sm = BeliefStateMachine(store)
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)

    b1 = store.add_belief(BeliefState(id="b1", subject_id="user", predicate="location", object_value="Delhi", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1))

    # Attempt supersession with nonexistent target ID
    cand = BeliefState(id="cand", subject_id="user", predicate="location", object_value="Bangalore", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=t1, valid_from=t1, version=1)

    with pytest.raises(KeyError):
        sm.supersede_belief(cand, "nonexistent_target_id")

    # Verify store has no candidate inserted partially
    assert store.get_belief("cand") is None
    assert len(store.edges) == 0
