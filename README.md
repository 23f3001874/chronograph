# ChronoGraph v1.1.0

**Temporal Belief Infrastructure for AI**  
*Built for Hack Hydra 2026 — Track 3: Memory & Context Retrieval*

🌐 **Live Vercel Production Demo**: [https://chronograph-seven.vercel.app](https://chronograph-seven.vercel.app)  
💻 **GitHub Repository**: [https://github.com/23f3001874/chronograph](https://github.com/23f3001874/chronograph)  
📄 **Open-Source License**: [MIT License](file:///C:/Users/91877/chronograph/LICENSE)

---

## 🎯 Track 3 Alignment: Memory & Context Retrieval

ChronoGraph was built directly to solve the core challenges outlined in **Hack Hydra 2026 Track 3 (Memory and Context Retrieval)**:

1. **Cross-Session Continuity & Chronological Ordering**: Maintaining accurate, versioned historical beliefs as user facts evolve across multiple chat sessions.
2. **Overwritten & Superseded Information**: Handling preference updates (e.g. VS Code $\rightarrow$ Cursor $\rightarrow$ VS Code) without destroying past context or leaking future choices into past timestamps.
3. **Long-Context RAG Failures**: Eliminating recency bias and future knowledge leakage in long memory streams.
4. **Deterministic Epistemic Abstention**: Refusing to fabricate answers (`UNKNOWN`, confidence `0.00`) when historical evidence is absent.

---

## 💡 Overview & Core Architectural Idea

> *"HydraDB is not just a database I mention in the architecture. It provides the underlying memory and graph context from which ChronoGraph constructs its beliefs. ChronoGraph adds the temporal and epistemic reasoning layer on top."*

**ChronoGraph** turns raw conversational memories stored in **HydraDB Cloud** into temporally versioned belief states — complete with grounded evidence, cycle-safe lineage graphs, contradiction detection, and explicit uncertainty.

```text
                                CHRONOGRAPH + HYDRADB ARCHITECTURE
                                
                                          HYDRADB CLOUD
                                    Memory & Graph Substrate
                                               │
                                               ▼
                                     ChronoGraph Normalizer
                                               │
                                               ▼
                                      Belief State Machine
                                               │
                             ┌─────────────────┼─────────────────┐
                             ▼                 ▼                 ▼
                         Temporal           Conflict          Evidence
                         Resolver          Detection         + Lineage
                             │
                             ▼
                        Point-in-Time Answer (T)
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

On our 10-scenario controlled benchmark, ChronoGraph achieved **100.0% accuracy** compared to **30.0%** for the naive recency memory baseline (+70.0 percentage point improvement on this controlled benchmark).

- **Future Knowledge Leakage**: Naive Baseline **40.0%** $\rightarrow$ ChronoGraph **0.0%**
- **Contradiction Detection**: Naive Baseline **0.0%** $\rightarrow$ ChronoGraph **100.0%**
- **UNKNOWN Abstention Accuracy**: Naive Baseline **0.0%** $\rightarrow$ ChronoGraph **100.0%**
- **Cancellation Accuracy**: Naive Baseline **0.0%** $\rightarrow$ ChronoGraph **100.0%**
- **Average Query Latency**: **0.089 ms** (Sub-millisecond execution)

*(Note: Benchmark evaluated on 10 deterministic controlled synthetic scenarios created for evaluating temporal reasoning behavior; open-domain text extraction accuracy depends on upstream normalizer precision.)*

---

## 🚀 Live Demo & Local Setup

### Live Production URL
👉 **[https://chronograph-seven.vercel.app](https://chronograph-seven.vercel.app)**

### Local Setup Prerequisites
- Python 3.12+
- Node.js 18+

#### 1. Start the Backend API
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

#### 2. Start the Frontend UI
```powershell
cd frontend
npm run dev
```
Open **[http://localhost:5173](http://localhost:5173)** in your browser.

#### 3. Run Benchmark Suite
```powershell
python scripts/run_phase9_benchmark.py
```

#### 4. Run Hack Hydra Presentation Demo Verification
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
- `GET /health`: Health check status endpoint.

---

## 📜 Acknowledgements & Attribution

- **Hack Hydra 2026**: Built for Track 3 (Memory and Context Retrieval).
- **HydraDB Cloud**: Used as the underlying memory substrate and graph context layer for vector embeddings and Cypher entity context relationships.
- **Open-Source Libraries**: Built using FastAPI, Starlette, Pydantic, httpx, React, Vite, Lucide React, and Uvicorn.
- **Benchmark Scenarios**: Controlled synthetic benchmark scenarios created specifically to evaluate point-in-time state resolution, future leakage, contradiction detection, and epistemic abstention.

---

## 🏷️ Project Status & Submission Metadata

- **Version**: `v1.1.0`
- **Track**: Track 03 — Memory and Context Retrieval
- **Live Demo**: [https://chronograph-seven.vercel.app](https://chronograph-seven.vercel.app)
- **GitHub Repository**: [https://github.com/23f3001874/chronograph](https://github.com/23f3001874/chronograph)
- **License**: MIT License
- **Backend Tests**: 104 passed / 1 skipped
- **Phase 9 Benchmark**: 100% vs 30% baseline on 10 controlled scenarios
- **Production Deployment**: Vercel Serverless Python Engine
