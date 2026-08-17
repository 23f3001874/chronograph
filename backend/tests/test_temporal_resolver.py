"""Tests for temporal resolver, point-in-time state queries, evidence lineage, and temporal boundaries."""

from datetime import datetime, timezone
import pytest

from app.engine.state_machine import BeliefStateMachine
from app.engine.store import ChronoGraphStore
from app.engine.temporal_resolver import (
    get_evidence_for_belief,
    get_lineage,
    resolve_at_time,
    resolve_current,
)
from app.models.domain import (
    BeliefState,
    EdgeType,
    GraphEdge,
    LifecycleStatus,
    Observation,
    ResolutionStatus,
)


@pytest.fixture
def store():
    return ChronoGraphStore()


def test_scenario_d_sequential_location_changes(store):
    """Scenario D: Sequential location changes and point-in-time queries."""
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

    # 1. At Jan 15 -> Delhi
    res_jan15 = resolve_at_time(store, "user", "lives_in", t_jan15)
    assert len(res_jan15) == 1
    assert res_jan15[0].object_value == "Delhi"

    # 2. At Feb 15 -> Bangalore
    res_feb15 = resolve_at_time(store, "user", "lives_in", t_feb15)
    assert len(res_feb15) == 1
    assert res_feb15[0].object_value == "Bangalore"

    # 3. At Mar 1 -> Empty (b2 valid_until is Mar 1 non-inclusive)
    res_mar1 = resolve_at_time(store, "user", "lives_in", t_mar1)
    assert len(res_mar1) == 0

    # 4. Current resolution at Mar 1 -> UNKNOWN
    cur_mar1 = resolve_current(store, "user", "lives_in", t_mar1)
    assert cur_mar1.status == ResolutionStatus.UNKNOWN


def test_temporal_boundary_conditions(store):
    """Section 10: Explicit tests for T == valid_from, T == valid_until, T before/after valid_until."""
    t_start = datetime(2025, 2, 1, 0, 0, 0, tzinfo=timezone.utc)
    t_end = datetime(2025, 3, 1, 0, 0, 0, tzinfo=timezone.utc)

    t_just_before = datetime(2025, 2, 28, 23, 59, 59, tzinfo=timezone.utc)
    t_just_after = datetime(2025, 3, 1, 0, 0, 1, tzinfo=timezone.utc)

    b = store.add_belief(
        BeliefState(
            id="b_boundary",
            subject_id="user",
            predicate="lives_in",
            object_value="Delhi",
            lifecycle_status=LifecycleStatus.ACTIVE,
            confidence=0.9,
            observed_at=t_start,
            valid_from=t_start,
            valid_until=t_end,
            version=1,
        )
    )

    # 1. T == valid_from -> VALID
    res_start = resolve_at_time(store, "user", "lives_in", t_start)
    assert len(res_start) == 1

    # 2. T just before valid_until -> VALID
    res_before = resolve_at_time(store, "user", "lives_in", t_just_before)
    assert len(res_before) == 1

    # 3. T == valid_until -> NOT VALID (non-inclusive valid_until)
    res_end = resolve_at_time(store, "user", "lives_in", t_end)
    assert len(res_end) == 0

    # 4. T just after valid_until -> NOT VALID
    res_after = resolve_at_time(store, "user", "lives_in", t_just_after)
    assert len(res_after) == 0


def test_scenario_b_flapping_editor_lineage(store):
    """Scenario B: VS Code -> Cursor -> VS Code flapping lineage & cycle safety."""
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 1, tzinfo=timezone.utc)
    t3 = datetime(2025, 3, 1, tzinfo=timezone.utc)

    sm = BeliefStateMachine(store)

    obs1 = store.add_observation(Observation(id="o1", source_text="VS Code", session_id="s1", observed_at=t1))
    obs2 = store.add_observation(Observation(id="o2", source_text="Cursor", session_id="s2", observed_at=t2))
    obs3 = store.add_observation(Observation(id="o3", source_text="VS Code again", session_id="s3", observed_at=t3))

    b1 = BeliefState(
        id="b1", subject_id="user", predicate="favorite_editor", object_value="VS Code",
        lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1, observation_ids=[obs1.id]
    )
    sm.activate_belief(b1)

    b2 = BeliefState(
        id="b2", subject_id="user", predicate="favorite_editor", object_value="Cursor",
        lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=t2, valid_from=t2, version=1, observation_ids=[obs2.id]
    )
    sm.supersede_belief(b2, b1.id)

    b3 = BeliefState(
        id="b3", subject_id="user", predicate="favorite_editor", object_value="VS Code",
        lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.95, observed_at=t3, valid_from=t3, version=2, observation_ids=[obs3.id]
    )
    sm.supersede_belief(b3, b2.id)

    # Lineage check
    lineage = get_lineage(store, b3.id)
    assert lineage["root_belief_id"] == "b3"
    history = lineage["history"]
    assert len(history) == 3

    history_b_ids = [item["belief"].id for item in history]
    assert history_b_ids == ["b3", "b2", "b1"]


def test_evidence_for_belief(store):
    t = datetime(2025, 1, 1, tzinfo=timezone.utc)
    obs = store.add_observation(Observation(id="o100", source_text="Evidence text", session_id="s1", observed_at=t))
    b = store.add_belief(
        BeliefState(
            id="b_ev", subject_id="u", predicate="p", object_value="v",
            lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t, valid_from=t, version=1, observation_ids=[obs.id]
        )
    )
    evidence = get_evidence_for_belief(store, b.id)
    assert len(evidence) == 1
    assert evidence[0].id == "o100"
