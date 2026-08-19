# ChronoGraph

**Temporal Memory & Epistemic Reasoning Engine for AI Agents**  
*Hack Hydra 2026 — Track 3: Memory + Context Retrieval*

---

## 💡 Overview

**ChronoGraph** is a deterministic temporal memory and epistemic reasoning engine built on top of **HydraDB Cloud**. It enables AI agents to track evolving entity facts over time, perform point-in-time historical state resolution ($T$), detect active temporal contradictions, and abstain deterministically (`UNKNOWN`) when evidence is absent.

```text
                                CHRONOGRAPH ARCHITECTURE
                                
  ┌─────────────────┐       ┌────────────────────────┐       ┌────────────────────────┐
  │  HydraDB Cloud  │ ────> │ Normalization Pipeline │ ────> │  Belief State Machine  │
  │ Vector & Graph  │       │ Triplet & Chunk Filter │       │ ACTIVE / SUPERSEDED    │
  └─────────────────┘       └────────────────────────┘       └────────────────────────┘
                                                                          │
  ┌─────────────────┐       ┌────────────────────────┐                    ▼
  │  React/Vite UI  │ <──── │  FastAPI REST Service  │ <──── ┌────────────────────────┐
  │ Visual Explorer │       │ Point-in-Time Resolver │       │   ChronoGraph Store    │
  └─────────────────┘       └────────────────────────┘       │  Temporal Indexing     │
                                                             └────────────────────────┘
```

---

## ❓ The Problem with Naive Agent Memory

Simplistic vector search and recency-ranked memory systems suffer from four severe failure modes:

1. **Future Knowledge Leakage**: Querying an agent for what the user preferred in *January* returns facts observed in *March* because the March memory is newest.
2. **Silent Overwrite of Conflicts**: Overlapping contradictory facts (e.g. living in Delhi AND Bangalore in February) cause naive systems to pick an arbitrary winner instead of flagging a conflict.
3. **Hallucination on Absent Facts**: Naive retrieval returns irrelevant high-scoring memories instead of cleanly abstaining when no evidence exists for a question.
4. **Misinterpreting Cancellations**: Storing "Cancelled Paris trip" causes naive systems to report "Paris" as an active supported destination.

---

## 🛡️ The ChronoGraph Solution

ChronoGraph solves these fundamental failure modes through formal temporal and epistemic modeling:

- **Point-in-Time State Resolution ($T$)**: Evaluates world validity across temporal intervals $[valid\_from, valid\_until)$ as of query timestamp $T$, preventing future knowledge leakage.
- **Explicit Lifecycle State Machine**: Manages belief transitions (`OBSERVED` $\rightarrow$ `ACTIVE` $\rightarrow$ `SUPERSEDED` / `CANCELLED`).
- **Epistemic Abstention (`UNKNOWN`)**: Returns `status: "UNKNOWN"` and `confidence: 0.0` when no evidence exists for a predicate.
- **Contradiction Detection (`CONFLICTED`)**: Identifies simultaneous active disagreements, returning `status: "CONFLICTED"` and `confidence: 0.5` without picking arbitrary winners.
- **Grounded Evidence & Lineage Stacks**: Every answer is linked directly to raw observations and cycle-safe `SUPERSEDES` / `INVALIDATES` transition graphs.

---

## 🔄 The Killer Temporal Demo

Consider a user whose editor preference evolves over time:

- **Jan 1, 2025**: *"I use VS Code as my favorite editor."*
- **Feb 1, 2025**: *"I switched to Cursor. Cursor is now my favorite editor."*
- **Mar 1, 2025**: *"I switched back to VS Code. It is my favorite editor again."*

### Querying ChronoGraph at Timestamp $T$:

| Query Date ($T$) | Question | ChronoGraph Output | Epistemic Status |
| :---: | :--- | :---: | :---: |
| **Jan 20, 2025** | *"What was my favorite editor?"* | **VS Code** | `SUPPORTED` (Conf: 0.90) |
| **Feb 20, 2025** | *"What was my favorite editor?"* | **Cursor** | `SUPPORTED` (Conf: 0.90) |
| **Mar 20, 2025** | *"What was my favorite editor?"* | **VS Code** | `SUPPORTED` (Conf: 0.90) |
| **Jan 15, 2025** | *"What is my favorite language?"* | `null` *(Abstains)* | `UNKNOWN` (Conf: 0.00) |
| **Feb 15, 2025** | *"Where do I live?"* *(Delhi vs Bangalore)* | `null` *(Conflict)* | `CONFLICTED` (Conf: 0.50) |

