"""Phase 8 REST API & HydraDB Failure Mode Red-Team Audit Suite."""

from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_pipeline, reset_store
from app.main import app
from app.services.ingestion_pipeline import ChronoGraphIngestionPipeline


@pytest.fixture
def client():
    reset_store()
    return TestClient(app)


def test_redteam_api_malformed_json_and_invalid_types(client):
    """Attack 1: Malformed JSON or invalid data types return HTTP 422 Unprocessable Entity."""
    # 1. Invalid timestamp format
    res1 = client.post("/api/v1/query", json={"subject_id": "user", "predicate": "city", "timestamp": "invalid_date_str"})
    assert res1.status_code == 422

    # 2. Non-boolean for include_evidence
    res2 = client.post("/api/v1/query", json={"subject_id": "user", "predicate": "city", "include_evidence": "not_a_bool"})
    assert res2.status_code == 422


def test_redteam_api_nonexistent_resources_return_404(client):
    """Attack 2: Querying non-existent belief detail, evidence, or lineage returns HTTP 404 Not Found."""
    res_b = client.get("/api/v1/beliefs/nonexistent_b999")
    assert res_b.status_code == 404

    res_ev = client.get("/api/v1/beliefs/nonexistent_b999/evidence")
    assert res_ev.status_code == 404

    res_lin = client.get("/api/v1/beliefs/nonexistent_b999/lineage")
    assert res_lin.status_code == 404


def test_redteam_api_hydradb_external_failure_preserves_local_state(client):
    """Attack 3: Mocking HydraDB network timeout/500 failure during ingestion does NOT corrupt local ChronoGraph state."""
    store = reset_store()
    mock_service = MagicMock()
    mock_service.query_memory.side_effect = RuntimeError("HydraDB API 500 Internal Server Error")

    mock_pipeline = ChronoGraphIngestionPipeline(service=mock_service)
    app.dependency_overrides[get_pipeline] = lambda: mock_pipeline

    try:
        req = {"collection": "test", "session_id": "s1", "text": "I use VS Code."}
        # External failure should raise Exception cleanly without corrupting store
        with pytest.raises(Exception):
            mock_pipeline.process_memories(collection="test", session_id="s1", query="VS Code", store=store)

        # Store remains clean with zero corrupted partial entries
        assert len(store.observations) == 0
        assert len(store.beliefs) == 0
    finally:
        app.dependency_overrides.clear()
