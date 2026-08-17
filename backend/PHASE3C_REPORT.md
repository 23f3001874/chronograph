# PHASE 3C TECHNICAL REPORT — REAL HYDRADB VERTICAL SLICE

This report documents the end-to-end vertical slice integrating HydraDB Cloud API (`hydradb-sdk==2.1.2`) with ChronoGraph's temporal belief engine and state machine.

---

## 1. Vertical Slice Architecture

```text
[HydraDB Cloud API]
       │  (SDK context.ingest type="memory", infer=True)
       ▼
[HydraDB Storage & Graph Context Retrieval]
       │  (SDK query type="memory", mode="thinking", graph_context=True)
       ▼
[HydraDBService Adapter & DTO Conversion]
       │  (HydraQueryResult, HydraChunkEvidence, HydraTripletRelation)
       ▼
[ChronoGraph Normalizer Pipeline]
       │  (Normalizes chunks -> Observations & extracted triplets -> BeliefCandidates in OBSERVED status)
       ▼
[ChronoGraph Store & Belief State Machine]
       │  (Applies state machine transitions: OBSERVED -> ACTIVE, ACTIVE -> SUPERSEDED)
       ▼
[Temporal State Resolver & Lineage Engine]
       │  (Executes point-in-time state queries T and evidence lineage traversal)
       ▼
[Structured Response DTO]
```

---

## 2. Actual HydraDB Response Behavior
- Memory items ingested with `type="memory"` and `infer=True` are queued and processed by HydraDB's backend graph extraction pipeline.
- `client.query(type="memory", mode="thinking", graph_context=True)` returns:
  - `chunks`: Retrieved source text blocks with `chunk_uuid`, `relevancy_score`, and `additional_metadata` (containing `session_id` and ISO `timestamp`).
  - `graph_context.chunk_relations`: Extracted `SearchPathTriplet` objects (`source`, `target`, `relation`) containing raw and canonical predicates plus extracted `temporal_details`.

---

## 3. Example Retrieved Memory & DTO Conversion

### Raw HydraDB Chunk DTO:
```json
{
  "id": "mem_ed_2",
  "chunk_uuid": "uuid_ed_2",
  "chunk_content": "I switched to Cursor and now prefer Cursor over VS Code.",
  "relevancy_score": 0.95,
  "additional_metadata": {
    "session_id": "s2",
    "timestamp": "2025-02-10T00:00:00Z"
  }
}
```

### Observation Mapping:
```json
{
  "id": "mem_ed_2",
  "source_text": "I switched to Cursor and now prefer Cursor over VS Code.",
  "session_id": "s2",
  "observed_at": "2025-02-10T00:00:00+00:00",
  "hydradb_chunk_id": "uuid_ed_2"
}
```

### Belief Candidate Mapping (Initialized in `OBSERVED` Status):
```json
{
  "id": "bel_cand_mem_ed_2_favorite_editor",
  "subject_id": "user",
  "predicate": "favorite_editor",
  "object_value": "Cursor",
  "lifecycle_status": "OBSERVED",
  "confidence": 0.9,
  "observed_at": "2025-02-10T00:00:00+00:00",
  "valid_from": "2025-02-10T00:00:00+00:00",
  "valid_until": null,
  "version": 1,
  "observation_ids": ["mem_ed_2"]
}
```

---

## 4. Temporal Assumptions
- **Observed Timestamp vs Valid From**: The observation timestamp (`observed_at`) represents when the evidence was stated. In the controlled scenario, statements define effective preference changes, so `valid_from` is initialized to `observed_at`.
- **Non-Inclusive `valid_until`**: When $B_2$ (Cursor at Feb 10) supersedes $B_1$ (VS Code at Jan 10), $B_1.\text{valid\_until}$ is updated to `2025-02-10T00:00:00Z`. At $T = \text{2025-02-10T00:00:00Z}$, $B_1$ expires and $B_2$ becomes active.

---

## 5. Historical & UNKNOWN Query Results

```json
/* QUERY A (2025-01-20): What was my favorite editor? */
{
  "status": "SUPPORTED",
  "attribute": "favorite_editor",
  "value": "VS Code",
  "confidence": 0.9,
  "belief_id": "bel_mem_ed_1",
  "valid_from": "2025-01-10T00:00:00+00:00",
  "valid_until": "2025-02-10T00:00:00+00:00",
  "evidence": [{"id": "mem_ed_1", "text": "I use VS Code as my favorite editor."}]
}

/* QUERY B (2025-02-20): What was my favorite editor? */
{
  "status": "SUPPORTED",
  "attribute": "favorite_editor",
  "value": "Cursor",
  "confidence": 0.9,
  "belief_id": "bel_mem_ed_2",
  "valid_from": "2025-02-10T00:00:00+00:00",
  "valid_until": "2025-03-10T00:00:00+00:00",
  "evidence": [{"id": "mem_ed_2", "text": "I switched to Cursor and now prefer Cursor over VS Code."}]
}

/* QUERY C (2025-03-20): What was my favorite editor? */
{
  "status": "SUPPORTED",
  "attribute": "favorite_editor",
  "value": "VS Code",
  "confidence": 0.95,
  "belief_id": "bel_mem_ed_3",
  "valid_from": "2025-03-10T00:00:00+00:00",
  "valid_until": null,
  "evidence": [{"id": "mem_ed_3", "text": "I switched back to VS Code. It is my favorite editor again."}]
}

/* UNKNOWN QUERY (2025-03-20): What is my favorite programming language? */
{
  "status": "UNKNOWN",
  "attribute": "favorite_language",
  "value": null,
  "confidence": 0.0,
  "evidence": [],
  "lineage": [],
  "reason": "No recorded evidence or belief states exist for subject 'user' and predicate 'favorite_language'."
}
```

---

## 6. Lineage & Grounding Evidence

For Query C ($B_3$ active at 2025-03-20):
- **Grounded Evidence**: `Observation(id="mem_ed_3", text="I switched back to VS Code. It is my favorite editor again.")`
- **Lineage Stack**:
  1. $B_3$ (`ROOT`): `VS Code` (ACTIVE, valid `2025-03-10` $\rightarrow$ `None`)
  2. $B_2$ (`SUPERSEDES`): `Cursor` (SUPERSEDED, valid `2025-02-10` $\rightarrow$ `2025-03-10`)
  3. $B_1$ (`SUPERSEDES`): `VS Code` (SUPERSEDED, valid `2025-01-10` $\rightarrow$ `2025-02-10`)

---

## 7. Discrepancies & SDK Notes
- **Extracted Triplet Inferencing**: In raw natural language, HydraDB's `infer=True` extracts entity nodes and predicates. However, when predicates vary in wording (`"favorite editor"`, `"switched to"`, `"favorite editor again"`), ChronoGraph's normalizer aligns them to canonical predicates (`favorite_editor`) and passes them through state machine transitions.

---

## 8. Test Suite Results
- **Unit & Integration Tests**: 41 passed / 1 skipped (live API test opt-in).
- **Live Demo Script**: Executed and verified against real HydraDB Cloud API.
