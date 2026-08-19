# CHRONOGRAPH PHASE 9 — COMPARATIVE EVALUATION & BENCHMARK REPORT

This document presents the experimental design, scenario definitions, comparative benchmark execution, failure analysis, and empirical conclusions of the Phase 9 ChronoGraph Evaluation.

---

## 1. Objective
The goal of Phase 9 is to experimentally measure and quantify whether ChronoGraph's temporal state machine and epistemic reasoning provide a measurable accuracy advantage over a naive recency-ranked memory retrieval approach.

---

## 2. Experimental Design & Architecture
The evaluation framework compares two independent memory resolution approaches across 10 controlled, deterministic benchmark scenarios:

1. **Approach A — Naive Memory Baseline**:
   - Represents a standard simplistic memory retrieval pipeline.
   - Ranks retrieved observations by `observed_at` timestamp in descending order (latest observed wins).
   - Ignores query timestamps, validity intervals (`[valid_from, valid_until)`), lifecycle transitions (`ACTIVE`, `SUPERSEDED`, `CANCELLED`), active contradictions, and missing evidence.
   - Always attempts to return a value with high confidence (1.0).

2. **Approach B — ChronoGraph Engine**:
   - Uses ChronoGraph's deterministic graph reasoning engine.
   - Point-in-time temporal state resolution (`resolve_at_time` / `resolve_current`).
   - Belief lifecycle state machine transitions (`ACTIVE`, `SUPERSEDED`, `CANCELLED`).
   - Contradiction engine (`CONFLICTED` status with 0.5 confidence).
   - Epistemic abstention (`UNKNOWN` status with 0.0 confidence for unrecorded facts).
   - Grounded evidence and lineage stack traversal (`SUPERSEDES`, `INVALIDATES`, `CONTRADICTS`).

---

## 3. Benchmark Scenario Definitions

| # | Scenario ID | Name | Query Timestamp | Ground Truth Expectation |
| :-: | :--- | :--- | :---: | :--- |
| **1** | `scenario_1_sequential_belief_change` | Sequential Belief Change | `2025-02-15` | `SUPPORTED` \| Value: `"Cursor"` |
| **2** | `scenario_2_overlapping_contradiction` | Overlapping Contradiction | `2025-02-15` | `CONFLICTED` \| Value: `null` |
| **3** | `scenario_3_future_knowledge_leakage` | Future Knowledge Leakage | `2025-01-15` | `SUPPORTED` \| Value: `"VS Code"` |
| **4** | `scenario_4_unknown_absent_fact` | UNKNOWN Epistemic Abstention | `2025-01-15` | `UNKNOWN` \| Value: `null` |
| **5** | `scenario_5_cancellation` | Planned Belief Cancellation | `2025-04-15` | `CANCELLED` \| Value: `null` |
| **6** | `scenario_6_same_value_reassertion` | Same-Value Reassertion | `2025-01-20` | `SUPPORTED` \| Value: `"VS Code"` |
| **7** | `scenario_7_explicit_supersession` | Explicit State Supersession | `2025-02-15` | `SUPPORTED` \| Value: `"Bangalore"` |
| **8** | `scenario_8_out_of_order_observations` | Out-of-Order Observation | `2025-01-15` | `SUPPORTED` \| Value: `"Delhi"` |
| **9** | `scenario_9_conflicting_evidence` | Simultaneous Disagreeing Evidence | `2025-01-15` | `CONFLICTED` \| Value: `null` |
| **10** | `scenario_10_long_lineage` | Deep Lineage Chain Traversal | `2025-03-15` | `SUPPORTED` \| Value: `"ToolC"` |

---

## 4. Aggregate Benchmark Results

| Metric | Naive Memory Baseline | ChronoGraph Engine | ChronoGraph Advantage |
| :--- | :---: | :---: | :---: |
| **Overall Accuracy** | 30.0% | **100.0%** | **+70.0%** |
| **Temporal Accuracy** | 40.0% | **100.0%** | **+60.0%** |
| **Future Leakage Rate** | 40.0% | **0.0%** | **-40.0%** (0% Leakage) |
| **Contradiction Detection** | 0.0% | **100.0%** | **+100.0%** |
| **UNKNOWN Abstention Acc.** | 0.0% | **100.0%** | **+100.0%** |
| **Supersession Accuracy** | 33.3% | **100.0%** | **+66.7%** |
| **Cancellation Accuracy** | 0.0% | **100.0%** | **+100.0%** |
| **Evidence Grounding** | 90.0% | **100.0%** | **+10.0%** |
| **Lineage Integrity** | 0.0% | **100.0%** | **+100.0%** |
| **Average Latency** | 0.002 ms | 0.092 ms | Sub-millisecond Execution |

---

## 5. Detailed Per-Scenario Failure Analysis

### 1. Future Knowledge Leakage (Scenarios 1, 3, 10)
- **Baseline Failure**: In Scenario 3, a March observation $O_2$ ("I switched to Cursor") was ingested after a January observation $O_1$ ("I use VS Code"). When queried at `2025-01-15`, the baseline selected $O_2$ because it was observed later. This caused severe **future knowledge leakage** (answering a January query using information observed in March).
- **ChronoGraph Result**: ChronoGraph evaluated world-time validity at `2025-01-15` ($[2025-01-01, 2025-02-01)$) and correctly returned `"VS Code"` with zero future leakage.

### 2. Overlapping Contradiction (Scenarios 2, 9)
- **Baseline Failure**: In Scenarios 2 and 9, two disagreeing active beliefs existed at the query timestamp without a supersession relationship. The baseline arbitrarily selected the latest observation and returned it as `SUPPORTED` truth with 1.0 confidence.
- **ChronoGraph Result**: ChronoGraph identified overlapping active disagreement, marked both states `CONFLICTED`, created a `CONTRADICTS` edge, and returned `status: CONFLICTED` with `confidence: 0.5`.

### 3. Epistemic Abstention (Scenario 4)
- **Baseline Failure**: When queried for an unrecorded predicate (`favorite_language`), the baseline could not abstain and returned a fallback value with 1.0 confidence.
- **ChronoGraph Result**: ChronoGraph detected zero recorded evidence, returning `status: UNKNOWN` and `confidence: 0.0`.

### 4. Planned Belief Cancellation (Scenario 5)
- **Baseline Failure**: When querying a planned move that was subsequently cancelled, the baseline selected the cancellation memory text `"Cancelled"` as a supported active location value.
- **ChronoGraph Result**: ChronoGraph updated the target belief lifecycle to `CANCELLED`, created an `INVALIDATES` edge, and returned `status: CANCELLED`.

---

## 6. Execution & Reproducibility
The benchmark is 100% deterministic, offline, and reproducible via:

```powershell
python scripts/run_phase9_benchmark.py
```

Machine-readable JSON results are exported to `scripts/benchmark_results.json`.

---

## 7. Evidence-Based Conclusion
The empirical benchmark demonstrates that ChronoGraph provides a **+70.0% overall accuracy increase** over naive recency-based memory retrieval (100.0% vs 30.0%). ChronoGraph completely eliminates future knowledge leakage (0.0% vs 40.0%), reliably flags contradictory active beliefs (100.0% vs 0.0%), and deterministically abstains on unrecorded facts (100.0% vs 0.0%).
