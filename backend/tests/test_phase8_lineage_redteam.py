"""Phase 8 Lineage Stack & Graph Traversal Red-Team Audit Suite."""

from datetime import datetime, timezone
import pytest

from app.api.dependencies import reset_store
from app.engine.store import ChronoGraphStore
from app.engine.temporal_resolver import get_lineage
from app.models.domain import BeliefState, EdgeType, GraphEdge, LifecycleStatus


def test_redteam_lineage_cyclic_graph_deadlock_prevention():
    """Attack 1: Traversal over a cyclic graph structure (A -> B -> C -> A) MUST terminate safely without infinite recursion or stack overflow."""
    store = reset_store()
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)

    bA = store.add_belief(BeliefState(id="bA", subject_id="u", predicate="p", object_value="A", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1))
    bB = store.add_belief(BeliefState(id="bB", subject_id="u", predicate="p", object_value="B", lifecycle_status=LifecycleStatus.SUPERSEDED, confidence=0.9, observed_at=t1, valid_from=t1, version=1))
    bC = store.add_belief(BeliefState(id="bC", subject_id="u", predicate="p", object_value="C", lifecycle_status=LifecycleStatus.SUPERSEDED, confidence=0.9, observed_at=t1, valid_from=t1, version=1))

    # Cyclic edges: bA supersedes bB, bB supersedes bC, bC supersedes bA (cycle!)
    store.add_edge(GraphEdge(id="e1", source_id="bA", target_id="bB", edge_type=EdgeType.SUPERSEDES, created_at=t1))
    store.add_edge(GraphEdge(id="e2", source_id="bB", target_id="bC", edge_type=EdgeType.SUPERSEDES, created_at=t1))
    store.add_edge(GraphEdge(id="e3", source_id="bC", target_id="bA", edge_type=EdgeType.SUPERSEDES, created_at=t1))

    lineage = get_lineage(store, "bA")

    # Cycle-safety check: Traversal terminates with exactly 3 unique visited nodes
    assert lineage["root_belief_id"] == "bA"
    assert len(lineage["history"]) == 3
    visited_ids = [h["belief"].id for h in lineage["history"]]
    assert set(visited_ids) == {"bA", "bB", "bC"}


def test_redteam_lineage_missing_target_node():
    """Attack 2: Edge referencing a non-existent target ID degrades gracefully without crashing."""
    store = reset_store()
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)

    b1 = store.add_belief(BeliefState(id="b1", subject_id="u", predicate="p", object_value="A", lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t1, valid_from=t1, version=1))
    store.add_edge(GraphEdge(id="e1", source_id="b1", target_id="missing_belief_id_999", edge_type=EdgeType.SUPERSEDES, created_at=t1))

    lineage = get_lineage(store, "b1")
    assert lineage["root_belief_id"] == "b1"
    assert len(lineage["history"]) == 1
    assert lineage["history"][0]["belief"].id == "b1"


def test_redteam_lineage_contradicts_edge_not_confused_for_supersession():
    """Attack 3: CONTRADICTS edges are NOT traversed as supersession lineage."""
    store = reset_store()
    t1 = datetime(2025, 1, 1, tzinfo=timezone.utc)

    b1 = store.add_belief(BeliefState(id="b1", subject_id="u", predicate="p", object_value="Delhi", lifecycle_status=LifecycleStatus.CONFLICTED, confidence=0.5, observed_at=t1, valid_from=t1, version=1))
    b2 = store.add_belief(BeliefState(id="b2", subject_id="u", predicate="p", object_value="Bangalore", lifecycle_status=LifecycleStatus.CONFLICTED, confidence=0.5, observed_at=t1, valid_from=t1, version=1))

    # CONTRADICTS edge
    store.add_edge(GraphEdge(id="e_con", source_id="b1", target_id="b2", edge_type=EdgeType.CONTRADICTS, created_at=t1))

    lineage = get_lineage(store, "b1")
    # Only root b1 returned (CONTRADICTS is not supersession lineage!)
    assert len(lineage["history"]) == 1
    assert lineage["history"][0]["belief"].id == "b1"
