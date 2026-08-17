# CHRONOGRAPH FASTAPI REST API SPECIFICATION

The ChronoGraph REST API exposes the temporal belief and memory reasoning engine via HTTP.

---

## 1. Architecture

```text
[HTTP Client / Frontend UI / Integration]
                 │
                 ▼
+---------------------------------+
|   FastAPI Transport Layer      |  <-- app/main.py, app/api/routes.py, app/api/schemas.py
+---------------------------------+
                 │
                 ▼
+---------------------------------+
| ChronoGraph Reasoning Engine    |  <-- Temporal Resolver, State Machine, Contradiction Engine, Abstention
+---------------------------------+
                 │
                 ▼
+---------------------------------+
| Process-Local ChronoGraphStore  |  <-- In-Memory Graph Indexing & Storage
+---------------------------------+
```

---

## 2. Endpoint List

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Service health status check. |
| `POST` | `/api/v1/query` | Resolves a structured temporal belief query as of timestamp $T$. |
| `GET` | `/api/v1/timeline/{subject_id}/{predicate}` | Retrieves complete state evolution timeline for an attribute. |
| `GET` | `/api/v1/beliefs/{belief_id}` | Retrieves details of a single belief state. |
| `GET` | `/api/v1/beliefs/{belief_id}/evidence` | Retrieves grounding evidence observations for a belief. |
| `GET` | `/api/v1/beliefs/{belief_id}/lineage` | Retrieves cycle-safe belief state transition lineage history. |
| `POST` | `/api/v1/ingest` | Ingests a raw memory statement into ChronoGraph. |

---

## 3. Request & Response Examples

### Query Resolution (`POST /api/v1/query`)

**Request**:
```json
{
  "subject_id": "user",
  "predicate": "favorite_editor",
  "timestamp": "2025-03-20T00:00:00Z",
  "include_evidence": true,
  "include_lineage": false
}
```

**Response (`200 OK`)**:
```json
{
  "status": "SUPPORTED",
  "value": "VS Code",
  "confidence": 0.95,
  "reason": "Active belief supported for 'user' predicate 'favorite_editor' value 'VS Code'.",
  "belief_id": "b3_vscode",
  "subject_id": "user",
  "predicate": "favorite_editor",
  "as_of": "2025-03-20T00:00:00Z",
  "evidence": [
    {
      "id": "obs_s3",
      "text": "I switched back to VS Code. It is my favorite editor again.",
      "observed_at": "2025-03-10T00:00:00Z",
      "session_id": "s3"
    }
  ],
  "lineage": []
}
```

---

### Timeline Query (`GET /api/v1/timeline/user/favorite_editor`)

**Response (`200 OK`)**:
```json
{
  "subject_id": "user",
  "predicate": "favorite_editor",
  "timeline": [
    {
      "belief_id": "b1_vscode",
      "value": "VS Code",
      "status": "SUPERSEDED",
      "valid_from": "2025-01-10T00:00:00Z",
      "valid_until": "2025-02-10T00:00:00Z",
      "version": 1
    },
    {
      "belief_id": "b2_cursor",
      "value": "Cursor",
      "status": "SUPERSEDED",
      "valid_from": "2025-02-10T00:00:00Z",
      "valid_until": "2025-03-10T00:00:00Z",
      "version": 1
    },
    {
      "belief_id": "b3_vscode",
      "value": "VS Code",
      "status": "ACTIVE",
      "valid_from": "2025-03-10T00:00:00Z",
      "valid_until": null,
      "version": 2
    }
  ]
}
```

---

## 4. Epistemic Safety Rules & Status Semantics

1. **`UNKNOWN`**: Returned when no recorded evidence or belief exists for $(S, P)$ at timestamp $T$. Returns HTTP `200 OK` with `status: "UNKNOWN"`, `value: null`, and `confidence: 0.0`. The API **never fabricates an answer** or converts `UNKNOWN` into `SUPPORTED`.
2. **`CONFLICTED`**: Returned when two or more active beliefs for $(S, P)$ overlap in temporal validity without a supersession link. Returns HTTP `200 OK` with `status: "CONFLICTED"`, `value: null`, and `confidence: 0.5`. The API **never automatically picks a winner** or converts `CONFLICTED` into `SUPPORTED`.
3. **`CANCELLED`**: Returned when a planned belief state was explicitly invalidated by a cancellation assertion.

---

## 5. In-Memory Process State Limitation

> [!IMPORTANT]
> The current ChronoGraph API operates on a process-local `ChronoGraphStore` instance.
> Restarting the FastAPI server clears the in-memory graph state. HydraDB Cloud remains the persistent external memory and evidence substrate. Database persistence will be introduced in a future phase.
