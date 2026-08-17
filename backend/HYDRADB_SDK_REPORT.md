# HYDRADB SDK CAPABILITY INSPECTION REPORT

**Package**: `hydradb-sdk`  
**Version**: `2.1.2`  
**Location**: `C:\Users\91877\chronograph\backend\.venv\Lib\site-packages\hydra_db`  
**Inspection Date**: August 17, 2026  

---

## A. Installed Version & Package Structure

- Installed PyPI Package: `hydradb-sdk==2.1.2`
- Root Module: `hydra_db`
- Core Client Classes: `hydra_db.HydraDB` (synchronous), `hydra_db.AsyncHydraDB` (asynchronous)
- Internal Dependencies: `httpx>=0.24`, `pydantic<3,>=1.10`, `typing-extensions`, `anyio`

---

## B. Client Initialization

```python
from hydra_db import HydraDB, AsyncHydraDB

# Constructor Signature
client = HydraDB(
    *,
    token: str,
    base_url: str | None = None,       # Defaults to "https://api.hydradb.com"
    timeout: float | None = None,        # Optional HTTP request timeout in seconds
    httpx_client: httpx.Client | None = None
)
```
- **Network I/O**: None during initialization (`HydraDB()` instantiates internal HTTP client lazily).

---

## C. Authentication

- **Mechanism**: Bearer token header `Authorization: Bearer <HYDRA_DB_API_KEY>`.
- **API Version**: `API-Version: 2` (automatically set by SDK headers).
- **Verification Method**: `client.databases.list()`
  - Signature: `client.databases.list(*, request_options: Optional[RequestOptions] = None)`
  - Network I/O: Synchronous HTTP `GET https://api.hydradb.com/databases`
  - Return Type: `HandlerEnvelopeTenantsTenantIdsResponse` (wrapped envelope with `.data.databases` containing list of database strings).

---

## D. Write API (`client.context.ingest`)

```python
response = client.context.ingest(
    *,
    database: str,
    type: Literal["knowledge", "memory"] | None = "knowledge",
    collection: str | None = None,
    memories: str | None = None,         # JSON-stringified list of memory dicts
    app_knowledge: str | None = None,   # JSON-stringified list of app connector records
    document_metadata: str | None = None,# JSON-stringified list binding source IDs to uploaded files
    documents: FileTypes | None = None,  # Binary file upload tuples
    graph_payload: str | None = None,
    upsert: str | None = "true"
)
```
- **Network I/O**: `POST /context/ingest` (multipart/form-data).
- **Return Type**: `HandlerEnvelopeIngestionV2SourceUploadResponse` containing `.data.results` (list of `IngestionV2SourceUploadResultItem` with `.id`, `.status`, `.error_code`).
- **Memory Item JSON Schema** (passed as string in `memories`):
  ```json
  [
    {
      "id": "mem_001",
      "text": "User prefers VS Code.",
      "infer": true,
      "user_name": "Alex",
      "custom_instructions": "Extract editor preferences",
      "tenant_metadata": "{\"team\": \"dev\"}",
      "additional_metadata": {"session": 1},
      "relations": {"ids": ["related_mem_002"]}
    }
  ]
  ```

---

## E. Retrieval & Search API (`client.query`)

```python
response = client.query(
    *,
    database: str,
    query: str,
    type: Literal["knowledge", "memory", "all"] | None = "knowledge",
    collection: str | None = None,
    query_by: Literal["hybrid", "text"] | None = "hybrid",
    mode: Literal["fast", "thinking"] | None = "fast",
    max_results: int | None = 10,
    recency_bias: float | None = None,           # 0.0 to 1.0 weighting for recent items
    graph_context: bool | None = True,           # Include extracted graph context
    query_forceful_relations: bool | None = None,# Forceful relation expansion (requires mode="thinking")
    metadata_filters: dict | None = None,        # Filter matching schema fields
    additional_context: str | None = None,       # Contextual prompt hint
    operator: Literal["or", "and", "phrase"] | None = None # Keyword operator for query_by="text"
)
```
- **Network I/O**: `POST /query` (application/json).
- **Return Type**: `HandlerEnvelopeSearchV2RetrievalResult` containing `.data` (`SearchV2RetrievalResult`):
  - `.chunks`: list of `SearchV2Chunk` (`.id`, `.chunk_uuid`, `.chunk_content`, `.relevancy_score`, `.metadata`, `.additional_metadata`, `.source_title`, `.source_type`, `.extra_context_ids`)
  - `.sources`: list of `SearchV2Source`
  - `.graph_context`: `SearchGraphContext` containing:
    - `.chunk_relations`: list of `SearchScoredPathResponse` with `.triplets` containing `SearchPathTriplet` (`source`, `target`, `relation`)
    - `.query_paths`
    - `.chunk_id_to_group_ids`

