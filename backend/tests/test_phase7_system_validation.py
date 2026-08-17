"""Phase 7 System Validation and Adversarial Integration Test Suite for ChronoGraph."""

from datetime import datetime, timezone
import os
import shutil
import tempfile
import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import reset_store
from app.engine.contradiction import detect_conflicts
from app.engine.persistence import SnapshotManager
from app.engine.state_machine import BeliefStateMachine
from app.engine.store import ChronoGraphStore
from app.engine.temporal_resolver import (
    get_evidence_for_belief,
    get_lineage,
    resolve_at_time,
    resolve_current,
)
from app.main import app
from app.models.domain import (
    BeliefState,
    LifecycleStatus,
    Observation,
    ResolutionStatus,
)


@pytest.fixture
def tmp_dir():
    dir_path = tempfile.mkdtemp(prefix="chronograph_phase7_test_")
    yield dir_path
    shutil.rmtree(dir_path, ignore_errors=True)


def test_val_1_true_contradiction_returns_conflicted():
    """Adversarial Test 1: Overlapping active beliefs return CONFLICTED without picking a winner."""
    store = reset_store()
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 1, tzinfo=timezone.utc)
    t3 = datetime(2025, 3, 1, tzinfo=timezone.utc)
    t4 = datetime(2025, 4, 1, tzinfo=timezone.utc)

    # Overlapping active locations (Delhi Jan 1-Mar 1 vs Bangalore Feb 1-Apr 1)
    store.add_belief(BeliefState(id="b1", subject_id="user", predicate="lives_in", object_value="Delhi", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, valid_until=t3, version=1))
    store.add_belief(BeliefState(id="b2", subject_id="user", predicate="lives_in", object_value="Bangalore", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t2, valid_from=t2, valid_until=t4, version=1))

    # Detect conflicts updates overlapping active states to CONFLICTED
    conflicts = detect_conflicts(store, "user", "lives_in")
    assert len(conflicts) == 1

    res_curr = resolve_current(store, "user", "lives_in", datetime(2025, 2, 15, tzinfo=timezone.utc))
    assert res_curr.status == ResolutionStatus.CONFLICTED
    assert res_curr.confidence == 0.5
    assert "Conflicting simultaneous active beliefs" in res_curr.reason or "Contradictory" in res_curr.reason


def test_val_2_supersession_lineage_stack():
    """Adversarial Test 2: Supersession maintains lineage stack B1 -> B2 -> B3."""
    store = reset_store()
    sm = BeliefStateMachine(store)

    t1 = datetime(2025, 1, 10, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 10, tzinfo=timezone.utc)
    t3 = datetime(2025, 3, 10, tzinfo=timezone.utc)

    b1 = store.add_belief(BeliefState(id="b1", subject_id="user", predicate="editor", object_value="VS Code", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1))
    b2 = BeliefState(id="b2", subject_id="user", predicate="editor", object_value="Cursor", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=t2, valid_from=t2, version=1)
    sm.supersede_belief(b2, b1.id)

    b3 = BeliefState(id="b3", subject_id="user", predicate="editor", object_value="VS Code", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.95, observed_at=t3, valid_from=t3, version=2)
    sm.supersede_belief(b3, b2.id)

    lineage = get_lineage(store, "b3")
    assert lineage["root_belief_id"] == "b3"
    assert len(lineage["history"]) == 3
    assert lineage["history"][0]["belief"].id == "b3"
    assert lineage["history"][1]["belief"].id == "b2"
    assert lineage["history"][2]["belief"].id == "b1"


def test_val_3_cancellation_of_planned_belief():
    """Adversarial Test 3: Explicit cancellation sets status to CANCELLED."""
    store = reset_store()
    sm = BeliefStateMachine(store)
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)

    b = store.add_belief(BeliefState(id="b_plan", subject_id="user", predicate="trip", object_value="Tokyo", lifecycle_status=LifecycleStatus.PLANNED, confidence=0.8, observed_at=t1, valid_from=t1, version=1))
    cancel_assertion = BeliefState(id="b_cancel", subject_id="user", predicate="trip", object_value="Cancelled", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=t1, valid_from=t1, version=1)
    c_b, p_b, edge = sm.cancel_belief(cancel_assertion, b.id)
    assert p_b.lifecycle_status == LifecycleStatus.CANCELLED


