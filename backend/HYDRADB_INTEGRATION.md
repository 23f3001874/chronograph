# HYDRADB INTEGRATION & NORMALIZATION PIPELINE

This document describes the architecture, service boundaries, normalization rules, and test procedures for integrating HydraDB Cloud (SDK `v2.1.2`) into ChronoGraph.

---

## 1. Architecture

```text
+-----------------------+
|  HydraDB Cloud API   |
+-----------------------+
           │  (SDK v2.1.2)
           ▼
+-----------------------+
|   HydraDBService      |  <-- Service Wrapper (Collection Isolation, DTO Parsing)
+-----------------------+
           │  (HydraQueryResult / HydraChunkEvidence / HydraTripletRelation DTOs)
           ▼
+-----------------------+
|   Normalizer Engine   |  <-- Transforms DTOs into Observations & Belief Candidates (OBSERVED)
+-----------------------+
           │  (Candidate BeliefStates in OBSERVED status)
           ▼
+-----------------------+
| ChronoGraph Store     |  <-- In-Memory Graph Indexing & State Store
| & State Machine       |  <-- Enforces Epistemic Lifecycles (ACTIVE, SUPERSEDED, CANCELLED, CONFLICTED)
+-----------------------+
```

---

## 2. Environment Variables

Configure these variables in your git-ignored `.env` file at `backend/.env`:

| Variable | Required | Description | Example |
| :--- | :---: | :--- | :--- |
| `HYDRA_DB_API_KEY` | **Yes** | HydraDB Cloud API Bearer Token | `sk_live_...` |
| `HYDRA_DB_DATABASE` | **Yes** | Target HydraDB database name | `chronograph_db` |
| `CHRONOGRAPH_LIVE_HYDRADB_TEST` | Optional | Set to `1` to run live integration test | `1` |

---

## 3. `HydraDBService` API

Located at `app/services/hydradb_service.py`:

- **`ingest_memory(*, collection: str, memories: list[dict], infer: bool = True, custom_instructions: str | None = None) -> list[HydraMemoryResultItem]`**  
  Ingests memory items into a collection partition with optional graph inference.
- **`query_memory(*, collection: str, query: str, mode: Literal["fast", "thinking"] = "thinking", max_results: int = 10, graph_context: bool = True, recency_bias: float | None = None) -> HydraQueryResult`**  
  Executes hybrid query over memory chunks and retrieves graph relations.
- **`inspect_memory(*, collection: str, memory_id: str, mode: str | None = None) -> dict`**  
  Inspects raw source text of a memory ID.
- **`get_memory_status(*, collection: str, memory_ids: list[str]) -> list[dict]`**  
  Retrieves indexing pipeline statuses for specified memory IDs.
- **`delete_memory(*, collection: str, memory_ids: list[str]) -> bool`**  
  Deletes specified memory IDs within the collection scope.
- **`get_relations(*, collection: str, memory_id: str, limit: int = 50) -> list[dict]`**  
  Retrieves explicit relations declared for a given memory ID.

---

## 4. Normalizer API

Located at `app/engine/normalizer.py`:

- **`normalize_observation(chunk: HydraChunkEvidence, fallback_session_id: str | None = None, fallback_observed_at: datetime | None = None) -> Observation`**  
  Transforms a retrieved chunk into a domain `Observation`.
- **`normalize_belief_candidate(triplet: HydraTripletRelation, observation: Observation, default_subject_id: str = "user", confidence: float = 0.8) -> BeliefState`**  
  Transforms an extracted triplet into a candidate `BeliefState` in `OBSERVED` status.
- **`normalize_graph_context(query_result: HydraQueryResult) -> list[HydraTripletRelation]`**  
  Extracts context triplets from query results.

---

## 5. HydraDB → Observation Mapping

| HydraDB Field | Observation Field | Handling / Validation Rule |
| :--- | :--- | :--- |
| `chunk.id` / `chunk.chunk_uuid` | `id` | Preserves exact HydraDB chunk identifier. |
| `chunk.chunk_content` | `source_text` | Requires non-empty string. |
| `metadata["session_id"]` | `session_id` | Falls back to `fallback_session_id` or `"unknown_session"`. |
| `metadata["timestamp"]` | `observed_at` | Parses ISO timestamp. **Raises `ValueError` if absent** (no date fabrication!). |
| `chunk.chunk_uuid` | `hydradb_chunk_id` | Stores unique HydraDB chunk UUID for evidence traceability. |

---

## 6. HydraDB → BeliefCandidate Mapping

| HydraDB Field | BeliefState Field | Handling / Validation Rule |
| :--- | :--- | :--- |
| `triplet.source_entity_name` | `subject_id` | Lowercased string (defaults to `"user"`). |
| `triplet.canonical_predicate` | `predicate` | Lowercased predicate string. |
| `triplet.target_entity_name` | `object_value` | Target scalar value or entity name. |
| *(Internal Constant)* | `lifecycle_status` | **ALWAYS set to `OBSERVED`**. Never auto-activated as truth! |
| `triplet.temporal_details` | `valid_from` | Parses extracted date. Falls back to `observation.observed_at`. |
| `[observation.id]` | `observation_ids` | Links candidate back to grounding `Observation`. |

---

## 7. Graph Context Mapping

HydraDB's `SearchGraphContext` returns `SearchPathTriplet` objects (`source`, `target`, `relation`). The normalizer parses these into internal `HydraTripletRelation` DTOs containing `source_entity_name`, `canonical_predicate`, `target_entity_name`, and `temporal_details`.

---

## 8. Collection Isolation

All memory methods in `HydraDBService` require callers to explicitly pass `collection=<collection_id>`. Passing an empty or whitespace-only collection string raises a `ValueError`. This enforces strict workspace/user isolation and prevents cross-user memory leakage.

---

## 9. Why HydraDB Relations Are NOT Automatically ChronoGraph Semantic Edges

HydraDB's graph inference extracts entity relations from individual text statements. However, HydraDB has **no global state machine** to determine whether a new statement invalidates, supersedes, or contradicts an older statement.

Therefore:
- HydraDB graph relations are treated strictly as **external evidence candidates**.
- ChronoGraph semantic edges (`SUPERSEDES`, `INVALIDATES`, `CONTRADICTS`) are created **exclusively by ChronoGraph's state machine and contradiction engine**.

---

## 10. Live Smoke Test Instructions

To execute the live integration test against HydraDB Cloud:

1. Ensure `HYDRA_DB_API_KEY` and `HYDRA_DB_DATABASE` are configured in `backend/.env`.
2. Set `CHRONOGRAPH_LIVE_HYDRADB_TEST=1` in your environment.
3. Run pytest:
   ```bash
   $env:CHRONOGRAPH_LIVE_HYDRADB_TEST="1"
   .venv\Scripts\pytest.exe -v tests/test_hydradb_integration_smoke.py
   ```
