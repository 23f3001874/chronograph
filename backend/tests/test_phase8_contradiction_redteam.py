"""Phase 8 Contradiction Engine Red-Team Audit Suite."""

from datetime import datetime, timezone
import pytest

from app.api.dependencies import reset_store
from app.engine.contradiction import detect_conflicts
from app.engine.state_machine import BeliefStateMachine
from app.engine.store import ChronoGraphStore
from app.engine.temporal_resolver import resolve_current
from app.models.domain import BeliefState, LifecycleStatus, ResolutionStatus


def test_redteam_contradiction_1_different_predicates_never_conflict():
    """14: Beliefs with different predicates (editor vs language) must NEVER conflict."""
    store = reset_store()
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)

    store.add_belief(BeliefState(id="b_ed", subject_id="user", predicate="favorite_editor", object_value="VS Code", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1))
    store.add_belief(BeliefState(id="b_lang", subject_id="user", predicate="favorite_language", object_value="Python", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1))

    conflicts_ed = detect_conflicts(store, "user", "favorite_editor")
    conflicts_lang = detect_conflicts(store, "user", "favorite_language")

    assert len(conflicts_ed) == 0
    assert len(conflicts_lang) == 0

    res_ed = resolve_current(store, "user", "favorite_editor", datetime(2025, 1, 15, tzinfo=timezone.utc))
    res_lang = resolve_current(store, "user", "favorite_language", datetime(2025, 1, 15, tzinfo=timezone.utc))

    assert res_ed.status == ResolutionStatus.SUPPORTED
    assert res_lang.status == ResolutionStatus.SUPPORTED


def test_redteam_contradiction_2_three_way_contradiction():
    """13: Three-way active contradiction (Delhi vs Bangalore vs Mumbai) returns CONFLICTED without picking a winner."""
    store = reset_store()
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)

    store.add_belief(BeliefState(id="b1", subject_id="user", predicate="city", object_value="Delhi", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1))
    store.add_belief(BeliefState(id="b2", subject_id="user", predicate="city", object_value="Bangalore", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1))
    store.add_belief(BeliefState(id="b3", subject_id="user", predicate="city", object_value="Mumbai", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1))

    conflicts = detect_conflicts(store, "user", "city")
    assert len(conflicts) >= 1

    res = resolve_current(store, "user", "city", datetime(2025, 1, 15, tzinfo=timezone.utc))
    assert res.status == ResolutionStatus.CONFLICTED
    assert res.confidence == 0.5
    assert len(res.beliefs) == 3


def test_redteam_contradiction_3_adjacent_intervals_no_conflict():
    """6: Adjacent intervals (Jan 1-Feb 1 vs Feb 1-Mar 1) do NOT conflict at Feb 1 (half-open interval [valid_from, valid_until))."""
    store = reset_store()
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 1, tzinfo=timezone.utc)
    t3 = datetime(2025, 3, 1, tzinfo=timezone.utc)

    store.add_belief(BeliefState(id="b1", subject_id="user", predicate="loc", object_value="Delhi", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, valid_until=t2, version=1))
    store.add_belief(BeliefState(id="b2", subject_id="user", predicate="loc", object_value="Bangalore", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t2, valid_from=t2, valid_until=t3, version=1))

    conflicts = detect_conflicts(store, "user", "loc")
    assert len(conflicts) == 0

    res = resolve_current(store, "user", "loc", t2)
    assert res.status == ResolutionStatus.SUPPORTED
    assert res.beliefs[0].object_value == "Bangalore"


def test_redteam_contradiction_4_nested_intervals_conflict():
    """7 & 8: A nested interval (Feb 1-Feb 15) inside a wider interval (Jan 1-Mar 1) produces CONFLICTED if both are ACTIVE."""
    store = reset_store()
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 1, tzinfo=timezone.utc)
    t3 = datetime(2025, 2, 15, tzinfo=timezone.utc)
    t4 = datetime(2025, 3, 1, tzinfo=timezone.utc)

    store.add_belief(BeliefState(id="b_wide", subject_id="user", predicate="loc", object_value="Delhi", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, valid_until=t4, version=1))
    store.add_belief(BeliefState(id="b_nested", subject_id="user", predicate="loc", object_value="Bangalore", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t2, valid_from=t2, valid_until=t3, version=1))

    conflicts = detect_conflicts(store, "user", "loc")
    assert len(conflicts) == 1

    res = resolve_current(store, "user", "loc", datetime(2025, 2, 10, tzinfo=timezone.utc))
    assert res.status == ResolutionStatus.CONFLICTED
