"""Process-local application state, snapshot integration, and FastAPI dependency providers."""

import os
from app.engine.persistence import SnapshotManager
from app.engine.store import ChronoGraphStore
from app.services.ingestion_pipeline import ChronoGraphIngestionPipeline

_STORE_INSTANCE = ChronoGraphStore()
_PIPELINE_INSTANCE = ChronoGraphIngestionPipeline()
_SNAPSHOT_MANAGER = SnapshotManager()


def get_store() -> ChronoGraphStore:
    """Returns the shared process-local ChronoGraphStore instance."""
    return _STORE_INSTANCE


def get_pipeline() -> ChronoGraphIngestionPipeline:
    """Returns the shared process-local ChronoGraphIngestionPipeline instance."""
    return _PIPELINE_INSTANCE


def get_snapshot_manager() -> SnapshotManager:
    """Returns the SnapshotManager instance."""
    return _SNAPSHOT_MANAGER


def restore_from_snapshot() -> bool:
    """Restores the process-local store from snapshot if available on disk."""
    try:
        return _SNAPSHOT_MANAGER.load_snapshot(_STORE_INSTANCE)
    except Exception as e:
        # Fails gracefully during test/startup if snapshot corrupted
        return False


def save_current_snapshot() -> str:
    """Saves current process-local store to disk snapshot atomically."""
    return _SNAPSHOT_MANAGER.save_snapshot(_STORE_INSTANCE)


def reset_store() -> ChronoGraphStore:
    """Resets the process-local store instance (used by unit tests for isolation)."""
    global _STORE_INSTANCE, _PIPELINE_INSTANCE
    _STORE_INSTANCE = ChronoGraphStore()
    _PIPELINE_INSTANCE = ChronoGraphIngestionPipeline()
    return _STORE_INSTANCE
