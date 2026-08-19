"""Phase 8 Normalizer Engine Red-Team Audit Suite."""

from datetime import datetime, timezone
import pytest

from app.engine.normalizer import (
    normalize_belief_candidate,
    normalize_observation,
)
from app.models.domain import LifecycleStatus
from app.services.hydradb_types import HydraChunkEvidence, HydraTripletRelation


def test_redteam_normalizer_never_invents_timestamp():
    """Attack 1: ChronoGraph normalizer MUST NEVER fabricate a timestamp when metadata timestamp and fallback are absent."""
    chunk = HydraChunkEvidence(
        id="c1",
        chunk_uuid="uuid1",
        chunk_content="I use VS Code.",
        relevancy_score=0.9,
        additional_metadata={},  # No timestamp
    )

    with pytest.raises(ValueError) as exc:
        normalize_observation(chunk, observed_at=None)
    assert "timestamp" in str(exc.value).lower()


def test_redteam_normalizer_empty_chunk_content_fails():
    """Attack 2: Chunk with empty or whitespace-only content raises ValueError."""
    chunk = HydraChunkEvidence(
        id="c2",
        chunk_uuid="uuid2",
        chunk_content="   ",  # Whitespace
        relevancy_score=0.9,
        additional_metadata={"timestamp": "2025-01-10T00:00:00Z"},
    )

    with pytest.raises(ValueError) as exc:
        normalize_observation(chunk)
    assert "empty" in str(exc.value).lower() or "chunk_content" in str(exc.value)


def test_redteam_normalizer_triplet_candidate_always_observed():
    """Attack 3: Candidates produced by normalizer are ALWAYS initialized to OBSERVED status, never automatically ACTIVE truth."""
    obs = normalize_observation(
        HydraChunkEvidence(
            id="c3",
            chunk_uuid="uuid3",
            chunk_content="I use Cursor.",
            relevancy_score=0.9,
            additional_metadata={"timestamp": "2025-01-10T00:00:00Z"},
        )
    )

    triplet = HydraTripletRelation(
        source_entity_name="user",
        source_entity_type="PERSON",
        raw_predicate="favorite editor is",
        canonical_predicate="favorite_editor",
        target_entity_name="Cursor",
        target_entity_type="PRODUCT",
        temporal_details="2025-01-10",
    )

    cand = normalize_belief_candidate(triplet, obs)
    assert cand.lifecycle_status == LifecycleStatus.OBSERVED
    assert cand.subject_id == "user"
    assert cand.predicate == "favorite_editor"
    assert cand.object_value == "Cursor"
    assert cand.observation_ids == [obs.id]
