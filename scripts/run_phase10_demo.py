"""Phase 10 Presentation & Hack Hydra Demo Verification Script.

Executes and verifies the 10-point presentation killer scenario offline and deterministically.
"""

from datetime import datetime, timezone
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.api.dependencies import reset_store
from app.engine.contradiction import detect_conflicts
from app.engine.state_machine import BeliefStateMachine
from app.engine.store import ChronoGraphStore
from app.engine.temporal_resolver import (
    get_evidence_for_belief,
    get_lineage,
)
from app.services.ingestion_pipeline import query_structured_answer
from app.models.domain import BeliefState, Entity, LifecycleStatus, Observation, ResolutionStatus


def run_phase10_demo_verification() -> None:
    print("=" * 70)
    print("      CHRONOGRAPH PHASE 10 — HACK HYDRA KILLER DEMO VERIFICATION")
    print("=" * 70)

    # 1. Initialize Store
    print("\n[1/10] Initializing ChronoGraph Engine & Store...")
    store = reset_store()
    store.add_entity(Entity(id="user", name="Alex", entity_type="PERSON"))

    # 2. Ingest Killer Temporal Memory Sequence
    print("[2/10] Loading Killer Temporal Scenario (VS Code -> Cursor -> VS Code)...")
    t_jan = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t_feb = datetime(2025, 2, 1, tzinfo=timezone.utc)
    t_mar = datetime(2025, 3, 1, tzinfo=timezone.utc)

    o1 = Observation(id="obs_jan_vscode", source_text="I use VS Code as my favorite editor.", session_id="s_jan", observed_at=t_jan, valid_from=t_jan, valid_until=t_feb)
    o2 = Observation(id="obs_feb_cursor", source_text="I switched to Cursor. Cursor is now my favorite editor.", session_id="s_feb", observed_at=t_feb, valid_from=t_feb, valid_until=t_mar)
    o3 = Observation(id="obs_mar_vscode", source_text="I switched back to VS Code. It is my favorite editor again.", session_id="s_mar", observed_at=t_mar, valid_from=t_mar)

    o4 = Observation(id="obs_delhi", source_text="I live in Delhi.", session_id="s_loc_1", observed_at=datetime(2025, 1, 10, tzinfo=timezone.utc), valid_from=t_jan, valid_until=t_mar)
    o5 = Observation(id="obs_blr", source_text="I live in Bangalore.", session_id="s_loc_2", observed_at=datetime(2025, 2, 10, tzinfo=timezone.utc), valid_from=t_feb, valid_until=datetime(2025, 4, 1, tzinfo=timezone.utc))

    for o in [o1, o2, o3, o4, o5]:
        store.add_observation(o)

    sm = BeliefStateMachine(store)
    b1 = store.add_belief(BeliefState(id="b1_vscode", subject_id="user", predicate="favorite_editor", object_value="VS Code", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=t_jan, valid_from=t_jan, valid_until=t_feb, version=1, observation_ids=[o1.id]))
    sm.activate_belief(b1)

    b2 = store.add_belief(BeliefState(id="b2_cursor", subject_id="user", predicate="favorite_editor", object_value="Cursor", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=t_feb, valid_from=t_feb, valid_until=t_mar, version=2, observation_ids=[o2.id]))
    sm.supersede_belief(b2, b1.id)

    b3 = store.add_belief(BeliefState(id="b3_vscode", subject_id="user", predicate="favorite_editor", object_value="VS Code", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=t_mar, valid_from=t_mar, version=3, observation_ids=[o3.id]))
    sm.supersede_belief(b3, b2.id)

    b_loc1 = store.add_belief(BeliefState(id="b_loc1_delhi", subject_id="user", predicate="location", object_value="Delhi", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=datetime(2025, 1, 10, tzinfo=timezone.utc), valid_from=t_jan, valid_until=t_mar, version=1, observation_ids=[o4.id]))
    sm.activate_belief(b_loc1)

    b_loc2 = store.add_belief(BeliefState(id="b_loc2_blr", subject_id="user", predicate="location", object_value="Bangalore", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=datetime(2025, 2, 10, tzinfo=timezone.utc), valid_from=t_feb, valid_until=datetime(2025, 4, 1, tzinfo=timezone.utc), version=1, observation_ids=[o5.id]))
    sm.activate_belief(b_loc2)

    detect_conflicts(store, "user", "location")

    # 3. Verify Query 1: Jan 20 -> VS Code
    print("[3/10] Query 1 (Jan 20, 2025): Evaluating historical preference...")
    q1 = query_structured_answer(store, "user", "favorite_editor", datetime(2025, 1, 20, tzinfo=timezone.utc))
    assert q1["status"] == "SUPPORTED"
    assert q1["value"] == "VS Code"
    print(f"      - Output: Value='{q1['value']}' | Status={q1['status']} (PASS)")

    # 4. Verify Query 2: Feb 20 -> Cursor
    print("[4/10] Query 2 (Feb 20, 2025): Evaluating historical preference...")
    q2 = query_structured_answer(store, "user", "favorite_editor", datetime(2025, 2, 20, tzinfo=timezone.utc))
    assert q2["status"] == "SUPPORTED"
    assert q2["value"] == "Cursor"
    print(f"      - Output: Value='{q2['value']}' | Status={q2['status']} (PASS)")

    # 5. Verify Query 3: Mar 20 -> VS Code
    print("[5/10] Query 3 (Mar 20, 2025): Evaluating historical preference...")
    q3 = query_structured_answer(store, "user", "favorite_editor", datetime(2025, 3, 20, tzinfo=timezone.utc))
    assert q3["status"] == "SUPPORTED"
    assert q3["value"] == "VS Code"
    print(f"      - Output: Value='{q3['value']}' | Status={q3['status']} (PASS)")

    # 6. Verify Query 4: Unknown Fact -> UNKNOWN
    print("[6/10] Query 4 (Absent Fact): Querying 'favorite_language'...")
    q4 = query_structured_answer(store, "user", "favorite_language", datetime(2025, 1, 20, tzinfo=timezone.utc))
    assert q4["status"] == "UNKNOWN"
    assert q4["value"] is None
    assert q4["confidence"] == 0.0
    print(f"      - Output: Value={q4['value']} | Status={q4['status']} | Confidence={q4['confidence']} (PASS)")

    # 7. Verify Query 5: Contradiction -> CONFLICTED
    print("[7/10] Query 5 (Overlapping Disagreement): Querying 'location'...")
    q5 = query_structured_answer(store, "user", "location", datetime(2025, 2, 15, tzinfo=timezone.utc))
    assert q5["status"] == "CONFLICTED"
    assert q5["value"] is None
    assert q5["confidence"] == 0.5
    print(f"      - Output: Value={q5['value']} | Status={q5['status']} | Confidence={q5['confidence']} (PASS)")

    # 8. Verify Evidence Grounding
    print("[8/10] Inspecting Grounded Evidence Observations...")
    ev = get_evidence_for_belief(store, "b3_vscode")
    assert len(ev) == 1
    assert ev[0].source_text == "I switched back to VS Code. It is my favorite editor again."
    print(f"      - Grounded Text: \"{ev[0].source_text}\" (PASS)")

    # 9. Verify Lineage Stack
    print("[9/10] Traversing Cycle-Safe Lineage Stack...")
    lin = get_lineage(store, "b3_vscode")
    assert lin["root_belief_id"] == "b3_vscode"
    assert len(lin["history"]) == 3
    print(f"      - Lineage Stack Depth: {len(lin['history'])} nodes traversed (PASS)")

    # 10. Verify Persistence & Snapshot Recovery
    print("[10/10] Verifying Atomic Persistence & Restoration...")
    from app.engine.persistence import SnapshotManager
    import tempfile
    import os

    tmp = tempfile.mktemp(suffix=".json")
    mgr = SnapshotManager(snapshot_path=tmp)
    mgr.save_snapshot(store, tmp)

    store_restored = ChronoGraphStore()
    mgr.load_snapshot(store_restored, tmp)
    assert len(store_restored.beliefs) == 5

    q_res = query_structured_answer(store_restored, "user", "favorite_editor", datetime(2025, 2, 20, tzinfo=timezone.utc))
    assert q_res["value"] == "Cursor"
    print(f"      - Restored Feb 20 Query: Value='{q_res['value']}' (PASS)")

    if os.path.exists(tmp):
        os.remove(tmp)

    print("\n" + "=" * 70)
    print("      CHRONOGRAPH PHASE 10 DEMO VERIFICATION PASSED 100%!")
    print("=" * 70)


if __name__ == "__main__":
    run_phase10_demo_verification()
