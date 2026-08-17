"""Comprehensive tests for ChronoGraph persistence, atomic snapshots, recovery, and concurrency protection."""

from datetime import datetime, timezone
import json
import os
import shutil
import tempfile
import threading
import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_store, reset_store, restore_from_snapshot, save_current_snapshot
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
    EdgeType,
    Entity,
    GraphEdge,
    LifecycleStatus,
    Observation,
    ResolutionStatus,
)


@pytest.fixture
def tmp_dir():
    dir_path = tempfile.mkdtemp(prefix="chronograph_test_data_")
    yield dir_path
    shutil.rmtree(dir_path, ignore_errors=True)


def test_snapshot_serialization_deserialization(tmp_dir):
    """Test 1 & 2: Complete graph round-trip serialization and deserialization."""
    store = ChronoGraphStore()
    t1 = datetime(2025, 1, 10, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 10, tzinfo=timezone.utc)

    user = store.add_entity(Entity(id="user", name="Alex", entity_type="PERSON"))
    obs = store.add_observation(Observation(id="o1", source_text="I use VS Code.", session_id="s1", observed_at=t1, hydradb_chunk_id="chunk1"))
    b1 = store.add_belief(BeliefState(id="b1", subject_id="user", predicate="favorite_editor", object_value="VS Code", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1, observation_ids=[obs.id]))
    edge = store.add_edge(GraphEdge(id="e1", source_id=b1.id, target_id=obs.id, edge_type=EdgeType.GROUNDED_IN, created_at=t1))

    snap_file = os.path.join(tmp_dir, "snapshot.json")
    mgr = SnapshotManager(snapshot_path=snap_file)

    mgr.save_snapshot(store, snap_file)
    assert os.path.exists(snap_file)

    # Restore into new store
    new_store = ChronoGraphStore()
    mgr.load_snapshot(new_store, snap_file)

    assert new_store.get_entity("user").name == "Alex"
    assert new_store.get_observation("o1").source_text == "I use VS Code."
    assert new_store.get_belief("b1").object_value == "VS Code"
    assert new_store.get_belief("b1").lifecycle_status == LifecycleStatus.ACTIVE
    assert len(new_store.get_edges_for_belief("b1")) == 1


def test_index_reconstruction(tmp_dir):
    """Test 3: Verification of subject_predicate_index reconstruction."""
    store = ChronoGraphStore()
    t1 = datetime(2025, 1, 10, tzinfo=timezone.utc)
    store.add_belief(BeliefState(id="b1", subject_id="user", predicate="location", object_value="Delhi", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1))

    snap_file = os.path.join(tmp_dir, "snapshot_index.json")
    mgr = SnapshotManager(snapshot_path=snap_file)
    mgr.save_snapshot(store, snap_file)

    new_store = ChronoGraphStore()
    mgr.load_snapshot(new_store, snap_file)

    indexed = new_store.get_beliefs("user", "location")
    assert len(indexed) == 1
    assert indexed[0].id == "b1"


def test_temporal_resolution_lineage_and_evidence_after_restore(tmp_dir):
    """Test 4, 5 & 6: Temporal resolution, lineage, and evidence produce identical results after restore."""
    store = ChronoGraphStore()
    sm = BeliefStateMachine(store)

    t1 = datetime(2025, 1, 10, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 10, tzinfo=timezone.utc)

    obs1 = store.add_observation(Observation(id="o1", source_text="VS Code statement", session_id="s1", observed_at=t1))
    obs2 = store.add_observation(Observation(id="o2", source_text="Cursor statement", session_id="s2", observed_at=t2))

    b1 = store.add_belief(BeliefState(id="b1", subject_id="user", predicate="favorite_editor", object_value="VS Code", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1, observation_ids=[obs1.id]))
    b2 = BeliefState(id="b2", subject_id="user", predicate="favorite_editor", object_value="Cursor", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.95, observed_at=t2, valid_from=t2, version=1, observation_ids=[obs2.id])
    sm.supersede_belief(b2, b1.id)

    # Save snapshot
    snap_file = os.path.join(tmp_dir, "snapshot_temporal.json")
    mgr = SnapshotManager(snapshot_path=snap_file)
    mgr.save_snapshot(store, snap_file)

    # Restore into fresh store
    restored_store = ChronoGraphStore()
    mgr.load_snapshot(restored_store, snap_file)

    # 1. Temporal resolution query at Jan 20 -> VS Code
    res_jan = resolve_at_time(restored_store, "user", "favorite_editor", datetime(2025, 1, 20, tzinfo=timezone.utc))
    assert len(res_jan) == 1
    assert res_jan[0].object_value == "VS Code"

    # 2. Temporal resolution query at Feb 20 -> Cursor
    res_feb = resolve_at_time(restored_store, "user", "favorite_editor", datetime(2025, 2, 20, tzinfo=timezone.utc))
    assert len(res_feb) == 1
    assert res_feb[0].object_value == "Cursor"

    # 3. Lineage stack check
    lineage = get_lineage(restored_store, "b2")
    assert lineage["root_belief_id"] == "b2"
    assert len(lineage["history"]) == 2

    # 4. Evidence check
    evidence = get_evidence_for_belief(restored_store, "b2")
    assert len(evidence) == 1
    assert evidence[0].source_text == "Cursor statement"


