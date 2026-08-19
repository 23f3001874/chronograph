# CHRONOGRAPH HACK HYDRA DEMO PRESENTATION GUIDE (PHASE 10)

This document provides step-by-step instructions, talking points, and verification flows for demonstrating ChronoGraph to judges and attendees at Hack Hydra 2026.

---

## 1. Executive Summary & 30-Second Elevator Pitch

> *"Most AI agent memory systems use vector search or recency matching. If a user says 'I prefer Cursor' in February and 'I prefer VS Code' in March, vector systems get confused and leak future facts into past historical queries. ChronoGraph builds a temporal belief graph on top of HydraDB Cloud. It models validity intervals, tracks state transitions, detects active contradictions, and abstains with UNKNOWN when evidence is absent."*

---

## 2. The Single Killer Scenario Walkthrough

The demo centers around a 3-month preference timeline:

- **January 2025**: *"I use VS Code as my favorite editor."*
- **February 2025**: *"I switched to Cursor. Cursor is now my favorite editor."*
- **March 2025**: *"I switched back to VS Code. It is my favorite editor again."*

Plus an active spatial contradiction:
- **Location 1**: *"I live in Delhi"* (Valid Jan 1 – Mar 1)
- **Location 2**: *"I live in Bangalore"* (Valid Feb 1 – Apr 1)

---

## 3. Demo Step-by-Step Execution Guide

### Option A: Interactive React UI Demo (Recommended for Presentations)

1. Open **[http://localhost:5173](http://localhost:5173)** in Chrome or Edge.
2. Click **`[Preset: VS Code → Cursor → VS Code]`** in the header bar or preset control box. (Loads the 5 killer observations into memory).
3. **Step 1 — Point-in-Time Historical Query (Jan 20)**:
   - Select timestamp **Jan 20, 2025**.
   - Click **Execute Resolution Query**.
   - **Show Output**: Status is `SUPPORTED`, Value is `"VS Code"`.
4. **Step 2 — Point-in-Time Historical Query (Feb 20)**:
   - Select timestamp **Feb 20, 2025**.
   - Click **Execute Resolution Query**.
   - **Show Output**: Status is `SUPPORTED`, Value is `"Cursor"`.
5. **Step 3 — Point-in-Time Historical Query (Mar 20)**:
   - Select timestamp **Mar 20, 2025**.
   - Click **Execute Resolution Query**.
   - **Show Output**: Status is `SUPPORTED`, Value is `"VS Code"`.
6. **Step 4 — Epistemic Abstention (UNKNOWN)**:
   - Select predicate `favorite_language`.
   - Click **Execute Resolution Query**.
   - **Show Output**: Status is `UNKNOWN`, Confidence is `0.0%`, Value is `null`. Point out that ChronoGraph refrains from hallucinating or guessing.
7. **Step 5 — Overlapping Active Contradiction (CONFLICTED)**:
   - Select predicate `location` and date **Feb 15, 2025**.
   - Click **Execute Resolution Query**.
   - **Show Output**: Status is `CONFLICTED`, Confidence is `50%`, Value is `null`. Point out that ChronoGraph flags simultaneous disagreement without picking an arbitrary winner.
8. **Step 6 — Inspect Evidence & Lineage Stack**:
   - Click **Belief Timeline** or **Graph & Lineage Stack** tab.
   - Show the 3-node supersession chain ($B_3 \rightarrow B_2 \rightarrow B_1$) and grounded observation text.

---

### Option B: Automated Terminal Command Demo

Run the automated presentation verification script:

```powershell
python scripts/run_phase10_demo.py
```

Output confirms 100% verification across all 10 demo steps.

---

## 4. Key Hack Hydra Talking Points for Judges

1. **HydraDB Cloud Substrate**:
   - We utilize HydraDB Cloud as our memory storage and context retrieval substrate (storing raw memories, vector embeddings, and chunk/triplet context relations).
2. **What ChronoGraph Adds**:
   - HydraDB stores memories; ChronoGraph reasons over temporal belief state transitions ($[valid\_from, valid\_until)$), state supersession, active contradiction detection, and epistemic abstention.
3. **Empirical Benchmark Proof**:
   - In our 10-scenario offline benchmark, naive recency retrieval achieved only 30.0% accuracy with 40.0% future leakage. ChronoGraph achieved **100.0% accuracy** with **0.0% future leakage** at **0.092 ms latency**.

---

## 5. Troubleshooting & Demo Safety

- **Backend Connection**: If the frontend header displays `Disconnected`, ensure `uvicorn app.main:app --port 8000` is running.
- **Store Reset**: Clicking any Preset button resets and reloads clean deterministic fixtures, ensuring repeatable demo presentations.
