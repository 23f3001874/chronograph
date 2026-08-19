"""Phase 8 Epistemic Abstention Engine Red-Team Audit Suite."""

from datetime import datetime, timezone
import pytest

from app.api.dependencies import reset_store
from app.engine.store import ChronoGraphStore
from app.engine.temporal_resolver import resolve_current
from app.models.domain import BeliefState, LifecycleStatus, ResolutionStatus


def test_redteam_abstention_unknown_subject_and_predicate():
    """Attack 1: Unknown subject and/or predicate returns UNKNOWN status, 0.0 confidence, and empty beliefs list."""
    store = reset_store()
    now = datetime(2025, 3, 20, tzinfo=timezone.utc)

    # 1. Unknown subject
    res1 = resolve_current(store, "nonexistent_user", "favorite_editor", now)
    assert res1.status == ResolutionStatus.UNKNOWN
    assert res1.confidence == 0.0
    assert len(res1.beliefs) == 0

    # 2. Unknown predicate for existing user
    store.add_belief(BeliefState(id="b1", subject_id="user", predicate="location", object_value="Delhi", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=now, valid_from=now, version=1))
    res2 = resolve_current(store, "user", "unknown_predicate", now)
    assert res2.status == ResolutionStatus.UNKNOWN
    assert res2.confidence == 0.0


def test_redteam_abstention_only_future_or_superseded_beliefs():
    """Attack 2: Only future-valid or superseded beliefs present returns UNKNOWN status."""
    store = reset_store()
    t_past = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t_mid = datetime(2025, 2, 1, tzinfo=timezone.utc)
    t_future = datetime(2025, 4, 1, tzinfo=timezone.utc)
    now = datetime(2025, 3, 1, tzinfo=timezone.utc)

    # 1. Only SUPERSEDED belief valid in Jan
    store.add_belief(BeliefState(id="b_past", subject_id="user", predicate="role", object_value="Intern", lifecycle_status=LifecycleStatus.SUPERSEDED, confidence=0.9, observed_at=t_past, valid_from=t_past, valid_until=t_mid, version=1))
    res_sup = resolve_current(store, "user", "role", now)
    assert res_sup.status == ResolutionStatus.UNKNOWN

    # 2. Only FUTURE-VALID belief valid in April
    store.add_belief(BeliefState(id="b_fut", subject_id="user", predicate="role", object_value="Manager", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t_future, valid_from=t_future, version=1))
    res_fut = resolve_current(store, "user", "role", now)
    assert res_fut.status == ResolutionStatus.UNKNOWN


def test_redteam_abstention_conflicted_never_becomes_unknown():
    """Attack 3: CONFLICTED state is NEVER converted into UNKNOWN or SUPPORTED."""
    store = reset_store()
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    now = datetime(2025, 1, 15, tzinfo=timezone.utc)

    store.add_belief(BeliefState(id="b1", subject_id="user", predicate="city", object_value="Delhi", lifecycle_status=LifecycleStatus.CONFLICTED, confidence=0.5, observed_at=t1, valid_from=t1, version=1))
    store.add_belief(BeliefState(id="b2", subject_id="user", predicate="city", object_value="Bangalore", lifecycle_status=LifecycleStatus.CONFLICTED, confidence=0.5, observed_at=t1, valid_from=t1, version=1))

    res = resolve_current(store, "user", "city", now)
    assert res.status == ResolutionStatus.CONFLICTED
    assert res.status != ResolutionStatus.UNKNOWN
    assert res.status != ResolutionStatus.SUPPORTED
