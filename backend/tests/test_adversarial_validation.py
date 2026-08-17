"""Adversarial validation suite for ChronoGraph Phase 2.

Verifies that:
1. Newer observations/versions NEVER silently win over overlapping active contradictions.
2. Sequential non-overlapping beliefs resolve cleanly.
3. Same-value overlaps are not flagged as conflicts.
4. Superseded beliefs do not trigger false conflicts.
5. Cancellations do not cause unrelated attribute conflicts.
"""

from datetime import datetime, timezone
import pytest

from app.engine.state_machine import BeliefStateMachine
from app.engine.store import ChronoGraphStore
from app.engine.temporal_resolver import (
    resolve_at_time,
    resolve_current,
)
from app.models.domain import (
    BeliefState,
    EdgeType,
    LifecycleStatus,
    Observation,
    ResolutionStatus,
)


@pytest.fixture
def store_and_sm():
    store = ChronoGraphStore()
    sm = BeliefStateMachine(store)
    return store, sm


def test_adversarial_1_newer_observation_does_not_silently_win(store_and_sm):
    """TEST 1: Newer observation / version MUST NOT silently override an overlapping active belief.

    B1: Delhi valid Jan 1 - Mar 1 (observed Jan 10, v1, ACTIVE)
    B2: Bangalore valid Feb 1 - Apr 1 (observed Feb 10, v2, ACTIVE)
    Query at Feb 15: Must return CONFLICTED, not silently pick Bangalore.
    """
    store, sm = store_and_sm

    t_jan1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t_jan10 = datetime(2025, 1, 10, tzinfo=timezone.utc)
    t_feb1 = datetime(2025, 2, 1, tzinfo=timezone.utc)
    t_feb10 = datetime(2025, 2, 10, tzinfo=timezone.utc)
    t_feb15 = datetime(2025, 2, 15, tzinfo=timezone.utc)
    t_mar1 = datetime(2025, 3, 1, tzinfo=timezone.utc)
    t_apr1 = datetime(2025, 4, 1, tzinfo=timezone.utc)

    # B1: Delhi (v1, observed Jan 10)
    b1 = store.add_belief(
        BeliefState(
            id="b1_delhi",
            subject_id="user",
            predicate="lives_in",
            object_value="Delhi",
            lifecycle_status=LifecycleStatus.ACTIVE,
            confidence=0.9,
            observed_at=t_jan10,
            valid_from=t_jan1,
            valid_until=t_mar1,
            version=1,
        )
    )

    # B2: Bangalore (v2, observed Feb 10 - newer observation & higher version, but overlapping!)
    b2 = store.add_belief(
        BeliefState(
            id="b2_bangalore",
            subject_id="user",
            predicate="lives_in",
            object_value="Bangalore",
            lifecycle_status=LifecycleStatus.ACTIVE,
            confidence=0.95,
            observed_at=t_feb10,
            valid_from=t_feb1,
            valid_until=t_apr1,
            version=2,
        )
    )

    # Query at Feb 15 (during overlap window)
    res = resolve_current(store, "user", "lives_in", t_feb15)

    # Must NOT silently select Bangalore
    assert res.status == ResolutionStatus.CONFLICTED
    assert len(res.beliefs) == 2
    assert set(b.id for b in res.beliefs) == {"b1_delhi", "b2_bangalore"}
    assert store.get_belief("b1_delhi").lifecycle_status == LifecycleStatus.CONFLICTED
    assert store.get_belief("b2_bangalore").lifecycle_status == LifecycleStatus.CONFLICTED

    # Verify CONTRADICTS edge was created
    edges = store.get_edges_for_belief("b1_delhi")
    assert any(e.edge_type == EdgeType.CONTRADICTS for e in edges)


