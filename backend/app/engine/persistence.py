"""Persistence and atomic snapshot management for ChronoGraph.

Provides JSON serialization, deserialization, atomic file writes (via tempfile + os.replace),
and store restoration for Entities, Observations, BeliefStates, and GraphEdges.
"""

from datetime import datetime, timezone
import json
import logging
import os
import tempfile
from typing import Any

from app.engine.store import ChronoGraphStore
from app.models.domain import (
    BeliefState,
    EdgeType,
    Entity,
    GraphEdge,
    LifecycleStatus,
    Observation,
)

logger = logging.getLogger("chronograph.persistence")

if os.environ.get("VERCEL"):
    DEFAULT_DATA_DIR = os.path.join(tempfile.gettempdir(), "chronograph_data")
else:
    DEFAULT_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")

DEFAULT_SNAPSHOT_PATH = os.path.join(DEFAULT_DATA_DIR, "chronograph_snapshot.json")


def _parse_datetime(dt_val: Any) -> datetime | None:
    """Parses string/timestamp into timezone-aware datetime."""
    if not dt_val:
        return None
    if isinstance(dt_val, datetime):
        if dt_val.tzinfo is None:
            return dt_val.replace(tzinfo=timezone.utc)
        return dt_val
    if isinstance(dt_val, str):
        clean = dt_val.strip()
        if clean.endswith("Z"):
            clean = clean[:-1] + "+00:00"
        dt = datetime.fromisoformat(clean)
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt
    return None


class SnapshotManager:
    """Manages snapshot serialization, deserialization, atomic writes, and restoration."""

    def __init__(self, snapshot_path: str | None = None) -> None:
        self.snapshot_path = snapshot_path or DEFAULT_SNAPSHOT_PATH
        try:
            os.makedirs(os.path.dirname(self.snapshot_path), exist_ok=True)
        except Exception:
            self.snapshot_path = os.path.join(tempfile.gettempdir(), "chronograph_snapshot.json")
            os.makedirs(os.path.dirname(self.snapshot_path), exist_ok=True)

    def serialize_store(self, store: ChronoGraphStore) -> dict[str, Any]:
        """Serializes ChronoGraphStore objects into a JSON-compatible dictionary."""
        entities_data = [e.model_dump(mode="json") for e in store.entities.values()]
        observations_data = [o.model_dump(mode="json") for o in store.observations.values()]
        beliefs_data = [b.model_dump(mode="json") for b in store.beliefs.values()]
        edges_data = [edge.model_dump(mode="json") for edge in store.edges.values()]

        return {
            "version": "1.0",
            "saved_at": datetime.now(timezone.utc).isoformat(),
            "entities": entities_data,
            "observations": observations_data,
            "beliefs": beliefs_data,
            "edges": edges_data,
        }

    def deserialize_store(self, data: dict[str, Any]) -> ChronoGraphStore:
        """Reconstructs a ChronoGraphStore from a snapshot dictionary, rebuilding all indexes."""
        store = ChronoGraphStore()

        # 1. Deserialize Entities
        for e_dict in data.get("entities", []):
            store.add_entity(Entity(**e_dict))

        # 2. Deserialize Observations
        for o_dict in data.get("observations", []):
            if "observed_at" in o_dict:
                o_dict["observed_at"] = _parse_datetime(o_dict["observed_at"])
            store.add_observation(Observation(**o_dict))

        # 3. Deserialize BeliefStates
        for b_dict in data.get("beliefs", []):
            if "observed_at" in b_dict:
                b_dict["observed_at"] = _parse_datetime(b_dict["observed_at"])
            if "valid_from" in b_dict:
                b_dict["valid_from"] = _parse_datetime(b_dict["valid_from"])
            if "valid_until" in b_dict and b_dict["valid_until"] is not None:
                b_dict["valid_until"] = _parse_datetime(b_dict["valid_until"])

            if "lifecycle_status" in b_dict and isinstance(b_dict["lifecycle_status"], str):
                b_dict["lifecycle_status"] = LifecycleStatus(b_dict["lifecycle_status"])

            store.add_belief(BeliefState(**b_dict))

        # 4. Deserialize GraphEdges
        for edge_dict in data.get("edges", []):
            if "created_at" in edge_dict:
                edge_dict["created_at"] = _parse_datetime(edge_dict["created_at"])
            if "edge_type" in edge_dict and isinstance(edge_dict["edge_type"], str):
                edge_dict["edge_type"] = EdgeType(edge_dict["edge_type"])

            store.add_edge(GraphEdge(**edge_dict))

        return store

    def save_snapshot(self, store: ChronoGraphStore, file_path: str | None = None) -> str:
        """Atomically saves the store to a JSON snapshot file (write to tmp, atomic replace)."""
        target_path = file_path or self.snapshot_path
        target_dir = os.path.dirname(target_path)
        os.makedirs(target_dir, exist_ok=True)

        data = self.serialize_store(store)
        json_bytes = json.dumps(data, indent=2).encode("utf-8")

        # Atomic Write Pattern: Write to named temporary file in same directory, then os.replace
        fd, temp_path = tempfile.mkstemp(dir=target_dir, prefix="snap_", suffix=".tmp")
        try:
            with os.fdopen(fd, "wb") as f:
                f.write(json_bytes)
                f.flush()
                os.fsync(f.fileno())

            os.replace(temp_path, target_path)
            logger.info("Successfully saved atomic snapshot to %s", target_path)
            return target_path
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            logger.error("Failed to save atomic snapshot: %s", e)
            raise

    def load_snapshot(self, store: ChronoGraphStore, file_path: str | None = None) -> bool:
        """Loads and restores store contents from a snapshot file if present."""
        target_path = file_path or self.snapshot_path
        if not os.path.exists(target_path):
            logger.info("No snapshot found at %s. Starting with empty store.", target_path)
            return False

        try:
            with open(target_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            restored = self.deserialize_store(data)

            # Copy restored contents into target store atomically under lock
            with store._lock:
                store.entities = restored.entities
                store.observations = restored.observations
                store.beliefs = restored.beliefs
                store.edges = restored.edges
                store.subject_predicate_index = restored.subject_predicate_index

            logger.info("Successfully restored store from %s", target_path)
            return True
        except Exception as e:
            logger.error("Snapshot file at %s is corrupted or invalid: %s", target_path, e)
            raise ValueError(f"Corrupted snapshot file: {e}")
