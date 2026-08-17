# CHRONOGRAPH PERSISTENCE & PRODUCTION HARDENING SPECIFICATION

This document describes the atomic snapshot persistence architecture, store restoration, concurrency protection, and API hardening implemented in Phase 6.

---

## 1. Persistence Architecture

```text
[FastAPI Ingestion / Mutations]
               │
               ▼
[Process-Local ChronoGraphStore (RLock Thread-Safe)]
               │
               ▼  (SnapshotManager.save_snapshot)
[Atomic Write: Write to tempfile -> os.replace()]
               │
               ▼
[Disk Snapshot: chronograph/data/chronograph_snapshot.json]
               │
               ▼  (FastAPI Lifespan Startup / load_snapshot)
[Restored ChronoGraphStore & Rebuilt Indexes]
```

---

## 2. Atomic Snapshot Pattern
- **Temporary Write & Replace**: The `SnapshotManager` serializes `entities`, `observations`, `beliefs`, and `edges` into JSON. It writes to a temporary file (`snap_*.tmp`) in the same directory, flushes and syncs to disk (`os.fsync`), and atomically replaces the target snapshot file via `os.replace`.
- **Zero Partial Writes**: If the process crashes or power is lost during write, the target snapshot file remains 100% intact and uncorrupted.

---

## 3. Concurrency Protection
- `ChronoGraphStore` incorporates a re-entrant thread lock (`threading.RLock`).
- All mutation operations (`add_entity`, `add_observation`, `add_belief`, `add_edge`) and lookup operations (`get_beliefs`, `get_active_beliefs`, `get_edges_for_belief`) execute within `with self._lock:` blocks.

---

## 4. API Hardening Changes
- **Lifespan Startup Restoration**: On application startup, FastAPI's `lifespan` handler automatically invokes `restore_from_snapshot()`, populating the in-memory graph from the disk snapshot.
- **Lifespan Shutdown Persistence**: On graceful application shutdown, FastAPI automatically persists the current store to disk.
- **Production CORS Configuration**: `ALLOWED_ORIGINS` environment variable allows comma-separated domain filtering, defaulting to `["*"]` for local development.

---

## 5. Restart & Recovery Guarantee

| Domain Property | Survival Verification |
| :--- | :---: |
| Entity IDs, Names, Types | **100% Preserved** |
| Observation Text, Timestamps, Chunk UUIDs | **100% Preserved** |
| Belief States, Validity Ranges (`valid_from`, `valid_until`) | **100% Preserved** |
| Lifecycle Statuses (`ACTIVE`, `SUPERSEDED`, `CONFLICTED`, `CANCELLED`) | **100% Preserved** |
| Graph Relationship Edges (`SUPERSEDES`, `INVALIDATES`, `CONTRADICTS`) | **100% Preserved** |
| Index Reconstruction (`subject_predicate_index`) | **Rebuilt 100%** |
| Temporal Resolver & Lineage Stack Queries | **100% Identical Output** |
