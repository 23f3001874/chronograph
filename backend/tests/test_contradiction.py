"""Tests for contradiction and conflict detection in ChronoGraph."""

from datetime import datetime, timezone
import pytest

from app.engine.contradiction import detect_conflicts
from app.engine.store import ChronoGraphStore
from app.models.domain import (
    BeliefState,
    EdgeType,
    LifecycleStatus,
)


@pytest.fixture
def store():
    return ChronoGraphStore()


def test_scenario_c_true_contradiction(store):
    """Scenario C: Overlapping active beliefs for same subject+predicate with different values."""
    t_jan1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t_feb1 = datetime(2025, 2, 1, tzinfo=timezone.utc)
    t_mar1 = datetime(2025, 3, 1, tzinfo=timezone.utc)
    t_apr1 = datetime(2025, 4, 1, tzinfo=timezone.utc)

    b1 = store.add_belief(
        BeliefState(
            id="b1_delhi",
            subject_id="user",
            predicate="location",
            object_value="Delhi",
            lifecycle_status=LifecycleStatus.ACTIVE,
            confidence=0.9,
            observed_at=t_jan1,
            valid_from=t_jan1,
            valid_until=t_mar1,
            version=1,
        )
    )

    b2 = store.add_belief(
        BeliefState(
            id="b2_bangalore",
            subject_id="user",
            predicate="location",
            object_value="Bangalore",
            lifecycle_status=LifecycleStatus.ACTIVE,
            confidence=0.9,
            observed_at=t_feb1,
            valid_from=t_feb1,
            valid_until=t_apr1,
            version=1,
        )
    )

    conflicts = detect_conflicts(store, "user", "location")
    assert len(conflicts) == 1

    b1_upd = store.get_belief("b1_delhi")
    b2_upd = store.get_belief("b2_bangalore")

    assert b1_upd.lifecycle_status == LifecycleStatus.CONFLICTED
    assert b2_upd.lifecycle_status == LifecycleStatus.CONFLICTED

    edges = store.get_edges_for_belief("b1_delhi")
    assert len(edges) == 1
    assert edges[0].edge_type == EdgeType.CONTRADICTS


def test_scenario_g_same_value_reassertion_no_conflict(store):
    """Scenario G: Same-value reassertion across consecutive intervals is NOT a contradiction."""
    t_jan1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t_feb1 = datetime(2025, 2, 1, tzinfo=timezone.utc)
    t_mar1 = datetime(2025, 3, 1, tzinfo=timezone.utc)

    b1 = store.add_belief(
        BeliefState(
            id="b1_vscode",
            subject_id="user",
            predicate="favorite_editor",
            object_value="VS Code",
            lifecycle_status=LifecycleStatus.ACTIVE,
            confidence=0.9,
            observed_at=t_jan1,
            valid_from=t_jan1,
            valid_until=t_feb1,
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
            confidence=0.9,
            observed_at=t_feb1,
            valid_from=t_feb1,
            valid_until=t_mar1,
            version=2,
        )
    )

    conflicts = detect_conflicts(store, "user", "favorite_editor")
    assert len(conflicts) == 0
    assert store.get_belief("b1_vscode").lifecycle_status == LifecycleStatus.ACTIVE
    assert store.get_belief("b2_vscode").lifecycle_status == LifecycleStatus.ACTIVE


def test_sequential_location_changes_no_conflict(store):
    """Sequential non-overlapping location changes are NOT contradictory."""
    t_jan1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t_feb1 = datetime(2025, 2, 1, tzinfo=timezone.utc)
    t_mar1 = datetime(2025, 3, 1, tzinfo=timezone.utc)

    store.add_belief(
        BeliefState(
            id="b1",
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
    store.add_belief(
        BeliefState(
            id="b2",
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

    conflicts = detect_conflicts(store, "user", "lives_in")
    assert len(conflicts) == 0