def test_corrupted_snapshot_handling(tmp_dir):
    """Test 7: Corrupted JSON snapshot raises ValueError gracefully."""
    snap_file = os.path.join(tmp_dir, "corrupted.json")
    with open(snap_file, "w", encoding="utf-8") as f:
        f.write("{ INVALID JSON DATA ...")

    mgr = SnapshotManager(snapshot_path=snap_file)
    store = ChronoGraphStore()

    with pytest.raises(ValueError) as exc:
        mgr.load_snapshot(store, snap_file)
    assert "Corrupted snapshot file" in str(exc.value)


def test_atomic_write_behavior(tmp_dir):
    """Test 8: Atomic write pattern (write to temp file then replace)."""
    snap_file = os.path.join(tmp_dir, "atomic_snap.json")
    mgr = SnapshotManager(snapshot_path=snap_file)
    store = ChronoGraphStore()
    store.add_entity(Entity(id="u1", name="Atomic", entity_type="PERSON"))

    mgr.save_snapshot(store, snap_file)

    # Verify target file exists and temp file was cleaned up
    assert os.path.exists(snap_file)
    temp_files = [f for f in os.listdir(tmp_dir) if f.endswith(".tmp")]
    assert len(temp_files) == 0


def test_concurrent_mutation_protection():
    """Test 9: Multithreaded concurrent additions do not cause race conditions or corrupt store."""
    store = ChronoGraphStore()

    def worker(worker_id: int):
        for i in range(50):
            t = datetime.now(timezone.utc)
            b = BeliefState(
                id=f"b_{worker_id}_{i}",
                subject_id=f"user_{worker_id}",
                predicate="item",
                object_value=f"val_{i}",
                lifecycle_status=LifecycleStatus.ACTIVE,
                confidence=0.9,
                observed_at=t,
                valid_from=t,
                version=1,
            )
            store.add_belief(b)

    threads = [threading.Thread(target=worker, args=(w,)) for w in range(5)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()

    assert len(store.beliefs) == 250


def test_api_validation_error_handling():
    """Test 10: API handles validation errors and malformed requests properly."""
    client = TestClient(app)
    # Missing required 'subject_id' field
    res = client.post("/api/v1/query", json={"predicate": "editor"})
    assert res.status_code == 422


def test_fastapi_startup_recovery_and_end_to_end_restart(tmp_dir):
    """Test 11 & 12: Complete FastAPI startup recovery and end-to-end restart verification.
    
    Ingest -> Query -> Persist -> Restart App -> Query again -> Compare identical semantics.
    """
    store = reset_store()
    snap_file = os.path.join(tmp_dir, "e2e_snap.json")

    # Patch SnapshotManager snapshot_path for test isolation
    from app.api.dependencies import _SNAPSHOT_MANAGER
    _SNAPSHOT_MANAGER.snapshot_path = snap_file

    client = TestClient(app)

    # 1. Ingest via API
    ing_res = client.post("/api/v1/ingest", json={"collection": "test", "session_id": "s1", "text": "I use VS Code as my favorite editor."})
    assert ing_res.status_code == 200

    # 2. Query before restart -> SUPPORTED VS Code
    q1 = client.post("/api/v1/query", json={"subject_id": "user", "predicate": "favorite_editor"})
    assert q1.json()["status"] == "SUPPORTED"
    assert q1.json()["value"] == "VS Code"

    # 3. Simulate App Restart: Reset in-memory store and re-run startup recovery via TestClient lifespan
    reset_store()
    
    # Query before load -> UNKNOWN
    q_blank = client.post("/api/v1/query", json={"subject_id": "user", "predicate": "favorite_editor"})
    assert q_blank.json()["status"] == "UNKNOWN"

    # Restore from snapshot
    restore_from_snapshot()

    # 4. Query after restore -> SUPPORTED VS Code (identical semantics!)
    q2 = client.post("/api/v1/query", json={"subject_id": "user", "predicate": "favorite_editor"})
    assert q2.json()["status"] == "SUPPORTED"
    assert q2.json()["value"] == "VS Code"
    assert q2.json()["confidence"] == q1.json()["confidence"]
