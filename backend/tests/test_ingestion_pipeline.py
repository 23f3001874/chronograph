"""Unit tests for ChronoGraphIngestionPipeline using mocked responses."""

from datetime import datetime, timezone
from unittest.mock import MagicMock
import pytest

from app.engine.store import ChronoGraphStore
from app.services.ingestion_pipeline import (
    ChronoGraphIngestionPipeline,
    query_structured_answer,
)
from app.services.hydradb_types import (
    HydraChunkEvidence,
    HydraQueryResult,
    HydraTripletRelation,
)


@pytest.fixture
def mock_service():
    service = MagicMock()
    service.ingest_memory.return_value = []
    return service


def test_pipeline_controlled_scenario_with_mocked_query_res(mock_service):
    """Tests full pipeline orchestration: Observations -> Candidates -> Supersession -> Temporal Queries."""
    t_jan10 = datetime(2025, 1, 10, 0, 0, 0, tzinfo=timezone.utc)
    t_feb10 = datetime(2025, 2, 10, 0, 0, 0, tzinfo=timezone.utc)
    t_mar10 = datetime(2025, 3, 10, 0, 0, 0, tzinfo=timezone.utc)

    # 1. Chunks
    c1 = HydraChunkEvidence(
        id="mem_ed_1", chunk_uuid="uuid_ed_1", chunk_content="I use VS Code as my favorite editor.",
        relevancy_score=0.95, additional_metadata={"session_id": "s1", "timestamp": "2025-01-10T00:00:00Z"}
    )
    c2 = HydraChunkEvidence(
        id="mem_ed_2", chunk_uuid="uuid_ed_2", chunk_content="I switched to Cursor and now prefer Cursor over VS Code.",
        relevancy_score=0.95, additional_metadata={"session_id": "s2", "timestamp": "2025-02-10T00:00:00Z"}
    )
    c3 = HydraChunkEvidence(
        id="mem_ed_3", chunk_uuid="uuid_ed_3", chunk_content="I switched back to VS Code. It is my favorite editor again.",
        relevancy_score=0.95, additional_metadata={"session_id": "s3", "timestamp": "2025-03-10T00:00:00Z"}
    )

    # 2. Triplets
    tr1 = HydraTripletRelation(
        source_entity_name="user", source_entity_type="PERSON", raw_predicate="favorite editor",
        canonical_predicate="favorite_editor", target_entity_name="VS Code", target_entity_type="PRODUCT",
        temporal_details="2025-01-10T00:00:00Z", chunk_id="mem_ed_1"
    )
    tr2 = HydraTripletRelation(
        source_entity_name="user", source_entity_type="PERSON", raw_predicate="switched to",
        canonical_predicate="favorite_editor", target_entity_name="Cursor", target_entity_type="PRODUCT",
        temporal_details="2025-02-10T00:00:00Z", chunk_id="mem_ed_2"
    )
    tr3 = HydraTripletRelation(
        source_entity_name="user", source_entity_type="PERSON", raw_predicate="favorite editor again",
        canonical_predicate="favorite_editor", target_entity_name="VS Code", target_entity_type="PRODUCT",
        temporal_details="2025-03-10T00:00:00Z", chunk_id="mem_ed_3"
    )

    query_res = HydraQueryResult(
        database="test_db",
        collection="chronograph_phase3c",
        chunks=[c1, c2, c3],
        triplets=[tr1, tr2, tr3],
    )
    mock_service.query_memory.return_value = query_res

    pipeline = ChronoGraphIngestionPipeline(service=mock_service)
    store, observations, active_beliefs = pipeline.build_graph_from_query_result(query_res)

    assert len(observations) == 3
    assert len(active_beliefs) == 3

    # 3. Query A: 2025-01-20 -> VS Code
    ans_a = query_structured_answer(store, "user", "favorite_editor", datetime(2025, 1, 20, tzinfo=timezone.utc))
    assert ans_a["status"] == "SUPPORTED"
    assert ans_a["value"] == "VS Code"

    # 4. Query B: 2025-02-20 -> Cursor
    ans_b = query_structured_answer(store, "user", "favorite_editor", datetime(2025, 2, 20, tzinfo=timezone.utc))
    assert ans_b["status"] == "SUPPORTED"
    assert ans_b["value"] == "Cursor"

    # 5. Query C: 2025-03-20 -> VS Code
    ans_c = query_structured_answer(store, "user", "favorite_editor", datetime(2025, 3, 20, tzinfo=timezone.utc))
    assert ans_c["status"] == "SUPPORTED"
    assert ans_c["value"] == "VS Code"

    # 6. UNKNOWN query: favorite_language -> UNKNOWN, confidence 0.0
    ans_unk = query_structured_answer(store, "user", "favorite_language", datetime(2025, 3, 20, tzinfo=timezone.utc))
    assert ans_unk["status"] == "UNKNOWN"
    assert ans_unk["confidence"] == 0.0
    assert ans_unk["value"] is None

    # 7. Lineage verification
    lineage = ans_c["lineage"]
    assert len(lineage) == 3
    b_ids = [item["belief"].object_value for item in lineage]
    assert b_ids == ["VS Code", "Cursor", "VS Code"]

    # 8. Evidence preservation
    evidence = ans_c["evidence"]
    assert len(evidence) == 1
    assert "VS Code" in evidence[0]["text"]
