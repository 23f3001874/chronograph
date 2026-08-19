"""Phase 8 Concurrency & Multithreading Red-Team Audit Suite."""

from datetime import datetime, timezone
import threading
import pytest

from app.engine.store import ChronoGraphStore
from app.models.domain import BeliefState, EdgeType, Entity, GraphEdge, LifecycleStatus, Observation


def test_redteam_concurrency_heavy_multithreaded_mutations():
    """Attack 1: 10 parallel threads executing 100 simultaneous additions each to ChronoGraphStore."""
    store = ChronoGraphStore()

    def worker(thread_idx: int):
        for i in range(100):
            t = datetime.now(timezone.utc)
            ent_id = f"ent_{thread_idx}_{i}"
            obs_id = f"obs_{thread_idx}_{i}"
            bel_id = f"bel_{thread_idx}_{i}"

            store.add_entity(Entity(id=ent_id, name=f"Entity_{i}", entity_type="ITEM"))
            store.add_observation(Observation(id=obs_id, source_text=f"Obs {i}", session_id="s1", observed_at=t))
            store.add_belief(
                BeliefState(
                    id=bel_id, subject_id=f"user_{thread_idx}", predicate="item", object_value=f"val_{i}",
                    lifecycle_status=LifecycleStatus.ACTIVE, confidence=0.9, observed_at=t, valid_from=t, version=1, observation_ids=[obs_id]
                )
            )
            store.add_edge(GraphEdge(id=f"e_{thread_idx}_{i}", source_id=bel_id, target_id=obs_id, edge_type=EdgeType.GROUNDED_IN, created_at=t))

    threads = [threading.Thread(target=worker, args=(t_id,)) for t_id in range(10)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()

    assert len(store.entities) == 1000
    assert len(store.observations) == 1000
    assert len(store.beliefs) == 1000
    assert len(store.edges) == 1000
