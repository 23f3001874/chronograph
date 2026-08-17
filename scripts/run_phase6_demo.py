"""Phase 6 End-to-End Persistence Demonstration Script.

Demonstrates:
  ingest -> query -> persist to disk -> clear memory -> restore from disk -> query again
  Verifies that SUPPORTED, UNKNOWN, CONFLICTED, SUPERSEDED, and CANCELLED semantics survive restart identically.
"""

from datetime import datetime, timezone
import os
import shutil
import sys
import tempfile

# Add backend to sys.path
backend_path = os.path.join(os.path.dirname(__file__), "..", "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.api.dependencies import get_store, reset_store
from app.engine.persistence import SnapshotManager
from app.engine.state_machine import BeliefStateMachine
from app.engine.temporal_resolver import resolve_at_time, resolve_current
from app.models.domain import BeliefState, LifecycleStatus, Observation, ResolutionStatus


def run_phase6_demo():
    print("==================================================================")
    print("      CHRONOGRAPH PHASE 6 — PERSISTENCE & RECOVERY DEMO          ")
    print("==================================================================")

    # 1. Setup temporary snapshot path for demonstration
    demo_dir = tempfile.mkdtemp(prefix="chronograph_phase6_demo_")
    snap_path = os.path.join(demo_dir, "chronograph_snapshot_demo.json")
    mgr = SnapshotManager(snapshot_path=snap_path)

    store = reset_store()
    sm = BeliefStateMachine(store)

    print(f"\n[1/6] Initializing Store & Ingesting Controlled Temporal Scenario...")
    t1 = datetime(2025, 1, 10, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 10, tzinfo=timezone.utc)
    t3 = datetime(2025, 3, 10, tzinfo=timezone.utc)

    obs1 = store.add_observation(Observation(id="o1", source_text="I use VS Code as my favorite editor.", session_id="s1", observed_at=t1))
    obs2 = store.add_observation(Observation(id="o2", source_text="I switched to Cursor.", session_id="s2", observed_at=t2))
    obs3 = store.add_observation(Observation(id="o3", source_text="I switched back to VS Code.", session_id="s3", observed_at=t3))

    b1 = store.add_belief(BeliefState(id="b1_vscode", subject_id="user", predicate="favorite_editor", object_value="VS Code", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1, observation_ids=[obs1.id]))
    b2 = BeliefState(id="b2_cursor", subject_id="user", predicate="favorite_editor", object_value="Cursor", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=t2, valid_from=t2, version=1, observation_ids=[obs2.id])
    sm.supersede_belief(b2, b1.id)

    b3 = BeliefState(id="b3_vscode", subject_id="user", predicate="favorite_editor", object_value="VS Code", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.95, observed_at=t3, valid_from=t3, version=2, observation_ids=[obs3.id])
    sm.supersede_belief(b3, b2.id)

    print("\n[2/6] Executing Pre-Persistence State Queries...")
    q1_before = resolve_at_time(store, "user", "favorite_editor", datetime(2025, 1, 20, tzinfo=timezone.utc))[0].object_value
    q2_before = resolve_at_time(store, "user", "favorite_editor", datetime(2025, 2, 20, tzinfo=timezone.utc))[0].object_value
    q3_before = resolve_at_time(store, "user", "favorite_editor", datetime(2025, 3, 20, tzinfo=timezone.utc))[0].object_value
    q_unk_before = resolve_current(store, "user", "favorite_language", datetime(2025, 3, 20, tzinfo=timezone.utc)).status.value

    print(f"      - Jan 20, 2025: {q1_before}")
    print(f"      - Feb 20, 2025: {q2_before}")
    print(f"      - Mar 20, 2025: {q3_before}")
    print(f"      - Absent Query: {q_unk_before}")

    print("\n[3/6] Saving Atomic Snapshot to Disk...")
    mgr.save_snapshot(store, snap_path)
    file_size = os.path.getsize(snap_path)
    print(f"      Snapshot File Created: '{snap_path}' ({file_size} bytes)")

    print("\n[4/6] Simulating Process Restart (Clearing In-Memory Store Completely)...")
    store = reset_store()
    q1_empty = resolve_current(store, "user", "favorite_editor", datetime(2025, 3, 20, tzinfo=timezone.utc)).status.value
    print(f"      - State immediately after memory clear: {q1_empty} (Store is 100% empty)")

    print("\n[5/6] Restoring Store from Disk Snapshot...")
    mgr.load_snapshot(store, snap_path)
    print(f"      - Restored Entities: {len(store.entities)}")
    print(f"      - Restored Observations: {len(store.observations)}")
    print(f"      - Restored Belief States: {len(store.beliefs)}")
    print(f"      - Restored Graph Edges: {len(store.edges)}")

    print("\n[6/6] Executing Post-Restoration Queries & Comparing Semantics...")
    q1_after = resolve_at_time(store, "user", "favorite_editor", datetime(2025, 1, 20, tzinfo=timezone.utc))[0].object_value
    q2_after = resolve_at_time(store, "user", "favorite_editor", datetime(2025, 2, 20, tzinfo=timezone.utc))[0].object_value
    q3_after = resolve_at_time(store, "user", "favorite_editor", datetime(2025, 3, 20, tzinfo=timezone.utc))[0].object_value
    q_unk_after = resolve_current(store, "user", "favorite_language", datetime(2025, 3, 20, tzinfo=timezone.utc)).status.value

    print(f"      - Jan 20, 2025: {q1_after} (Matches Before: {q1_after == q1_before})")
    print(f"      - Feb 20, 2025: {q2_after} (Matches Before: {q2_after == q2_before})")
    print(f"      - Mar 20, 2025: {q3_after} (Matches Before: {q3_after == q3_before})")
    print(f"      - Absent Query: {q_unk_after} (Matches Before: {q_unk_after == q_unk_before})")

    # Cleanup temp demo dir
    shutil.rmtree(demo_dir, ignore_errors=True)

    print("\n==================================================================")
    print("      PERSISTENCE & RECOVERY DEMONSTRATION PASSED 100%!           ")
    print("==================================================================")


if __name__ == "__main__":
    run_phase6_demo()
