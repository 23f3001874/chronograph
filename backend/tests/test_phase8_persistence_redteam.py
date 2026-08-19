"""Phase 8 Persistence Engine Red-Team Audit Suite."""

from datetime import datetime, timezone
import json
import os
import shutil
import tempfile
import pytest

from app.engine.persistence import SnapshotManager
from app.engine.store import ChronoGraphStore
from app.models.domain import BeliefState, EdgeType, GraphEdge, LifecycleStatus, Observation


@pytest.fixture
def tmp_dir():
    dir_path = tempfile.mkdtemp(prefix="chronograph_pers_redteam_")
    yield dir_path
    shutil.rmtree(dir_path, ignore_errors=True)


def test_redteam_persistence_empty_snapshot_handling(tmp_dir):
    """Attack 1: Loading an empty snapshot clears store cleanly."""
    snap_file = os.path.join(tmp_dir, "empty.json")
    with open(snap_file, "w", encoding="utf-8") as f:
        json.dump({"version": "1.0", "entities": [], "observations": [], "beliefs": [], "edges": []}, f)

    mgr = SnapshotManager(snapshot_path=snap_file)
    store = ChronoGraphStore()
    store.add_observation(Observation(id="o1", source_text="test", session_id="s1", observed_at=datetime.now(timezone.utc)))

    mgr.load_snapshot(store, snap_file)
    assert len(store.observations) == 0
    assert len(store.beliefs) == 0


def test_redteam_persistence_missing_referenced_observation(tmp_dir):
    """Attack 2: Belief referencing a missing observation ID degrades gracefully without crashing."""
    snap_file = os.path.join(tmp_dir, "missing_obs.json")
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc).isoformat()
    data = {
        "version": "1.0",
        "entities": [],
        "observations": [],  # Observation list EMPTY
        "beliefs": [
            {
                "id": "b1", "subject_id": "user", "predicate": "city", "object_value": "Delhi",
                "lifecycle_status": "ACTIVE", "confidence": 0.9, "observed_at": t1, "valid_from": t1,
                "valid_until": None, "version": 1, "observation_ids": ["nonexistent_obs_999"]
            }
        ],
        "edges": [],
    }

    with open(snap_file, "w", encoding="utf-8") as f:
        json.dump(data, f)

    mgr = SnapshotManager(snapshot_path=snap_file)
    store = ChronoGraphStore()
    mgr.load_snapshot(store, snap_file)

    assert len(store.beliefs) == 1
    assert store.get_belief("b1").observation_ids == ["nonexistent_obs_999"]
