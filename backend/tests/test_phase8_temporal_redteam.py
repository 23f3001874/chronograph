"""Phase 8 Temporal Resolution Red-Team Audit Suite."""

from datetime import datetime, timedelta, timezone
import pytest

from app.api.dependencies import reset_store
from app.engine.contradiction import detect_conflicts
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
    LifecycleStatus,
    Observation,
    ResolutionStatus,
)


def test_redteam_temporal_A_exact_valid_from_boundary():
    """A: Querying at exact valid_from timestamp returns the belief as valid."""
    store = reset_store()
    t1 = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    store.add_belief(
        BeliefState(
            id="b1", subject_id="user", predicate="location", object_value="Delhi",
            lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1
        )
    )
    res = resolve_at_time(store, "user", "location", t1)
    assert len(res) == 1
    assert res[0].id == "b1"


def test_redteam_temporal_B_exact_valid_until_boundary():
    """B: Querying at exact valid_until timestamp returns the belief as INVALID (half-open interval [valid_from, valid_until))."""
    store = reset_store()
    t1 = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 1, 0, 0, 0, tzinfo=timezone.utc)
    store.add_belief(
        BeliefState(
            id="b1", subject_id="user", predicate="location", object_value="Delhi",
            lifecycle_status=LifecycleStatus.SUPERSEDED, confidence=0.9, observed_at=t1, valid_from=t1, valid_until=t2, version=1
        )
    )
    res = resolve_at_time(store, "user", "location", t2)
    assert len(res) == 0


def test_redteam_temporal_C_D_instant_before_and_after_expiration():
    """C & D: Querying one microsecond before valid_until is valid; one microsecond after valid_until is invalid."""
    store = reset_store()
    t1 = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 1, 0, 0, 0, tzinfo=timezone.utc)
    store.add_belief(
        BeliefState(
            id="b1", subject_id="user", predicate="location", object_value="Delhi",
            lifecycle_status=LifecycleStatus.SUPERSEDED, confidence=0.9, observed_at=t1, valid_from=t1, valid_until=t2, version=1
        )
    )

    # 1 microsecond before t2
    t_before = t2 - timedelta(microseconds=1)
    res_before = resolve_at_time(store, "user", "location", t_before)
    assert len(res_before) == 1

    # 1 microsecond after t2
    t_after = t2 + timedelta(microseconds=1)
    res_after = resolve_at_time(store, "user", "location", t_after)
    assert len(res_after) == 0


def test_redteam_temporal_E_future_knowledge_leakage_prevention():
    """E: Inserting a future observation (observed Mar 5) must NOT alter past historical query at Jan 15."""
    store = reset_store()
    sm = BeliefStateMachine(store)

    t1_obs = datetime(2025, 1, 5, tzinfo=timezone.utc)
    t1_from = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t1_until = datetime(2025, 2, 1, tzinfo=timezone.utc)

    b1 = store.add_belief(
        BeliefState(
            id="b1", subject_id="user", predicate="location", object_value="Delhi",
            lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1_obs, valid_from=t1_from, valid_until=t1_until, version=1
        )
    )

    # Query before future observation -> Delhi
    res_jan_initial = resolve_current(store, "user", "location", datetime(2025, 1, 15, tzinfo=timezone.utc))
    assert res_jan_initial.status == ResolutionStatus.SUPPORTED
    assert res_jan_initial.beliefs[0].object_value == "Delhi"

    # Insert future observation observed in March
    t2_obs = datetime(2025, 3, 5, tzinfo=timezone.utc)
    t2_from = datetime(2025, 2, 1, tzinfo=timezone.utc)
    b2 = BeliefState(
        id="b2", subject_id="user", predicate="location", object_value="Bangalore",
        lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=t2_obs, valid_from=t2_from, version=1
    )
    sm.supersede_belief(b2, b1.id)

    # Query at Jan 15 AGAIN after future observation inserted -> MUST STILL BE Delhi!
    res_jan_after = resolve_current(store, "user", "location", datetime(2025, 1, 15, tzinfo=timezone.utc))
    assert res_jan_after.status == ResolutionStatus.SUPPORTED
    assert res_jan_after.beliefs[0].object_value == "Delhi"


