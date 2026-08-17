"""Integration smoke test for live HydraDB Cloud API.

Skipped automatically unless CHRONOGRAPH_LIVE_HYDRADB_TEST=1 is set in the environment.
"""

from datetime import datetime, timezone
import os
import time
import pytest

from app.engine.normalizer import normalize_observation
from app.services.hydradb_service import HydraDBService

LIVE_TEST_ENABLED = os.environ.get("CHRONOGRAPH_LIVE_HYDRADB_TEST") == "1"


@pytest.mark.skipif(not LIVE_TEST_ENABLED, reason="Live HydraDB API test disabled by default. Set CHRONOGRAPH_LIVE_HYDRADB_TEST=1 to enable.")
def test_live_hydradb_integration_smoke():
    """Live smoke test verifying ingest, query, normalization, and delete against HydraDB Cloud."""
    service = HydraDBService()
    test_collection = f"smoke_test_{int(time.time())}"
    mem_id = f"smoke_mem_{int(time.time())}"
    now_iso = datetime.now(timezone.utc).isoformat()

    # 1. Ingest test memory
    memories = [
        {
            "id": mem_id,
            "text": "Smoke test observation: The user prefers Python for AI engineering.",
            "infer": True,
            "additional_metadata": {"session_id": "smoke_s1", "timestamp": now_iso},
        }
    ]

    ingest_res = service.ingest_memory(collection=test_collection, memories=memories)
    assert len(ingest_res) == 1
    assert ingest_res[0].id == mem_id

    # Allow brief indexing propagation
    time.sleep(2.0)

    # 2. Query collection
    query_res = service.query_memory(
        collection=test_collection,
        query="What language does the user prefer?",
        mode="fast",
        max_results=5,
    )

    assert query_res.collection == test_collection
    assert len(query_res.chunks) > 0

    # 3. Normalize result chunk into Observation
    chunk = query_res.chunks[0]
    obs = normalize_observation(chunk, fallback_session_id="smoke_s1", fallback_observed_at=datetime.now(timezone.utc))

    assert obs.source_text is not None
    assert obs.hydradb_chunk_id is not None

    # 4. Clean up test memory
    service.delete_memory(collection=test_collection, memory_ids=[mem_id])