---

## 🧩 HydraDB Cloud Integration vs ChronoGraph Engine

| Subsystem | Managed By | Responsibility |
| :--- | :---: | :--- |
| **Memory Ingestion & Chunks** | **HydraDB Cloud** | Persistent memory storage, vector embeddings, chunk UUIDs. |
| **Graph Triplet Context** | **HydraDB Cloud** | OpenCypher context query, `chunk_relations`, source/target entity inference. |
| **Temporal Validity Bounds** | **ChronoGraph** | Normalizing $[valid\_from, valid\_until)$ timestamps. |
| **Belief Lifecycle State Machine** | **ChronoGraph** | `ACTIVE`, `SUPERSEDED`, `CANCELLED`, `CONFLICTED` state management. |
| **Point-in-Time Historical Resolver**| **ChronoGraph** | Point-in-time temporal state evaluation as of query timestamp $T$. |
| **Epistemic Abstention & Conflict** | **ChronoGraph** | `UNKNOWN` (0.0 confidence) and `CONFLICTED` (0.5 confidence) semantics. |
| **Lineage Graph Stack** | **ChronoGraph** | Cycle-safe `SUPERSEDES` and `INVALIDATES` graph traversal. |

---

## 📊 Evaluation & Benchmark Results

On our 10-scenario controlled benchmark, ChronoGraph achieved **100.0% accuracy** compared to **30.0%** for the naive recency memory baseline (+70.0 percentage point improvement).

- **Future Knowledge Leakage**: Naive Baseline **40.0%** $\rightarrow$ ChronoGraph **0.0%**
- **Contradiction Detection**: Naive Baseline **0.0%** $\rightarrow$ ChronoGraph **100.0%**
- **UNKNOWN Abstention Accuracy**: Naive Baseline **0.0%** $\rightarrow$ ChronoGraph **100.0%**
- **Cancellation Accuracy**: Naive Baseline **0.0%** $\rightarrow$ ChronoGraph **100.0%**
- **Average Query Latency**: **0.092 ms** (Sub-millisecond execution)

*(Note: Benchmark evaluated on 10 deterministic controlled synthetic scenarios; open-domain text extraction accuracy depends on upstream normalizer precision.)*

---

## 🚀 Quick Start & Local Setup

### Prerequisites
- Python 3.13+
- Node.js 18+

### 1. Start the Backend API
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

### 2. Start the Frontend UI
```powershell
cd frontend
npm run dev
```
Open **[http://localhost:5173](http://localhost:5173)** in your browser.

### 3. Run Benchmark Suite
```powershell
python scripts/run_phase9_benchmark.py
```

### 4. Run Hack Hydra Presentation Demo Verification
```powershell
python scripts/run_phase10_demo.py
```

---

## 📡 REST API Summary

- `POST /api/v1/query`: Resolves structured temporal belief query as of timestamp $T$.
- `GET /api/v1/timeline/{subject_id}/{predicate}`: Retrieves complete historical belief evolution timeline.
- `GET /api/v1/beliefs/{belief_id}`: Retrieves single belief detail.
- `GET /api/v1/beliefs/{belief_id}/evidence`: Retrieves grounding evidence observations.
- `GET /api/v1/beliefs/{belief_id}/lineage`: Retrieves cycle-safe belief state transition lineage stack.
- `POST /api/v1/ingest`: Ingests raw memory statement and constructs normalized candidates.
- `POST /api/v1/demo/load`: Loads deterministic Hack Hydra killer scenario into memory.

---

## 🏷️ Project Status
- **Current Version**: `v0.9.0` (Phase 10 Presentation Ready)
- **Backend Test Suite**: 104 passed / 1 skipped
- **Frontend Build**: Vite production build clean (0 errors)
