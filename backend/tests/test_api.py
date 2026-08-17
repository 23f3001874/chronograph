"""API test suite for ChronoGraph FastAPI endpoints using TestClient."""

from datetime import datetime, timezone
import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_store, reset_store
from app.engine.state_machine import BeliefStateMachine
from app.main import app
from app.models.domain import (
    BeliefState,
    LifecycleStatus,
    Observation,
)


@pytest.fixture
def client():
    # Reset process-local store before each test for test isolation
    reset_store()
    return TestClient(app)


def test_health_endpoint(client):
    """Test 1: GET /health returns ok status."""
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok", "service": "chronograph"}


def test_supported_query(client):
    """Test 2: POST /api/v1/query resolves SUPPORTED active belief."""
    store = reset_store()
    t = datetime(2025, 1, 10, tzinfo=timezone.utc)
    obs = store.add_observation(Observation(id="o1", source_text="I use VS Code.", session_id="s1", observed_at=t))
    b = store.add_belief(
        BeliefState(
            id="b1_vscode", subject_id="user", predicate="favorite_editor", object_value="VS Code",
            lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t, valid_from=t, version=1, observation_ids=[obs.id]
        )
    )

    req = {
        "subject_id": "user",
        "predicate": "favorite_editor",
        "timestamp": "2025-01-15T00:00:00Z",
        "include_evidence": True,
    }
    res = client.post("/api/v1/query", json=req)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "SUPPORTED"
    assert data["value"] == "VS Code"
    assert data["confidence"] == 0.9
    assert data["belief_id"] == "b1_vscode"
    assert len(data["evidence"]) == 1
    assert data["evidence"][0]["text"] == "I use VS Code."


def test_unknown_query(client):
    """Test 3 & 12: Querying absent attribute returns UNKNOWN status and 0.0 confidence without converting to SUPPORTED."""
    req = {
        "subject_id": "user",
        "predicate": "favorite_language",
        "timestamp": "2025-03-20T00:00:00Z",
    }
    res = client.post("/api/v1/query", json=req)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "UNKNOWN"
    assert data["value"] is None
    assert data["confidence"] == 0.0
    assert "No recorded evidence" in data["reason"]


def test_conflicted_query(client):
    """Test 4 & 13: Querying overlapping active contradictions returns CONFLICTED without converting to SUPPORTED."""
    store = reset_store()
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 1, tzinfo=timezone.utc)
    t3 = datetime(2025, 3, 1, tzinfo=timezone.utc)
    t4 = datetime(2025, 4, 1, tzinfo=timezone.utc)

    # Overlapping active beliefs (Delhi Jan 1-Mar 1 vs Bangalore Feb 1-Apr 1)
    b1 = store.add_belief(
        BeliefState(
            id="b1_delhi", subject_id="user", predicate="lives_in", object_value="Delhi",
            lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, valid_until=t3, version=1
        )
    )
    b2 = store.add_belief(
        BeliefState(
            id="b2_bangalore", subject_id="user", predicate="lives_in", object_value="Bangalore",
            lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t2, valid_from=t2, valid_until=t4, version=1
        )
    )

    req = {
        "subject_id": "user",
        "predicate": "lives_in",
        "timestamp": "2025-02-15T00:00:00Z",
    }
    res = client.post("/api/v1/query", json=req)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "CONFLICTED"
    assert data["value"] is None
    assert data["confidence"] == 0.5


def test_temporal_query(client):
    """Test 5: Querying at different point-in-time timestamps T."""
    store = reset_store()
    sm = BeliefStateMachine(store)

    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 1, tzinfo=timezone.utc)

    b1 = store.add_belief(
        BeliefState(
            id="b1", subject_id="user", predicate="lives_in", object_value="Delhi",
            lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1
        )
    )
    b2 = BeliefState(
        id="b2", subject_id="user", predicate="lives_in", object_value="Bangalore",
        lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=t2, valid_from=t2, version=1
    )
    sm.supersede_belief(b2, b1.id)

    # Query at Jan 15 -> Delhi
    res_jan = client.post("/api/v1/query", json={"subject_id": "user", "predicate": "lives_in", "timestamp": "2025-01-15T00:00:00Z"})
    assert res_jan.json()["value"] == "Delhi"

    # Query at Feb 15 -> Bangalore
    res_feb = client.post("/api/v1/query", json={"subject_id": "user", "predicate": "lives_in", "timestamp": "2025-02-15T00:00:00Z"})
    assert res_feb.json()["value"] == "Bangalore"