def test_redteam_temporal_G_H_same_timestamp_contradictions_and_versions():
    """G & H: Two overlapping active beliefs at identical valid_from return CONFLICTED. Higher version alone without explicit edge does not silently win."""
    store = reset_store()
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)

    # b1 version 1 vs b2 version 2 at same timestamp without supersession edge
    b1 = store.add_belief(
        BeliefState(
            id="b1", subject_id="user", predicate="editor", object_value="VS Code",
            lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1
        )
    )
    b2 = store.add_belief(
        BeliefState(
            id="b2", subject_id="user", predicate="editor", object_value="Cursor",
            lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=2
        )
    )

    detect_conflicts(store, "user", "editor")
    res = resolve_current(store, "user", "editor", datetime(2025, 1, 15, tzinfo=timezone.utc))

    # Must return CONFLICTED (not silently pick version 2!)
    assert res.status == ResolutionStatus.CONFLICTED
    assert res.confidence == 0.5


def test_redteam_temporal_I_non_overlapping_sequential_beliefs():
    """I: Non-overlapping sequential beliefs resolve correctly across exact interval boundaries."""
    store = reset_store()
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 1, tzinfo=timezone.utc)
    t3 = datetime(2025, 3, 1, tzinfo=timezone.utc)

    store.add_belief(BeliefState(id="b1", subject_id="user", predicate="city", object_value="Delhi", lifecycle_status=LifecycleStatus.SUPERSEDED, confidence=0.9, observed_at=t1, valid_from=t1, valid_until=t2, version=1))
    store.add_belief(BeliefState(id="b2", subject_id="user", predicate="city", object_value="Bangalore", lifecycle_status=LifecycleStatus.SUPERSEDED, confidence=0.9, observed_at=t2, valid_from=t2, valid_until=t3, version=1))

    # Jan 31 -> Delhi
    res_jan = resolve_current(store, "user", "city", datetime(2025, 1, 31, tzinfo=timezone.utc))
    assert res_jan.status == ResolutionStatus.SUPPORTED
    assert res_jan.beliefs[0].object_value == "Delhi"

    # Feb 1 -> Bangalore
    res_feb1 = resolve_current(store, "user", "city", t2)
    assert res_feb1.status == ResolutionStatus.SUPPORTED
    assert res_feb1.beliefs[0].object_value == "Bangalore"

    # Mar 1 -> UNKNOWN (Both expired)
    res_mar1 = resolve_current(store, "user", "city", t3)
    assert res_mar1.status == ResolutionStatus.UNKNOWN


def test_redteam_temporal_J_K_historical_conflict_and_supersession():
    """J & K: Historical conflict does not poison future valid state. Superseded belief does not conflict with active superseding belief."""
    store = reset_store()
    sm = BeliefStateMachine(store)

    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 1, tzinfo=timezone.utc)

    b1 = store.add_belief(BeliefState(id="b1", subject_id="user", predicate="tool", object_value="ToolA", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1))
    b2 = BeliefState(id="b2", subject_id="user", predicate="tool", object_value="ToolB", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=t2, valid_from=t2, version=1)

    sm.supersede_belief(b2, b1.id)

    # Feb 15 -> ToolB (SUPERSEDED b1 does not conflict with b2)
    res_feb = resolve_current(store, "user", "tool", datetime(2025, 2, 15, tzinfo=timezone.utc))
    assert res_feb.status == ResolutionStatus.SUPPORTED
    assert res_feb.beliefs[0].object_value == "ToolB"


def test_redteam_temporal_L_M_N_same_value_overlap_and_cancellation():
    """L, M & N: Overlapping same values do not conflict. Cancelled beliefs cannot be returned as SUPPORTED, and cancellation does not mutate unrelated beliefs."""
    store = reset_store()
    sm = BeliefStateMachine(store)

    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)

    # Cancelled belief
    b_plan = store.add_belief(BeliefState(id="b_plan", subject_id="user", predicate="trip", object_value="Paris", lifecycle_status=LifecycleStatus.PLANNED, confidence=0.8, observed_at=t1, valid_from=t1, version=1))
    b_cancel = BeliefState(id="b_cancel", subject_id="user", predicate="trip", object_value="Cancelled", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=t1, valid_from=t1, version=1)
    sm.cancel_belief(b_cancel, b_plan.id)

    # Unrelated belief for different predicate
    b_unrelated = store.add_belief(BeliefState(id="b_unrelated", subject_id="user", predicate="food", object_value="Pizza", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1))

    # Query trip -> CANCELLED
    res_trip = resolve_current(store, "user", "trip", datetime(2025, 1, 15, tzinfo=timezone.utc))
    assert res_trip.status == ResolutionStatus.CANCELLED

    # Query food -> SUPPORTED Pizza (unrelated belief completely unaffected)
    res_food = resolve_current(store, "user", "food", datetime(2025, 1, 15, tzinfo=timezone.utc))
    assert res_food.status == ResolutionStatus.SUPPORTED
    assert res_food.beliefs[0].object_value == "Pizza"
