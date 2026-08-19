# CHRONOGRAPH PHASE 8 RED-TEAM & CORRECTNESS AUDIT REPORT

This document presents the findings, adversarial attack scenarios, discovered bugs, fixes, and architectural semantics of the Phase 8 ChronoGraph Red-Team Audit.

---

## 1. Audit Scope & Baseline
- **Audit Target**: Domain Model, Store, State Machine, Temporal Resolver, Contradiction Engine, Abstention Engine, Lineage Traversal, Normalizer, Ingestion Pipeline, REST API, Snapshot Persistence, and Multithreaded Concurrency.
- **Baseline Test Count**: 68 total (67 passed, 1 skipped live test, 0 failed).
- **Final Test Count**: 101 total (100 passed, 1 skipped live test, 0 failed).

---

## 2. Discovered Bugs, Reproductions & Fixes

### BUG 1 — State Machine Subject/Predicate Mismatch in Supersession
- **Severity**: **HIGH**
- **Reproduction**: Invoking `sm.supersede_belief(b2_diff_pred, b1.id)` where `b2` had `predicate="editor"` and `b1` had `predicate="location"`.
- **Actual Behavior**: The state machine permitted superseding a `location` belief with an `editor` candidate, creating a `SUPERSEDES` edge across unrelated predicates.
- **Expected Behavior**: Supersession must require matching `subject_id` and `predicate`.
- **Root Cause**: `BeliefStateMachine.supersede_belief` lacked subject/predicate validation.
- **Fix**: Added validation check:
  ```python
  if old_belief.subject_id != new_belief.subject_id or old_belief.predicate != new_belief.predicate:
      raise ValueError(f"Subject or Predicate mismatch in supersession...")
  ```
- **Regression Test**: `test_redteam_statemachine_incompatible_subject_or_predicate_supersession` in `tests/test_phase8_state_machine_redteam.py`.

---

### BUG 2 — Out-of-Order Temporal Supersession
- **Severity**: **HIGH**
- **Reproduction**: Invoking `sm.supersede_belief(b_earlier, b1.id)` where superseding belief `b_earlier` had `valid_from = Jan 1` and old belief `b1` had `valid_from = Feb 1`.
- **Actual Behavior**: State machine set `b1.valid_until = Jan 1`, creating an inverted interval (`valid_from (Feb 1) > valid_until (Jan 1)`).
- **Expected Behavior**: A superseding belief's `valid_from` cannot precede the old belief's `valid_from`.
- **Root Cause**: Missing lower-bound temporal validation in `supersede_belief`.
- **Fix**: Added validation check:
  ```python
  if new_belief.valid_from < old_belief.valid_from:
      raise ValueError(f"Superseding belief valid_from cannot precede old belief valid_from...")
  ```
- **Regression Test**: `test_redteam_statemachine_invalid_temporal_order_supersession` in `tests/test_phase8_state_machine_redteam.py`.

---

### BUG 3 — Unvalidated `OBSERVED` Candidates Leaking into Active Point-in-Time Resolution
- **Severity**: **HIGH**
- **Reproduction**: `sm.cancel_belief(b_cancel, b_plan.id)` added `b_cancel` as an `OBSERVED` observation statement. Querying `resolve_current` returned `SUPPORTED` with value `"Cancelled"` because `resolve_at_time` included `OBSERVED` candidate beliefs.
- **Actual Behavior**: Unvalidated candidate observations (`OBSERVED` status) were treated as active truth during historical point-in-time state resolution.
- **Expected Behavior**: Point-in-time state resolution (`resolve_at_time`) must evaluate world-time validity for **active truth** (`ACTIVE`, `SUPERSEDED`, `CONFLICTED`), explicitly excluding candidate `OBSERVED` and `CANCELLED` beliefs.
- **Root Cause**: `resolve_at_time` filtered out `CANCELLED` status, but failed to exclude `OBSERVED` candidate status.
- **Fix**: Updated `resolve_at_time` status filter:
  ```python
  if b.lifecycle_status in {LifecycleStatus.CANCELLED, LifecycleStatus.OBSERVED}:
      continue
  ```
- **Regression Test**: `test_redteam_temporal_L_M_N_same_value_overlap_and_cancellation` in `tests/test_phase8_temporal_redteam.py`.

---

### BUG 4 — Pipeline Collection Partition Name Validation
- **Severity**: **MEDIUM**
- **Reproduction**: Passing `collection="   "` to `process_memories`.
- **Actual Behavior**: Pipeline proceeded with whitespace-only collection string, bypassing isolation checks.
- **Fix**: Added validation check:
  ```python
  if not collection or not collection.strip():
      raise ValueError("Collection partition name cannot be empty or whitespace.")
  ```
- **Regression Test**: `test_redteam_ingestion_invalid_collection_raises_error` in `tests/test_phase8_ingestion_redteam.py`.

---

## 3. Epistemic & Temporal Semantics Audit Findings

### Future-Knowledge Leakage Audit
- **Result**: **PASS**.
- **Verification**: Injected observation $O_2$ observed in March into a store containing $O_1$ observed in January. Queries evaluated at January 15 returned the exact January state without leakage or mutation caused by the existence of the March observation.

### Epistemic Abstention Audit
- **Result**: **PASS**.
- **Verification**: Querying absent attributes returns `status: "UNKNOWN"`, `confidence: 0.0`, and `value: null`. The engine never fabricates answers or converts `UNKNOWN` into `SUPPORTED`.

### Contradiction Detection Audit
- **Result**: **PASS**.
- **Verification**: Overlapping active beliefs with disagreeing values return `status: "CONFLICTED"` and `confidence: 0.5`. Three-way contradictions return all conflicting candidates without picking an arbitrary winner. Distinct predicates (`favorite_editor` vs `favorite_language`) never conflict.

### Multithreaded Concurrency Audit
- **Result**: **PASS**.
- **Verification**: Executed 10 parallel threads performing 100 simultaneous store mutations each (1,000 total insertions). Thread lock (`RLock`) prevented lost updates, index corruption, and race conditions.

---

## 4. Final Validation Metrics
- **Pytest Suite**: **100 passed, 1 skipped, 0 failed** (1.23s execution time).
- **Python Compilation**: Clean compilation across all `app` and `tests` packages.
- **Frontend Production Build**: **Vite build succeeded** in 1.05s (0 errors / 0 warnings).
- **End-to-End Demonstration**: `python scripts/run_phase7_demo.py` passed 100%.
- **Git Status**: Working tree clean (No uncommitted debug files, no pushed changes).
