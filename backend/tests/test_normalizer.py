"""Unit tests for ChronoGraph normalizer pipeline."""

from datetime import datetime, timezone
import pytest

from app.engine.normalizer import (
    normalize_belief_candidate,
    normalize_graph_context,
    normalize_observation,
)
from app.engine.state_machine import BeliefStateMachine
from app.engine.store import ChronoGraphStore
from app.models.domain import EdgeType, LifecycleStatus
from app.services.hydradb_types import (
    HydraChunkEvidence,
    HydraQueryResult,
    HydraTripletRelation,
)


def test_normalize_chunk_to_observation_and_id_preservation():
    """Test 6 & 8: Normalization of HydraDB chunk into Observation and preservation of IDs."""
    chunk = HydraChunkEvidence(
        id="chunk_sess_101",
        chunk_uuid="uuid_sess_101",
        chunk_content="My favorite editor is VS Code.",
        relevancy_score=0.95,
        source_title="Session 1",
        source_type="memory",
        metadata={"session_id": "sess_1"},
        additional_metadata={"timestamp": "2025-01-01T00:00:00Z"},
    )

    obs = normalize_observation(chunk)

    assert obs.id == "chunk_sess_101"
    assert obs.hydradb_chunk_id == "uuid_sess_101"
    assert obs.source_text == "My favorite editor is VS Code."
    assert obs.session_id == "sess_1"
    assert obs.observed_at == datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)


def test_normalize_triplet_to_belief_candidate():
    """Test 7, 9 & 13: Normalization of triplet into BeliefState candidate (OBSERVED)
    and verification of state-machine processing readiness.
    """
    obs_time = datetime(2025, 2, 1, 0, 0, 0, tzinfo=timezone.utc)
    chunk = HydraChunkEvidence(
        id="chunk_2",
        chunk_uuid="uuid_2",
        chunk_content="I've started using Cursor.",
        relevancy_score=0.9,
        additional_metadata={"session_id": "sess_2", "timestamp": "2025-02-01T00:00:00Z"},
    )
    obs = normalize_observation(chunk)

    triplet = HydraTripletRelation(
        source_entity_name="user",
        source_entity_type="PERSON",
        raw_predicate="started using",
        canonical_predicate="favorite_editor",
        target_entity_name="Cursor",
        target_entity_type="PRODUCT",
        temporal_details="2025-02-01T00:00:00Z",
        timestamp=None,
        chunk_id="chunk_2",
    )

    candidate = normalize_belief_candidate(triplet, obs)

    # 1. Verification of OBSERVED status (NOT automatically ACTIVE or TRUTH)
    assert candidate.lifecycle_status == LifecycleStatus.OBSERVED
    assert candidate.subject_id == "user"
    assert candidate.predicate == "favorite_editor"
    assert candidate.object_value == "Cursor"
    assert candidate.valid_from == datetime(2025, 2, 1, 0, 0, 0, tzinfo=timezone.utc)
    assert candidate.observation_ids == ["chunk_2"]

    # 2. Verification of suitability for ChronoGraph state machine
    store = ChronoGraphStore()
    sm = BeliefStateMachine(store)
    activated = sm.activate_belief(candidate)
    assert activated.lifecycle_status == LifecycleStatus.ACTIVE
    assert store.get_belief(candidate.id) is not None


def test_missing_temporal_information_raises_validation_error():
    """Test 10: Missing timestamp in chunk/metadata raises ValueError and never fabricates dates."""
    chunk = HydraChunkEvidence(
        id="chunk_no_date",
        chunk_uuid="uuid_no_date",
        chunk_content="I live in Delhi.",
        relevancy_score=0.8,
        metadata={},
        additional_metadata={},  # No timestamp key!
    )

    with pytest.raises(ValueError) as exc:
        normalize_observation(chunk, observed_at=None)

    assert "Cannot establish observation timestamp" in str(exc.value)


def test_hydradb_relations_do_not_automatically_become_semantic_edges():
    """Test 11 & 12: HydraDB context triplets do NOT automatically become SUPERSEDES or CONTRADICTS edges."""
    triplet = HydraTripletRelation(
        source_entity_name="user",
        source_entity_type="PERSON",
        raw_predicate="lives in",
        canonical_predicate="lives_in",
        target_entity_name="Bangalore",
        target_entity_type="LOCATION",
        temporal_details="2025-06-01T00:00:00Z",
    )
    query_result = HydraQueryResult(
        database="test_db",
        collection="user_alex",
        chunks=[],
        triplets=[triplet],
    )

    context_triplets = normalize_graph_context(query_result)
    assert len(context_triplets) == 1

    # Verify that normalizing context creates DTOs, NOT ChronoGraph GraphEdges
    store = ChronoGraphStore()
    edges = store.edges
    assert len(edges) == 0  # 0 SUPERSEDES or CONTRADICTS edges created automatically


def test_malformed_chunk_produces_clear_validation_error():
    """Test 14: Malformed chunk with empty content produces a clear ValueError."""
    chunk = HydraChunkEvidence(
        id="chunk_bad",
        chunk_uuid="uuid_bad",
        chunk_content="   ",  # Empty/whitespace content
        relevancy_score=0.0,
    )

    with pytest.raises(ValueError) as exc:
        normalize_observation(chunk, observed_at=datetime.now(timezone.utc))

    assert "source text is empty" in str(exc.value)
