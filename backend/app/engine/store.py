"""In-memory data store and index for ChronoGraph.

Provides deterministic storage, indexing, and lookup operations for Entities,
Observations, BeliefStates, and GraphEdges with thread-safe concurrency locks.
"""

import threading
from app.models.domain import (
    BeliefState,
    Entity,
    GraphEdge,
    LifecycleStatus,
    Observation,
)


class ChronoGraphStore:
    """In-memory graph store maintaining domain objects, indexes, and thread locks."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self.entities: dict[str, Entity] = {}
        self.beliefs: dict[str, BeliefState] = {}
        self.observations: dict[str, Observation] = {}
        self.edges: dict[str, GraphEdge] = {}

        # Index: (subject_id, predicate) -> list of belief IDs
        self.subject_predicate_index: dict[tuple[str, str], list[str]] = {}

    def add_entity(self, entity: Entity) -> Entity:
        """Stores an Entity thread-safely and returns it."""
        with self._lock:
            self.entities[entity.id] = entity
            return entity

    def get_entity(self, entity_id: str) -> Entity | None:
        """Retrieves an Entity by ID thread-safely, returning None if absent."""
        with self._lock:
            return self.entities.get(entity_id)

    def add_observation(self, observation: Observation) -> Observation:
        """Stores an Observation thread-safely and returns it."""
        with self._lock:
            self.observations[observation.id] = observation
            return observation

    def get_observation(self, observation_id: str) -> Observation | None:
        """Retrieves an Observation by ID thread-safely, returning None if absent."""
        with self._lock:
            return self.observations.get(observation_id)

    def add_belief(self, belief: BeliefState) -> BeliefState:
        """Stores a BeliefState thread-safely and indexes it by (subject_id, predicate).

        Note: The store only validates and indexes; it does NOT mutate lifecycle status.
        """
        with self._lock:
            self.beliefs[belief.id] = belief

            key = (belief.subject_id, belief.predicate)
            if key not in self.subject_predicate_index:
                self.subject_predicate_index[key] = []
            if belief.id not in self.subject_predicate_index[key]:
                self.subject_predicate_index[key].append(belief.id)

            return belief

    def get_belief(self, belief_id: str) -> BeliefState | None:
        """Retrieves a BeliefState by ID thread-safely, returning None if absent."""
        with self._lock:
            return self.beliefs.get(belief_id)

    def add_edge(self, edge: GraphEdge) -> GraphEdge:
        """Stores a GraphEdge thread-safely and returns it."""
        with self._lock:
            self.edges[edge.id] = edge
            return edge

    def get_edges_for_belief(self, belief_id: str) -> list[GraphEdge]:
        """Returns all GraphEdges connected to the specified belief (as source or target)."""
        with self._lock:
            return [
                edge
                for edge in self.edges.values()
                if edge.source_id == belief_id or edge.target_id == belief_id
            ]

    def get_beliefs(self, subject_id: str, predicate: str) -> list[BeliefState]:
        """Returns all stored BeliefStates for a given (subject_id, predicate) pair."""
        with self._lock:
            key = (subject_id, predicate)
            belief_ids = self.subject_predicate_index.get(key, [])
            return [self.beliefs[bid] for bid in belief_ids if bid in self.beliefs]

    def get_active_beliefs(self, subject_id: str, predicate: str) -> list[BeliefState]:
        """Returns all BeliefStates with lifecycle_status ACTIVE for a (subject_id, predicate) pair."""
        with self._lock:
            all_beliefs = self.get_beliefs(subject_id, predicate)
            return [b for b in all_beliefs if b.lifecycle_status == LifecycleStatus.ACTIVE]
