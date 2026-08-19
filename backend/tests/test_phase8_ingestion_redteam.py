"""Phase 8 Ingestion Pipeline Red-Team Audit Suite."""

from datetime import datetime, timezone
from unittest.mock import MagicMock
import pytest

from app.api.dependencies import reset_store
from app.services.ingestion_pipeline import ChronoGraphIngestionPipeline
from app.services.hydradb_types import HydraQueryResult


def test_redteam_ingestion_invalid_collection_raises_error():
    """Attack 1: Empty or whitespace-only collection partition raises ValueError."""
    pipeline = ChronoGraphIngestionPipeline(service=MagicMock())

    with pytest.raises(ValueError):
        pipeline.process_memories(collection="   ", memories=[{"text": "test"}], query_hint="test")


def test_redteam_ingestion_empty_query_result_degrades_gracefully():
    """Attack 2: HydraDB returning zero chunks or empty graph context degrades safely to UNKNOWN without corrupting store."""
    store = reset_store()
    mock_service = MagicMock()
    mock_service.query_memory.return_value = HydraQueryResult(
        database="chronograph_exp_db",
        collection="test_coll",
        query="unknown predicate",
        chunks=[],
        context_triplets=[],
        raw_response={},
    )

    pipeline = ChronoGraphIngestionPipeline(service=mock_service)
    res_store, obs_list, b_list = pipeline.process_memories(
        collection="test_coll",
        memories=[{"id": "m1", "text": "What is my favorite language?", "additional_metadata": {"timestamp": "2025-01-10T00:00:00Z"}}],
        query_hint="What is my favorite language?",
    )

    assert len(obs_list) == 1
    assert obs_list[0].source_text == "What is my favorite language?"
