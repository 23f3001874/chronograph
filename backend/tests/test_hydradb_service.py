"""Unit tests for HydraDBService using mocked SDK calls (no network required)."""

from unittest.mock import MagicMock, patch
import pytest

from app.services.hydradb_service import HydraDBService
from app.services.hydradb_types import (
    HydraChunkEvidence,
    HydraMemoryResultItem,
    HydraQueryResult,
    HydraTripletRelation,
)


def test_service_configuration_validation(monkeypatch):
    """Test 1: Service raises ValueError when API key or database configuration is missing."""
    monkeypatch.delenv("HYDRA_DB_API_KEY", raising=False)
    monkeypatch.delenv("HYDRA_DB_DATABASE", raising=False)

    with pytest.raises(ValueError) as exc:
        HydraDBService(api_key=None, database="test_db")
    assert "HYDRA_DB_API_KEY is missing" in str(exc.value)

    with pytest.raises(ValueError) as exc:
        HydraDBService(api_key="valid_key", database="")
    assert "HYDRA_DB_DATABASE configuration is missing" in str(exc.value)


def test_collection_propagation_validation():
    """Test 4: Service enforces explicit collection parameter on all memory operations."""
    service = HydraDBService(api_key="test_key", database="test_db")

    with pytest.raises(ValueError) as exc:
        service.ingest_memory(collection="", memories=[{"text": "hello"}])
    assert "Explicit collection partition identifier is required" in str(exc.value)

    with pytest.raises(ValueError) as exc:
        service.query_memory(collection="  ", query="hello")
    assert "Explicit collection partition identifier is required" in str(exc.value)


@patch("app.services.hydradb_service.HydraDBService.client")
def test_memory_ingest_request_construction_and_type_propagation(mock_client):
    """Test 2 & 5: Ingestion request construction, memory type propagation, and result parsing."""
    mock_res_item = MagicMock()
    mock_res_item.id = "mem_001"
    mock_res_item.status = "queued"
    mock_res_item.error_code = None
    mock_res_item.error = None

    mock_response = MagicMock()
    mock_response.data.results = [mock_res_item]
    mock_client.context.ingest.return_value = mock_response

    service = HydraDBService(api_key="test_key", database="test_db")
    results = service.ingest_memory(
        collection="user_alex",
        memories=[{"id": "mem_001", "text": "VS Code"}],
        infer=True,
    )

    assert len(results) == 1
    assert results[0].id == "mem_001"
    assert results[0].status == "queued"

    # Verify underlying SDK call parameters
    mock_client.context.ingest.assert_called_once()
    kwargs = mock_client.context.ingest.call_args.kwargs

    assert kwargs["type"] == "memory"
    assert kwargs["database"] == "test_db"
    assert kwargs["collection"] == "user_alex"
    assert '"infer": true' in kwargs["memories"]


@patch("app.services.hydradb_service.HydraDBService.client")
def test_query_request_construction(mock_client):
    """Test 3: Query request construction and result parsing into DTOs."""
    mock_chunk = MagicMock()
    mock_chunk.id = "chunk_1"
    mock_chunk.chunk_uuid = "uuid_1"
    mock_chunk.chunk_content = "I live in Delhi."
    mock_chunk.relevancy_score = 0.92
    mock_chunk.source_title = "Title"
    mock_chunk.source_type = "memory"
    mock_chunk.metadata = {}
    mock_chunk.additional_metadata = {"session_id": "s1"}

    mock_response = MagicMock()
    mock_response.data.chunks = [mock_chunk]
    mock_response.data.graph_context = None
    mock_response.data.additional_context = None
    mock_client.query.return_value = mock_response

    service = HydraDBService(api_key="test_key", database="test_db")
    query_res = service.query_memory(
        collection="user_alex",
        query="Where does the user live?",
        mode="thinking",
    )

    assert isinstance(query_res, HydraQueryResult)
    assert query_res.collection == "user_alex"
    assert len(query_res.chunks) == 1
    assert query_res.chunks[0].chunk_content == "I live in Delhi."

    mock_client.query.assert_called_once()
    kwargs = mock_client.query.call_args.kwargs
    assert kwargs["type"] == "memory"
    assert kwargs["query_by"] == "hybrid"
    assert kwargs["mode"] == "thinking"
    assert kwargs["collection"] == "user_alex"