def test_val_4_same_value_reassertion_no_conflict():
    """Adversarial Test 4: Re-asserting the same value does not produce conflict."""
    store = reset_store()
    sm = BeliefStateMachine(store)
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 1, tzinfo=timezone.utc)

    b1 = store.add_belief(BeliefState(id="b1", subject_id="user", predicate="editor", object_value="VS Code", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1))
    b2 = BeliefState(id="b2", subject_id="user", predicate="editor", object_value="VS Code", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.95, observed_at=t2, valid_from=t2, version=1)

    new_b = sm.activate_belief(b2)
    assert new_b.lifecycle_status == LifecycleStatus.ACTIVE

    res = resolve_current(store, "user", "editor", datetime(2025, 2, 15, tzinfo=timezone.utc))
    assert res.status == ResolutionStatus.SUPPORTED
    assert res.beliefs[0].object_value == "VS Code"


def test_val_5_unknown_abstention():
    """Adversarial Test 5: Querying an unrecorded attribute returns UNKNOWN, 0.0 confidence, and empty beliefs list."""
    store = reset_store()
    res = resolve_current(store, "user", "favorite_language", datetime(2025, 3, 20, tzinfo=timezone.utc))
    assert res.status == ResolutionStatus.UNKNOWN
    assert len(res.beliefs) == 0
    assert res.confidence == 0.0


def test_val_6_temporal_boundary_conditions():
    """Adversarial Test 6: Boundary evaluation at exact valid_from and valid_until."""
    store = reset_store()
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 1, tzinfo=timezone.utc)

    store.add_belief(BeliefState(id="b1", subject_id="user", predicate="status", object_value="active_user", lifecycle_status=LifecycleStatus.SUPERSEDED, confidence=0.9, observed_at=t1, valid_from=t1, valid_until=t2, version=1))

    # At exact valid_from t1 -> valid
    assert len(resolve_at_time(store, "user", "status", t1)) == 1

    # At exact valid_until t2 -> superseded / invalid
    assert len(resolve_at_time(store, "user", "status", t2)) == 0


def test_val_7_malformed_input_returns_422():
    """Adversarial Test 7: Malformed request payload returns HTTP 422 Unprocessable Entity."""
    client = TestClient(app)
    res = client.post("/api/v1/query", json={"invalid_field": 123})
    assert res.status_code == 422


def test_val_8_duplicate_ingestion_idempotency():
    """Adversarial Test 8: Duplicate memory ingestion does not duplicate belief state index."""
    reset_store()
    client = TestClient(app)

    req = {"collection": "test", "session_id": "s1", "text": "I use VS Code as my favorite editor."}
    res1 = client.post("/api/v1/ingest", json=req)
    res2 = client.post("/api/v1/ingest", json=req)

    assert res1.status_code == 200
    assert res2.status_code == 200

    q = client.post("/api/v1/query", json={"subject_id": "user", "predicate": "favorite_editor"})
    assert q.json()["status"] == "SUPPORTED"
    assert q.json()["value"] == "VS Code"


def test_val_9_persistence_recovery(tmp_dir):
    """Adversarial Test 9: Complete persistence snapshot recovery roundtrip."""
    snap_file = os.path.join(tmp_dir, "val_snap.json")
    mgr = SnapshotManager(snapshot_path=snap_file)
    store = ChronoGraphStore()
    t1 = datetime(2025, 1, 10, tzinfo=timezone.utc)

    store.add_belief(BeliefState(id="b1", subject_id="user", predicate="location", object_value="Delhi", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1))
    mgr.save_snapshot(store, snap_file)

    restored = ChronoGraphStore()
    mgr.load_snapshot(restored, snap_file)
    assert restored.get_belief("b1").object_value == "Delhi"


def test_val_10_nonexistent_belief_404():
    """Adversarial Test 10: Nonexistent belief ID returns HTTP 404 Not Found."""
    client = TestClient(app)
    res = client.get("/api/v1/beliefs/nonexistent_id_12345")
    assert res.status_code == 404