def test_adversarial_2_sequential_beliefs_resolve_normally(store_and_sm):
    """TEST 2: Sequential non-overlapping beliefs resolve normally.

    B1: Delhi Jan 1 -> Feb 1
    B2: Bangalore Feb 1 -> Mar 1
    Query Feb 15 -> SUPPORTED Bangalore
    Query Jan 15 -> SUPPORTED Delhi
    Query Mar 1 -> UNKNOWN
    """
    store, sm = store_and_sm

    t_jan1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t_jan15 = datetime(2025, 1, 15, tzinfo=timezone.utc)
    t_feb1 = datetime(2025, 2, 1, tzinfo=timezone.utc)
    t_feb15 = datetime(2025, 2, 15, tzinfo=timezone.utc)
    t_mar1 = datetime(2025, 3, 1, tzinfo=timezone.utc)

    b1 = store.add_belief(
        BeliefState(
            id="b1_delhi",
            subject_id="user",
            predicate="lives_in",
            object_value="Delhi",
            lifecycle_status=LifecycleStatus.SUPERSEDED,
            confidence=0.9,
            observed_at=t_jan1,
            valid_from=t_jan1,
            valid_until=t_feb1,
            version=1,
        )
    )
    b2 = store.add_belief(
        BeliefState(
            id="b2_bangalore",
            subject_id="user",
            predicate="lives_in",
            object_value="Bangalore",
            lifecycle_status=LifecycleStatus.ACTIVE,
            confidence=0.9,
            observed_at=t_feb1,
            valid_from=t_feb1,
            valid_until=t_mar1,
            version=1,
        )
    )

    # 1. Query Feb 15 -> SUPPORTED Bangalore
    res_feb15 = resolve_current(store, "user", "lives_in", t_feb15)
    assert res_feb15.status == ResolutionStatus.SUPPORTED
    assert res_feb15.beliefs[0].object_value == "Bangalore"

    # 2. Query Jan 15 -> SUPPORTED Delhi
    res_jan15 = resolve_current(store, "user", "lives_in", t_jan15)
    assert res_jan15.status == ResolutionStatus.SUPPORTED
    assert res_jan15.beliefs[0].object_value == "Delhi"

    # 3. Query Mar 1 -> UNKNOWN
    res_mar1 = resolve_current(store, "user", "lives_in", t_mar1)
    assert res_mar1.status == ResolutionStatus.UNKNOWN


def test_adversarial_3_same_value_overlap_is_not_contradiction(store_and_sm):
    """TEST 3: Same-value overlapping intervals do NOT trigger a contradiction.

    B1: VS Code Jan -> Mar
    B2: VS Code Feb -> Apr
    Expected: NOT CONFLICTED.
    """
    store, sm = store_and_sm

    t_jan = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t_feb = datetime(2025, 2, 1, tzinfo=timezone.utc)
    t_mar = datetime(2025, 3, 1, tzinfo=timezone.utc)
    t_apr = datetime(2025, 4, 1, tzinfo=timezone.utc)

    b1 = store.add_belief(
        BeliefState(
            id="b1_vscode",
            subject_id="user",
            predicate="favorite_editor",
            object_value="VS Code",
            lifecycle_status=LifecycleStatus.ACTIVE,
            confidence=0.9,
            observed_at=t_jan,
            valid_from=t_jan,
            valid_until=t_mar,
            version=1,
        )
    )
    b2 = store.add_belief(
        BeliefState(
            id="b2_vscode",
            subject_id="user",
            predicate="favorite_editor",
            object_value="VS Code",
            lifecycle_status=LifecycleStatus.ACTIVE,
            confidence=0.95,
            observed_at=t_feb,
            valid_from=t_feb,
            valid_until=t_apr,
            version=2,
        )
    )

    res = resolve_current(store, "user", "favorite_editor", datetime(2025, 2, 15, tzinfo=timezone.utc))

    assert res.status == ResolutionStatus.SUPPORTED
    assert store.get_belief("b1_vscode").lifecycle_status == LifecycleStatus.ACTIVE
    assert store.get_belief("b2_vscode").lifecycle_status == LifecycleStatus.ACTIVE