def test_timeline_endpoint(client):
    """Test 6: GET /api/v1/timeline/{subject_id}/{predicate}."""
    store = reset_store()
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 1, tzinfo=timezone.utc)

    store.add_belief(
        BeliefState(
            id="b1", subject_id="user", predicate="editor", object_value="VS Code",
            lifecycle_status=LifecycleStatus.SUPERSEDED, confidence=0.9, observed_at=t1, valid_from=t1, valid_until=t2, version=1
        )
    )
    store.add_belief(
        BeliefState(
            id="b2", subject_id="user", predicate="editor", object_value="Cursor",
            lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.95, observed_at=t2, valid_from=t2, version=2
        )
    )

    res = client.get("/api/v1/timeline/user/editor")
    assert res.status_code == 200
    data = res.json()
    assert data["subject_id"] == "user"
    assert data["predicate"] == "editor"
    assert len(data["timeline"]) == 2
    assert data["timeline"][0]["value"] == "VS Code"
    assert data["timeline"][1]["value"] == "Cursor"


def test_belief_detail_evidence_and_lineage_endpoints(client):
    """Test 7, 8, 9 & 10: Belief lookup, evidence endpoint, lineage endpoint, and 404 for nonexistent belief."""
    store = reset_store()
    sm = BeliefStateMachine(store)
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 1, tzinfo=timezone.utc)

    obs1 = store.add_observation(Observation(id="o1", source_text="VS Code text", session_id="s1", observed_at=t1))
    obs2 = store.add_observation(Observation(id="o2", source_text="Cursor text", session_id="s2", observed_at=t2))

    b1 = store.add_belief(
        BeliefState(
            id="b1", subject_id="user", predicate="editor", object_value="VS Code",
            lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1, observation_ids=[obs1.id]
        )
    )
    b2 = BeliefState(
        id="b2", subject_id="user", predicate="editor", object_value="Cursor",
        lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.95, observed_at=t2, valid_from=t2, version=1, observation_ids=[obs2.id]
    )
    sm.supersede_belief(b2, b1.id)

    # 1. Belief Detail GET /api/v1/beliefs/b2
    res_b2 = client.get("/api/v1/beliefs/b2")
    assert res_b2.status_code == 200
    assert res_b2.json()["object_value"] == "Cursor"

    # 2. Evidence GET /api/v1/beliefs/b2/evidence
    res_ev = client.get("/api/v1/beliefs/b2/evidence")
    assert res_ev.status_code == 200
    assert len(res_ev.json()) == 1
    assert res_ev.json()[0]["text"] == "Cursor text"

    # 3. Lineage GET /api/v1/beliefs/b2/lineage
    res_lin = client.get("/api/v1/beliefs/b2/lineage")
    assert res_lin.status_code == 200
    assert res_lin.json()["root_belief_id"] == "b2"

    # 4. Nonexistent belief 404
    res_404 = client.get("/api/v1/beliefs/nonexistent")
    assert res_404.status_code == 404


def test_ingest_endpoint(client):
    """Test 11: POST /api/v1/ingest ingests statement and creates belief."""
    req = {
        "collection": "test_coll",
        "session_id": "s1",
        "text": "I use VS Code as my favorite editor.",
    }
    res = client.post("/api/v1/ingest", json=req)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["observations_created"] == 1
    assert data["beliefs_created"] == 1

    # Verify query reflects the ingested belief
    query_res = client.post("/api/v1/query", json={"subject_id": "user", "predicate": "favorite_editor"})
    assert query_res.json()["value"] == "VS Code"
