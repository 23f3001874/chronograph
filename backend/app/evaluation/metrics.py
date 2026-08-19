"""Evaluation Metrics Calculation for ChronoGraph Benchmark.

Calculates individual and aggregate metrics across benchmark scenario executions.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class ScenarioEvaluation:
    scenario_id: str
    scenario_name: str
    expected_status: str
    expected_value: str | None
    actual_status: str
    actual_value: str | None
    correct_status: bool
    correct_value: bool
    is_correct: bool
    future_leakage: bool
    detected_conflict: bool
    detected_abstention: bool
    evidence_grounded: bool
    lineage_depth: int
    execution_time_ms: float
    failure_reason: str | None = None


@dataclass
class EvaluationSummary:
    approach_name: str
    total_scenarios: int
    correct_scenarios: int
    overall_accuracy: float
    temporal_accuracy: float
    future_leakage_rate: float
    contradiction_detection_rate: float
    unknown_abstention_accuracy: float
    supersession_accuracy: float
    cancellation_accuracy: float
    evidence_grounding_rate: float
    lineage_integrity_rate: float
    total_latency_ms: float
    avg_latency_ms: float
    scenario_evaluations: list[ScenarioEvaluation]


def evaluate_scenario_result(
    scenario_id: str,
    scenario_name: str,
    query_timestamp: Any,
    expected_status: str,
    expected_value: str | None,
    actual_status: str,
    actual_value: str | None,
    evidence_count: int,
    lineage_depth: int,
    execution_time_ms: float,
    selected_observed_at: Any | None = None,
) -> ScenarioEvaluation:
    """Evaluates a single scenario execution against ground truth expectations."""
    correct_status = (actual_status == expected_status)
    correct_value = (actual_value == expected_value)
    is_correct = correct_status and correct_value

    # Check future knowledge leakage: selected/returned timestamp is greater than query_timestamp
    future_leakage = False
    if selected_observed_at and selected_observed_at > query_timestamp:
        future_leakage = True

    detected_conflict = (actual_status == "CONFLICTED")
    detected_abstention = (actual_status == "UNKNOWN")
    evidence_grounded = (actual_status != "SUPPORTED") or (evidence_count > 0)

    failure_reason = None
    if not is_correct:
        reasons = []
        if not correct_status:
            reasons.append(f"Status mismatch (expected '{expected_status}', got '{actual_status}')")
        if not correct_value:
            reasons.append(f"Value mismatch (expected '{expected_value}', got '{actual_value}')")
        if future_leakage:
            reasons.append("Future knowledge leakage detected")
        failure_reason = "; ".join(reasons)

    return ScenarioEvaluation(
        scenario_id=scenario_id,
        scenario_name=scenario_name,
        expected_status=expected_status,
        expected_value=expected_value,
        actual_status=actual_status,
        actual_value=actual_value,
        correct_status=correct_status,
        correct_value=correct_value,
        is_correct=is_correct,
        future_leakage=future_leakage,
        detected_conflict=detected_conflict,
        detected_abstention=detected_abstention,
        evidence_grounded=evidence_grounded,
        lineage_depth=lineage_depth,
        execution_time_ms=execution_time_ms,
        failure_reason=failure_reason,
    )


def compute_aggregate_summary(
    approach_name: str,
    evaluations: list[ScenarioEvaluation],
) -> EvaluationSummary:
    """Computes aggregate benchmark summary metrics across all scenarios."""
    total = len(evaluations)
    if total == 0:
        return EvaluationSummary(
            approach_name=approach_name, total_scenarios=0, correct_scenarios=0, overall_accuracy=0.0,
            temporal_accuracy=0.0, future_leakage_rate=0.0, contradiction_detection_rate=0.0,
            unknown_abstention_accuracy=0.0, supersession_accuracy=0.0, cancellation_accuracy=0.0,
            evidence_grounding_rate=0.0, lineage_integrity_rate=0.0, total_latency_ms=0.0, avg_latency_ms=0.0,
            scenario_evaluations=[],
        )

    correct_count = sum(1 for e in evaluations if e.is_correct)
    overall_acc = (correct_count / total) * 100.0

    # 1. Temporal Accuracy across sequential/temporal scenarios (1, 3, 7, 8, 10)
    temp_scenarios = [e for e in evaluations if e.scenario_id in {
        "scenario_1_sequential_belief_change", "scenario_3_future_knowledge_leakage",
        "scenario_7_explicit_supersession", "scenario_8_out_of_order_observations", "scenario_10_long_lineage"
    }]
    temp_acc = (sum(1 for e in temp_scenarios if e.is_correct) / len(temp_scenarios) * 100.0) if temp_scenarios else 0.0

    # 2. Future Leakage Rate
    leakage_count = sum(1 for e in evaluations if e.future_leakage)
    leakage_rate = (leakage_count / total) * 100.0

    # 3. Contradiction Detection Rate across conflict scenarios (2, 9)
    conflict_scenarios = [e for e in evaluations if e.expected_status == "CONFLICTED"]
    conflict_rate = (sum(1 for e in conflict_scenarios if e.actual_status == "CONFLICTED") / len(conflict_scenarios) * 100.0) if conflict_scenarios else 0.0

    # 4. UNKNOWN Abstention Accuracy (scenario 4)
    unknown_scenarios = [e for e in evaluations if e.expected_status == "UNKNOWN"]
    unknown_acc = (sum(1 for e in unknown_scenarios if e.actual_status == "UNKNOWN") / len(unknown_scenarios) * 100.0) if unknown_scenarios else 0.0

    # 5. Supersession Accuracy (scenarios 1, 7, 10)
    sup_scenarios = [e for e in evaluations if e.scenario_id in {"scenario_1_sequential_belief_change", "scenario_7_explicit_supersession", "scenario_10_long_lineage"}]
    sup_acc = (sum(1 for e in sup_scenarios if e.is_correct) / len(sup_scenarios) * 100.0) if sup_scenarios else 0.0

    # 6. Cancellation Accuracy (scenario 5)
    canc_scenarios = [e for e in evaluations if e.expected_status == "CANCELLED"]
    canc_acc = (sum(1 for e in canc_scenarios if e.actual_status == "CANCELLED") / len(canc_scenarios) * 100.0) if canc_scenarios else 0.0

    # 7. Evidence Grounding Rate
    grounding_rate = (sum(1 for e in evaluations if e.evidence_grounded) / total) * 100.0

    # 8. Lineage Integrity Rate (lineage depth > 1 for deep scenarios)
    lineage_scenarios = [e for e in evaluations if e.scenario_id in {"scenario_1_sequential_belief_change", "scenario_7_explicit_supersession", "scenario_10_long_lineage"}]
    lineage_rate = (sum(1 for e in lineage_scenarios if e.lineage_depth > 1) / len(lineage_scenarios) * 100.0) if lineage_scenarios else 0.0

    # 9. Latency Metrics
    total_latency = sum(e.execution_time_ms for e in evaluations)
    avg_latency = total_latency / total

    return EvaluationSummary(
        approach_name=approach_name,
        total_scenarios=total,
        correct_scenarios=correct_count,
        overall_accuracy=overall_acc,
        temporal_accuracy=temp_acc,
        future_leakage_rate=leakage_rate,
        contradiction_detection_rate=conflict_rate,
        unknown_abstention_accuracy=unknown_acc,
        supersession_accuracy=sup_acc,
        cancellation_accuracy=canc_acc,
        evidence_grounding_rate=grounding_rate,
        lineage_integrity_rate=lineage_rate,
        total_latency_ms=total_latency,
        avg_latency_ms=avg_latency,
        scenario_evaluations=evaluations,
    )
