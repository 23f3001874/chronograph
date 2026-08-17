"""Tests for domain models and validations in ChronoGraph."""

from datetime import datetime, timezone
import pytest
from pydantic import ValidationError

from app.models.domain import (
    BeliefState,
    EdgeType,
    Entity,
    GraphEdge,
    LifecycleStatus,
    Observation,
)


def test_entity_creation():
    user = Entity(id="ent_user", name="Alex", entity_type="PERSON")
    assert user.id == "ent_user"
    assert user.name == "Alex"
    assert user.entity_type == "PERSON"


def test_observation_creation():
    now = datetime.now(timezone.utc)
    obs = Observation(
        id="obs_s1",
        source_text="I live in Delhi.",
        session_id="session_1",
        observed_at=now,
        hydradb_chunk_id="chunk_101",
    )
    assert obs.id == "obs_s1"
    assert obs.source_text == "I live in Delhi."
    assert obs.hydradb_chunk_id == "chunk_101"


def test_belief_state_valid_creation():
    now = datetime.now(timezone.utc)
    belief = BeliefState(
        id="bel_loc_1",
        subject_id="ent_user",
        predicate="lives_in",
        object_value="Delhi",
        lifecycle_status=LifecycleStatus.ACTIVE,
        confidence=0.95,
        observed_at=now,
        valid_from=now,
        valid_until=None,
        version=1,
        observation_ids=["obs_s1"],
    )
    assert belief.id == "bel_loc_1"
    assert belief.object_value == "Delhi"
    assert belief.confidence == 0.95
    assert belief.version == 1
    assert belief.observation_ids == ["obs_s1"]


def test_confidence_validation():
    now = datetime.now(timezone.utc)
    # Test confidence > 1.0
    with pytest.raises(ValidationError):
        BeliefState(
            id="bel_bad",
            subject_id="user",
            predicate="lives_in",
            object_value="Delhi",
            lifecycle_status=LifecycleStatus.ACTIVE,
            confidence=1.5,  # Invalid
            observed_at=now,
            valid_from=now,
            version=1,
        )

    # Test confidence < 0.0
    with pytest.raises(ValidationError):
        BeliefState(
            id="bel_bad2",
            subject_id="user",
            predicate="lives_in",
            object_value="Delhi",
            lifecycle_status=LifecycleStatus.ACTIVE,
            confidence=-0.1,  # Invalid
            observed_at=now,
            valid_from=now,
            version=1,
        )


def test_version_validation():
    now = datetime.now(timezone.utc)
    with pytest.raises(ValidationError):
        BeliefState(
            id="bel_bad_ver",
            subject_id="user",
            predicate="lives_in",
            object_value="Delhi",
            lifecycle_status=LifecycleStatus.ACTIVE,
            confidence=0.9,
            observed_at=now,
            valid_from=now,
            version=0,  # Invalid, must be >= 1
        )


def test_object_presence_validation():
    now = datetime.now(timezone.utc)
    # Neither object_id nor object_value provided
    with pytest.raises(ValidationError) as exc_info:
        BeliefState(
            id="bel_no_obj",
            subject_id="user",
            predicate="lives_in",
            object_id=None,
            object_value=None,
            lifecycle_status=LifecycleStatus.ACTIVE,
            confidence=0.9,
            observed_at=now,
            valid_from=now,
            version=1,
        )
    assert "at least one of object_id or object_value" in str(exc_info.value)


def test_temporal_range_validation():
    t_start = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t_invalid_end = datetime(2024, 12, 31, tzinfo=timezone.utc)

    with pytest.raises(ValidationError) as exc_info:
        BeliefState(
            id="bel_bad_range",
            subject_id="user",
            predicate="lives_in",
            object_value="Delhi",
            lifecycle_status=LifecycleStatus.ACTIVE,
            confidence=0.9,
            observed_at=t_start,
            valid_from=t_start,
            valid_until=t_invalid_end,  # Invalid: end < start
            version=1,
        )
    assert "greater than or equal to valid_from" in str(exc_info.value)


def test_graph_edge_creation():
    now = datetime.now(timezone.utc)
    edge = GraphEdge(
        id="edge_1",
        source_id="bel_loc_2",
        target_id="bel_loc_1",
        edge_type=EdgeType.SUPERSEDES,
        created_at=now,
        metadata={"reason": "location_changed"},
    )
    assert edge.id == "edge_1"
    assert edge.edge_type == EdgeType.SUPERSEDES
    assert edge.metadata["reason"] == "location_changed"