---

## F. Memory & Context Lifecycle APIs

1. **Check Status**: `client.context.status(*, database: str, ids: Sequence[str], collection: str | None = None)`
   - Returns processing status (`"queued"`, `"processing"`, `"graph_creation"`, `"completed"`, `"errored"`).
2. **Delete Context/Memory**: `client.context.delete(*, database: str, type: Literal["knowledge", "memory"], ids: Sequence[str], collection: str | None = None)`
   - Deletes specified memory IDs within scope.
3. **Inspect Content**: `client.context.inspect(*, id: str, database: str, collection: str | None = None, mode: str | None = None)`
   - Retrieves original source text or presigned URL.
4. **List Memories**: `client.context.list(*, database: str, type: Literal["knowledge", "memory"], collection: str | None = None, filters: dict | None = None, page: int | None = 1, page_size: int | None = 50)`
   - Browses stored memories matching metadata filters.
5. **Update Source Metadata**: `client.context.update_source_metadata(id: str, *, database: str, additional_metadata: dict | None = None, tenant_metadata: dict | None = None)`
   - Updates metadata attached to an indexed source.

---

## G. Inference & Entity Extraction APIs

- **`infer: True`**: When enabled on memory item JSON during `client.context.ingest()`, HydraDB's pipeline automatically extracts structured entities (`PERSON`, `LOCATION`, `PRODUCT`, `CONCEPT`) and predicate triplets with temporal attributes (`temporal_details`, `timestamp`).
- **Guided Inference**: Accepts `custom_instructions: str` and `user_assistant_pairs: list` in memory payloads to guide fact/preference extraction.

---

## H. Graph & Triplet APIs

1. **`client.context.relations(*, database: str, id: str, type: Literal["knowledge", "memory"], collection: str | None = None, limit: int | None = 50)`**
   - Retrieves explicitly declared relationships for a given source ID.
2. **Search Graph Context (`client.query(..., graph_context=True)`)**
   - Returns `graph_context.chunk_relations` containing `SearchPathTriplet`:
     - `source`: `{ entity_id, name, namespace, type }`
     - `target`: `{ entity_id, name, namespace, type }`
     - `relation`: `{ raw_predicate, canonical_predicate, temporal_details, timestamp, source_entity_id, target_entity_id }`

---

## I. Metadata & Provenance Support

- **`tenant_metadata`**: Fast, schema-aligned metadata filter fields declared at database creation via `client.databases.create(database_metadata_schema=[...])`.
- **`additional_metadata`**: Free-form key-value pairs (e.g. `{"session": 1, "timestamp": "2025-01-01"}`).
- **Provenance**: Query chunks carry `.id` (source ID), `.chunk_uuid`, `.source_title`, `.source_type`, and `.extra_context_ids` linking retrieved chunks back to raw observations.

---

## J. Temporal Support

- **Recency Weighting**: `recency_bias: float` (`0.0` to `1.0`) on `client.query()`.
- **Extracted Temporal Metadata**: Extracted triplets carry `temporal_details` strings (e.g. `"2025-02-01"`) and unix `timestamp` floats inside `triplet.relation`.

---

## K. SDK Limitations (What is NOT supported on Cloud Managed SDK)

1. **No Direct OpenCypher Query Execution**: `client.query()` accepts natural language string queries, not raw OpenCypher statements. OpenCypher is exclusive to the self-hosted HydraDB engine via Bolt/HTTP.
2. **No Native Belief Revision / Supersession**: HydraDB Cloud stores extracted triplets and chunks, but does not automatically invalidate older contradictory memories or manage state transition DAGs (`SUPERSEDES` / `INVALIDATES`).
3. **No Native Epistemic Abstention**: If asked about an unmentioned attribute, `client.query()` returns top nearest semantic chunks rather than returning an explicit `UNKNOWN` status.

---

## L. Recommended Integration Interface for ChronoGraph

ChronoGraph should construct a clean wrapper service (`app/services/hydradb_service.py`) that:
1. **Ingest Phase**: Calls `client.context.ingest(type="memory", memories=json_data)` with `infer=True` to store raw statements and trigger entity-triplet extraction.
2. **Query Phase**: Calls `client.query(type="memory", mode="thinking", graph_context=True)` to fetch semantic context chunks and extracted `SearchPathTriplet` objects.
3. **Normalization Phase**: Converts retrieved `SearchPathTriplet` objects and chunks into ChronoGraph domain `Observation` objects and candidate `BeliefState` assertions for processing by ChronoGraph's Phase 2 temporal belief engine.