def test_adversarial_4_supersession_resolves_correctly(store_and_sm):
    """TEST 4: Supersession resolves cleanly without false conflicts.

    B1: VS Code Jan -> Feb (SUPERSEDED)
    B2: Cursor Feb -> present (ACTIVE)
    Query after Feb -> SUPPORTED Cursor. Presence of B1 does NOT cause conflict.
    """
    store, sm = store_and_sm

    t_jan = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t_feb = datetime(2025, 2, 1, tzinfo=timezone.utc)
    t_mar = datetime(2025, 3, 1, tzinfo=timezone.utc)

    b1 = BeliefState(
        id="b1_vscode",
        subject_id="user",
        predicate="favorite_editor",
        object_value="VS Code",
        lifecycle_status=LifecycleStatus.ACTIVE,
        confidence=0.9,
        observed_at=t_jan,
        valid_from=t_jan,
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
        observed_at=t_feb,
        valid_from=t_feb,
        valid_until=None,
        version=1,
    )
    sm.supersede_belief(b2, b1.id)

    res = resolve_current(store, "user", "favorite_editor", t_mar)

    assert res.status == ResolutionStatus.SUPPORTED
    assert len(res.beliefs) == 1
    assert res.beliefs[0].object_value == "Cursor"


def test_adversarial_5_cancellation_does_not_create_unrelated_conflicts(store_and_sm):
    """TEST 5: Cancellation invalidates planned belief without creating unrelated attribute conflicts.

    B_plan: planned_move = Bangalore (PLANNED)
    B_cancel: move_cancellation = Bangalore (OBSERVED -> INVALIDATES B_plan)
    Unrelated: lives_in = Delhi (ACTIVE)
    Verify: B_plan becomes CANCELLED, lives_in = Delhi remains ACTIVE and unaffected.
    """
    store, sm = store_and_sm

    t_may = datetime(2025, 5, 1, tzinfo=timezone.utc)
    t_jun = datetime(2025, 6, 1, tzinfo=timezone.utc)
    t_jul = datetime(2025, 7, 1, tzinfo=timezone.utc)

    # Active location belief
    b_delhi = store.add_belief(
        BeliefState(
            id="b_delhi",
            subject_id="user",
            predicate="lives_in",
            object_value="Delhi",
            lifecycle_status=LifecycleStatus.ACTIVE,
            confidence=0.9,
            observed_at=t_may,
            valid_from=t_may,
            valid_until=None,
            version=1,
        )
    )

    # Planned move
    b_plan = store.add_belief(
        BeliefState(
            id="b_plan",
            subject_id="user",
            predicate="planned_move",
            object_value="Bangalore",
            lifecycle_status=LifecycleStatus.PLANNED,
            confidence=0.85,
            observed_at=t_jun,
            valid_from=t_jun,
            valid_until=None,
            version=1,
        )
    )

    # Cancellation
    b_cancel = BeliefState(
        id="b_cancel",
        subject_id="user",
        predicate="move_cancellation",
        object_value="Bangalore",
        lifecycle_status=LifecycleStatus.OBSERVED,
        confidence=0.95,
        observed_at=t_jul,
        valid_from=t_jul,
        valid_until=None,
        version=1,
    )
    sm.cancel_belief(b_cancel, b_plan.id)

    # 1. Planned move is now CANCELLED
    assert store.get_belief("b_plan").lifecycle_status == LifecycleStatus.CANCELLED

    # 2. Query lives_in at July -> STILL SUPPORTED Delhi
    res_loc = resolve_current(store, "user", "lives_in", t_jul)
    assert res_loc.status == ResolutionStatus.SUPPORTED
    assert res_loc.beliefs[0].object_value == "Delhi"

    # 3. Query planned_move at July -> CANCELLED
    res_plan = resolve_current(store, "user", "planned_move", t_jul)
    assert res_plan.status == ResolutionStatus.CANCELLED
