"""Tests for ChronoGraphStore indexing, retrieval, and relationship store."""

from datetime import datetime, timezone
import pytest

from app.engine.store import ChronoGraphStore
from app.models.domain import (
    BeliefState,
    EdgeType,
    Entity,
    GraphEdge,
    LifecycleStatus,
    Observation,
)


@pytest.fixture
def store():
    return ChronoGraphStore()


def test_entity_indexing(store):
    user = Entity(id="ent_user", name="Alex", entity_type="PERSON")
    store.add_entity(user)
    assert store.get_entity("ent_user") == user
    assert store.get_entity("non_existent") is None


def test_observation_indexing(store):
    now = datetime.now(timezone.utc)
    obs = Observation(
        id="obs_s1",
        source_text="I live in Delhi.",
        session_id="session_1",
        observed_at=now,
    )
    store.add_observation(obs)
    assert store.get_observation("obs_s1") == obs
    assert store.get_observation("non_existent") is None


def test_belief_indexing_and_active_retrieval(store):
    now = datetime.now(timezone.utc)
    b1 = BeliefState(
        id="b1",
        subject_id="ent_user",
        predicate="lives_in",
        object_value="Delhi",
        lifecycle_status=LifecycleStatus.SUPERSEDES if hasattr(LifecycleStatus, 'SUPERSEDES') else LifecycleStatus.SUPERSEDED,
        confidence=0.9,
        observed_at=now,
        valid_from=now,
        version=1,
    )
    b2 = BeliefState(
        id="b2",
        subject_id="ent_user",
        predicate="lives_in",
        object_value="Delhi",
        lifecycle_status=LifecycleStatus.ACTIVE,
        confidence=0.95,
        observed_at=now,
        valid_from=now,
        version=2,
    )

    store.add_belief(b1)
    store.add_belief(b2)

    all_beliefs = store.get_beliefs("ent_user", "lives_in")
    assert len(all_beliefs) == 2
    assert set(b.id for b in all_beliefs) == {"b1", "b2"}

    active_beliefs = store.get_active_beliefs("ent_user", "lives_in")
    assert len(active_beliefs) == 1
    assert active_beliefs[0].id == "b2"


def test_store_does_not_mutate_lifecycle_status(store):
    """Verifies that adding a new belief does NOT automatically mutate existing beliefs."""
    now = datetime.now(timezone.utc)
    b1 = BeliefState(
        id="b1",
        subject_id="ent_user",
        predicate="lives_in",
        object_value="Delhi",
        lifecycle_status=LifecycleStatus.ACTIVE,
        confidence=0.9,
        observed_at=now,
        valid_from=now,
        version=1,
    )
    store.add_belief(b1)

    # Add a second active belief for same subject+predicate
    b2 = BeliefState(
        id="b2",
        subject_id="ent_user",
        predicate="lives_in",
        object_value="Bangalore",
        lifecycle_status=LifecycleStatus.ACTIVE,
        confidence=0.9,
        observed_at=now,
        valid_from=now,
        version=2,
    )
    store.add_belief(b2)

    # Verify b1 was NOT mutated to SUPERSEDES / SUPERSEDED by the store
    stored_b1 = store.get_belief("b1")
    assert stored_b1.lifecycle_status == LifecycleStatus.ACTIVE


def test_delhi_bangalore_scenario(store):
    """Test Scenario 1: Delhi / Bangalore location observations and explicit edges."""
    t1 = datetime(2025, 5, 1, tzinfo=timezone.utc)
    t2 = datetime(2025, 6, 1, tzinfo=timezone.utc)
    t3 = datetime(2025, 7, 1, tzinfo=timezone.utc)
    t4 = datetime(2025, 8, 1, tzinfo=timezone.utc)

    # 1. Observations
    obs1 = store.add_observation(
        Observation(id="obs_s1", source_text="I live in Delhi.", session_id="s1", observed_at=t1)
    )
    obs2 = store.add_observation(
        Observation(id="obs_s2", source_text="I'm planning to move to Bangalore.", session_id="s2", observed_at=t2)
    )
    obs3 = store.add_observation(
        Observation(id="obs_s3", source_text="The Bangalore move was cancelled.", session_id="s3", observed_at=t3)
    )
    obs4 = store.add_observation(
        Observation(id="obs_s4", source_text="I'll remain in Delhi.", session_id="s4", observed_at=t4)
    )

    # 2. Beliefs
    b1 = store.add_belief(
        BeliefState(
            id="b1_delhi",
            subject_id="user",
            predicate="lives_in",
            object_value="Delhi",
            lifecycle_status=LifecycleStatus.SUPERSEDED,
            confidence=0.9,
            observed_at=t1,
            valid_from=t1,
            valid_until=t2,
            version=1,
            observation_ids=[obs1.id],
        )
    )
    b2 = store.add_belief(
        BeliefState(
            id="b2_bangalore_plan",
            subject_id="user",
            predicate="planned_move",
            object_value="Bangalore",
            lifecycle_status=LifecycleStatus.CANCELLED,
            confidence=0.85,
            observed_at=t2,
            valid_from=t2,
            valid_until=t3,
            version=1,
            observation_ids=[obs2.id],
        )
    )
    b3 = store.add_belief(
        BeliefState(
            id="b3_cancel_move",
            subject_id="user",
            predicate="move_cancellation",
            object_value="Bangalore",
            lifecycle_status=LifecycleStatus.SUPERSEDED,
            confidence=0.95,
            observed_at=t3,
            valid_from=t3,
            valid_until=t4,
            version=1,
            observation_ids=[obs3.id],
        )
    )
    b4 = store.add_belief(
        BeliefState(
            id="b4_remain_delhi",
            subject_id="user",
            predicate="lives_in",
            object_value="Delhi",
            lifecycle_status=LifecycleStatus.ACTIVE,
            confidence=0.95,
            observed_at=t4,
            valid_from=t4,
            valid_until=None,
            version=2,
            observation_ids=[obs4.id],
        )
    )

    # 3. Edges
    edge_ground1 = store.add_edge(
        GraphEdge(id="e_g1", source_id=b1.id, target_id=obs1.id, edge_type=EdgeType.GROUNDED_IN, created_at=t1)
    )
    edge_invalidates = store.add_edge(
        GraphEdge(id="e_inv", source_id=b3.id, target_id=b2.id, edge_type=EdgeType.INVALIDATES, created_at=t3)
    )
    edge_supersedes = store.add_edge(
        GraphEdge(id="e_sup", source_id=b4.id, target_id=b3.id, edge_type=EdgeType.SUPERSEDES, created_at=t4)
    )

    # Assertions
    assert store.get_belief("b1_delhi") is not None
    assert store.get_belief("b4_remain_delhi").lifecycle_status == LifecycleStatus.ACTIVE
    
    b2_edges = store.get_edges_for_belief("b2_bangalore_plan")
    assert len(b2_edges) == 1
    assert b2_edges[0].edge_type == EdgeType.INVALIDATES

    b4_edges = store.get_edges_for_belief("b4_remain_delhi")
    assert len(b4_edges) == 1
    assert b4_edges[0].edge_type == EdgeType.SUPERSEDES


