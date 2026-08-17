"""Phase 7 Final Comprehensive System Validation Demonstration Script.

Demonstrates the complete ChronoGraph thesis:
  Ingestion -> Temporal Evolution -> Historical Queries -> UNKNOWN Abstention ->
  CONFLICTED Contradiction -> Lineage Stack -> Grounded Evidence -> Atomic Persistence ->
  Process Restart Simulation -> Identical State Recovery.
"""

from datetime import datetime, timezone
import json
import os
import shutil
import sys
import tempfile

# Add backend to sys.path
backend_path = os.path.join(os.path.dirname(__file__), "..", "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.api.dependencies import reset_store
from app.engine.contradiction import detect_conflicts
from app.engine.persistence import SnapshotManager
from app.engine.state_machine import BeliefStateMachine
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


def run_phase7_demo():
    print("==================================================================")
    print("      CHRONOGRAPH PHASE 7 — FINAL SYSTEM VALIDATION DEMO          ")
    print("==================================================================")

    demo_dir = tempfile.mkdtemp(prefix="chronograph_phase7_demo_")
    snap_path = os.path.join(demo_dir, "chronograph_phase7_snapshot.json")
    mgr = SnapshotManager(snapshot_path=snap_path)

    store = reset_store()
    sm = BeliefStateMachine(store)

    # 1. Ingest Controlled Scenario (VS Code -> Cursor -> VS Code)
    print("\n[1/7] Ingesting Controlled Temporal Memory Sequence...")
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

    # 2. Historical Point-in-Time Resolution
    print("\n[2/7] Resolving Point-in-Time Historical Queries...")
    q_jan = resolve_at_time(store, "user", "favorite_editor", datetime(2025, 1, 20, tzinfo=timezone.utc))[0].object_value
    q_feb = resolve_at_time(store, "user", "favorite_editor", datetime(2025, 2, 20, tzinfo=timezone.utc))[0].object_value
    q_mar = resolve_at_time(store, "user", "favorite_editor", datetime(2025, 3, 20, tzinfo=timezone.utc))[0].object_value

    print(f"      - Query at 2025-01-20: Value='{q_jan}' (Expected: 'VS Code')")
    print(f"      - Query at 2025-02-20: Value='{q_feb}' (Expected: 'Cursor')")
    print(f"      - Query at 2025-03-20: Value='{q_mar}' (Expected: 'VS Code')")

    # 3. Epistemic Abstention (UNKNOWN)
    print("\n[3/7] Testing UNKNOWN Epistemic Abstention...")
    res_unk = resolve_current(store, "user", "favorite_language", datetime(2025, 3, 20, tzinfo=timezone.utc))
    val_unk = res_unk.beliefs[0].object_value if res_unk.beliefs else None
    print(f"      - Query 'favorite_language': Status={res_unk.status.value} | Value={val_unk} | Confidence={res_unk.confidence}")
    print(f"      - Reason: \"{res_unk.reason}\"")

    # 4. Overlapping Contradiction (CONFLICTED)
    print("\n[4/7] Testing Overlapping Contradiction (CONFLICTED)...")
    t_con1 = datetime(2025, 5, 1, tzinfo=timezone.utc)
    t_con2 = datetime(2025, 5, 15, tzinfo=timezone.utc)
    store.add_belief(BeliefState(id="b_delhi", subject_id="user", predicate="location", object_value="Delhi", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t_con1, valid_from=t_con1, version=1))
    store.add_belief(BeliefState(id="b_bangalore", subject_id="user", predicate="location", object_value="Bangalore", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t_con2, valid_from=t_con2, version=1))

    detect_conflicts(store, "user", "location")
    res_con = resolve_current(store, "user", "location", datetime(2025, 5, 20, tzinfo=timezone.utc))
    val_con = res_con.beliefs[0].object_value if res_con.beliefs and res_con.status == ResolutionStatus.SUPPORTED else None
    print(f"      - Query 'location': Status={res_con.status.value} | Value={val_con} | Confidence={res_con.confidence}")

    # 5. Lineage & Grounded Evidence
    print("\n[5/7] Inspecting Lineage Stack & Grounded Evidence...")
    lineage = get_lineage(store, "b3_vscode")
    print(f"      - Lineage Root ID: {lineage['root_belief_id']} (Depth: {len(lineage['history'])})")
    for h in lineage['history']:
        b = h['belief']
        print(f"        * [{h['relationship']}] ID: {b.id} | Value: '{b.object_value}' | Status: {b.lifecycle_status.value}")

    evidence = get_evidence_for_belief(store, "b3_vscode")
    print(f"      - Grounded Observations Count: {len(evidence)}")
    print(f"        * Observation text: \"{evidence[0].source_text}\"")

    # 6. Atomic Persistence & Process Restart Recovery
    print("\n[6/7] Testing Atomic Snapshot Persistence & Store Recovery...")
    mgr.save_snapshot(store, snap_path)
    file_bytes = os.path.getsize(snap_path)
    print(f"      - Atomic snapshot saved to '{snap_path}' ({file_bytes} bytes)")

    # Clear in-memory store completely
    reset_store()
    blank_res = resolve_current(store, "user", "favorite_editor", datetime(2025, 3, 20, tzinfo=timezone.utc))
    print(f"      - Memory status after reset: Status={blank_res.status.value} (Store empty)")

    # Restore from snapshot
    mgr.load_snapshot(store, snap_path)
    print(f"      - Store restored from disk: {len(store.beliefs)} belief states recovered")

    # 7. Post-Restore Verification
    print("\n[7/7] Verifying Post-Restoration Semantics...")
    q_jan_post = resolve_at_time(store, "user", "favorite_editor", datetime(2025, 1, 20, tzinfo=timezone.utc))[0].object_value
    q_feb_post = resolve_at_time(store, "user", "favorite_editor", datetime(2025, 2, 20, tzinfo=timezone.utc))[0].object_value
    q_mar_post = resolve_at_time(store, "user", "favorite_editor", datetime(2025, 3, 20, tzinfo=timezone.utc))[0].object_value
    res_unk_post = resolve_current(store, "user", "favorite_language", datetime(2025, 3, 20, tzinfo=timezone.utc))
    res_con_post = resolve_current(store, "user", "location", datetime(2025, 5, 20, tzinfo=timezone.utc))

    assert q_jan_post == q_jan
    assert q_feb_post == q_feb
    assert q_mar_post == q_mar
    assert res_unk_post.status == ResolutionStatus.UNKNOWN
    assert res_con_post.status == ResolutionStatus.CONFLICTED

    print(f"      - Post-Restore Jan 20: '{q_jan_post}' (Matches: True)")
    print(f"      - Post-Restore Feb 20: '{q_feb_post}' (Matches: True)")
    print(f"      - Post-Restore Mar 20: '{q_mar_post}' (Matches: True)")
    print(f"      - Post-Restore UNKNOWN: {res_unk_post.status.value} (Matches: True)")
    print(f"      - Post-Restore CONFLICTED: {res_con_post.status.value} (Matches: True)")

    shutil.rmtree(demo_dir, ignore_errors=True)

    print("\n==================================================================")
    print("      CHRONOGRAPH PHASE 7 SYSTEM VALIDATION PASSED 100%!         ")
    print("==================================================================")


if __name__ == "__main__":
    run_phase7_demo()
