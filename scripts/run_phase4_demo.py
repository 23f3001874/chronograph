"""Phase 4 Demonstration Script for ChronoGraph REST API.

Demonstrates end-to-end temporal belief queries, historical supersessions,
unknown abstention, conflict detection, evidence lookup, and lineage stack
using the FastAPI application instance.
"""

from datetime import datetime, timezone
import json
import os
import sys

# Add backend to sys.path
backend_path = os.path.join(os.path.dirname(__file__), "..", "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from fastapi.testclient import TestClient
from app.api.dependencies import reset_store
from app.engine.state_machine import BeliefStateMachine
from app.main import app
from app.models.domain import (
    BeliefState,
    LifecycleStatus,
    Observation,
)


def run_phase4_demo():
    print("==================================================================")
    print("          CHRONOGRAPH PHASE 4 — FASTAPI REASONING API             ")
    print("==================================================================")

    store = reset_store()
    sm = BeliefStateMachine(store)
    client = TestClient(app)

    # 1. Health check
    res_health = client.get("/health")
    print(f"\n[1/6] GET /health Response: {res_health.json()}")

    # 2. Ingest controlled temporal scenario (VS Code -> Cursor -> VS Code)
    t1 = datetime(2025, 1, 10, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 10, tzinfo=timezone.utc)
    t3 = datetime(2025, 3, 10, tzinfo=timezone.utc)

    obs1 = store.add_observation(Observation(id="o1", source_text="I use VS Code as my favorite editor.", session_id="s1", observed_at=t1))
    obs2 = store.add_observation(Observation(id="o2", source_text="I switched to Cursor and now prefer Cursor over VS Code.", session_id="s2", observed_at=t2))
    obs3 = store.add_observation(Observation(id="o3", source_text="I switched back to VS Code. It is my favorite editor again.", session_id="s3", observed_at=t3))

    b1 = store.add_belief(BeliefState(id="b1_vscode", subject_id="user", predicate="favorite_editor", object_value="VS Code", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1, observation_ids=[obs1.id]))
    b2 = BeliefState(id="b2_cursor", subject_id="user", predicate="favorite_editor", object_value="Cursor", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=t2, valid_from=t2, version=1, observation_ids=[obs2.id])
    sm.supersede_belief(b2, b1.id)

    b3 = BeliefState(id="b3_vscode", subject_id="user", predicate="favorite_editor", object_value="VS Code", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.95, observed_at=t3, valid_from=t3, version=2, observation_ids=[obs3.id])
    sm.supersede_belief(b3, b2.id)

    print("\n[2/6] Executing Point-in-Time Temporal Queries via POST /api/v1/query...")

    # Query Jan 20
    res_jan = client.post("/api/v1/query", json={"subject_id": "user", "predicate": "favorite_editor", "timestamp": "2025-01-20T00:00:00Z", "include_evidence": True})
    print(f"      - Jan 20, 2025: Status={res_jan.json()['status']} | Value='{res_jan.json()['value']}' | Confidence={res_jan.json()['confidence']}")

    # Query Feb 20
    res_feb = client.post("/api/v1/query", json={"subject_id": "user", "predicate": "favorite_editor", "timestamp": "2025-02-20T00:00:00Z", "include_evidence": True})
    print(f"      - Feb 20, 2025: Status={res_feb.json()['status']} | Value='{res_feb.json()['value']}' | Confidence={res_feb.json()['confidence']}")

    # Query Mar 20
    res_mar = client.post("/api/v1/query", json={"subject_id": "user", "predicate": "favorite_editor", "timestamp": "2025-03-20T00:00:00Z", "include_evidence": True, "include_lineage": True})
    print(f"      - Mar 20, 2025: Status={res_mar.json()['status']} | Value='{res_mar.json()['value']}' | Confidence={res_mar.json()['confidence']}")

    print("\n[3/6] Executing UNKNOWN Abstention Query for 'favorite_language'...")
    res_unk = client.post("/api/v1/query", json={"subject_id": "user", "predicate": "favorite_language", "timestamp": "2025-03-20T00:00:00Z"})
    print(f"      - Status: {res_unk.json()['status']} | Value: {res_unk.json()['value']} | Confidence: {res_unk.json()['confidence']}")
    print(f"      - Reason: \"{res_unk.json()['reason']}\"")

    print("\n[4/6] Retrieving Belief Timeline via GET /api/v1/timeline/user/favorite_editor...")
    res_time = client.get("/api/v1/timeline/user/favorite_editor")
    for item in res_time.json()["timeline"]:
        print(f"      - Belief: {item['belief_id']} | Value: '{item['value']}' | Status: {item['status']} | Valid: {item['valid_from']} -> {item['valid_until']}")

    print("\n[5/6] Retrieving Evidence & Lineage Stack via GET /api/v1/beliefs/b3_vscode/lineage...")
    res_lin = client.get("/api/v1/beliefs/b3_vscode/lineage")
    for h in res_lin.json()["history"]:
        b = h["belief"]
        print(f"      - [{h['relationship']}] Belief ID: {b['id']} | Value: '{b['object_value']}' | Status: {b['lifecycle_status']}")

    print("\n[6/6] Demonstrating CONFLICTED Epistemic State Resolution...")
    # Inject overlapping contradiction (Delhi vs Bangalore)
    t_con1 = datetime(2025, 5, 1, tzinfo=timezone.utc)
    t_con2 = datetime(2025, 5, 15, tzinfo=timezone.utc)
    store.add_belief(BeliefState(id="b_delhi", subject_id="user", predicate="location", object_value="Delhi", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t_con1, valid_from=t_con1, version=1))
    store.add_belief(BeliefState(id="b_bangalore", subject_id="user", predicate="location", object_value="Bangalore", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t_con2, valid_from=t_con2, version=1))

    res_con = client.post("/api/v1/query", json={"subject_id": "user", "predicate": "location", "timestamp": "2025-05-20T00:00:00Z"})
    print(f"      - Overlapping Contradiction Query: Status={res_con.json()['status']} | Value={res_con.json()['value']} | Confidence={res_con.json()['confidence']}")

    print("\n==================================================================")
    print("         PHASE 4 DEMONSTRATION EXECUTED SUCCESSFULLY!            ")
    print("==================================================================")


if __name__ == "__main__":
    run_phase4_demo()