def test_editor_sequence_scenario(store):
    """Test Scenario 2: VS Code -> Cursor -> VS Code editor sequence."""
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2025, 2, 1, tzinfo=timezone.utc)
    t3 = datetime(2025, 3, 1, tzinfo=timezone.utc)

    # Observations
    obs1 = store.add_observation(Observation(id="obs_ed1", source_text="My favorite editor is VS Code.", session_id="s1", observed_at=t1))
    obs2 = store.add_observation(Observation(id="obs_ed2", source_text="I've started using Cursor.", session_id="s2", observed_at=t2))
    obs3 = store.add_observation(Observation(id="obs_ed3", source_text="Actually, I'm back to VS Code.", session_id="s3", observed_at=t3))

    # Beliefs
    b1 = store.add_belief(
        BeliefState(
            id="b_ed1", subject_id="user", predicate="favorite_editor", object_value="VS Code",
            lifecycle_status=LifecycleStatus.SUPERSEDED, confidence=0.9, observed_at=t1, valid_from=t1, valid_until=t2, version=1, observation_ids=[obs1.id]
        )
    )
    b2 = store.add_belief(
        BeliefState(
            id="b_ed2", subject_id="user", predicate="favorite_editor", object_value="Cursor",
            lifecycle_status=LifecycleStatus.SUPERSEDED, confidence=0.9, observed_at=t2, valid_from=t2, valid_until=t3, version=1, observation_ids=[obs2.id]
        )
    )
    b3 = store.add_belief(
        BeliefState(
            id="b_ed3", subject_id="user", predicate="favorite_editor", object_value="VS Code",
            lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.95, observed_at=t3, valid_from=t3, valid_until=None, version=2, observation_ids=[obs3.id]
        )
    )

    # Supersession Edges
    store.add_edge(GraphEdge(id="e_ed_sup1", source_id=b2.id, target_id=b1.id, edge_type=EdgeType.SUPERSEDES, created_at=t2))
    store.add_edge(GraphEdge(id="e_ed_sup2", source_id=b3.id, target_id=b2.id, edge_type=EdgeType.SUPERSEDES, created_at=t3))

    # Grounding Edges
    store.add_edge(GraphEdge(id="e_g_ed1", source_id=b1.id, target_id=obs1.id, edge_type=EdgeType.GROUNDED_IN, created_at=t1))
    store.add_edge(GraphEdge(id="e_g_ed2", source_id=b2.id, target_id=obs2.id, edge_type=EdgeType.GROUNDED_IN, created_at=t2))
    store.add_edge(GraphEdge(id="e_g_ed3", source_id=b3.id, target_id=obs3.id, edge_type=EdgeType.GROUNDED_IN, created_at=t3))

    # Index Verification
    editor_beliefs = store.get_beliefs("user", "favorite_editor")
    assert len(editor_beliefs) == 3
    assert set(b.id for b in editor_beliefs) == {"b_ed1", "b_ed2", "b_ed3"}

    active_editors = store.get_active_beliefs("user", "favorite_editor")
    assert len(active_editors) == 1
    assert active_editors[0].id == "b_ed3"
    assert active_editors[0].object_value == "VS Code"

    # Edge Lookup Verification
    b2_edges = store.get_edges_for_belief("b_ed2")
    edge_types = set(e.edge_type for e in b2_edges)
    assert EdgeType.SUPERSEDES in edge_types
    assert EdgeType.GROUNDED_IN in edge_types
