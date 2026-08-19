"""Phase 9 Evaluation Framework Test Suite."""

import pytest

from app.evaluation.baseline import NaiveMemoryBaseline
from app.evaluation.metrics import compute_aggregate_summary
from app.evaluation.runner import BenchmarkRunner
from app.evaluation.scenarios import get_all_scenarios


def test_scenario_definitions_count_and_fields():
    """1. Verify scenario suite defines 10 controlled scenarios with required ground truth fields."""
    scenarios = get_all_scenarios()
    assert len(scenarios) == 10

    for sc in scenarios:
        assert sc.id is not None
        assert sc.name is not None
        assert sc.subject_id == "user"
        assert sc.predicate is not None
        assert sc.expected_status in {"SUPPORTED", "UNKNOWN", "CONFLICTED", "CANCELLED"}
        assert len(sc.observations) > 0 or sc.expected_status == "UNKNOWN"


def test_naive_baseline_isolation_and_failure_modes():
    """2. Verify naive baseline operates independently from ChronoGraph and demonstrates expected failure modes."""
    baseline = NaiveMemoryBaseline()
    scenarios = get_all_scenarios()

    # Find future leakage scenario (Scenario 3)
    sc3 = next(s for s in scenarios if s.id == "scenario_3_future_knowledge_leakage")
    res3 = baseline.resolve_query(sc3)
    assert res3.future_leakage is True
    assert res3.value == "Cursor"  # Inverted answer due to future observation

    # Find abstention scenario (Scenario 4)
    sc4 = next(s for s in scenarios if s.id == "scenario_4_unknown_absent_fact")
    res4 = baseline.resolve_query(sc4)
    assert res4.detected_abstention is False
    assert res4.confidence == 1.0  # Baseline fails to abstain cleanly


def test_chronograph_100_percent_benchmark_accuracy():
    """3. Verify ChronoGraph engine achieves 100% accuracy across all 10 benchmark scenarios."""
    runner = BenchmarkRunner()
    cg_summary, base_summary = runner.run_full_benchmark()

    assert cg_summary.total_scenarios == 10
    assert cg_summary.correct_scenarios == 10
    assert cg_summary.overall_accuracy == 100.0
    assert cg_summary.temporal_accuracy == 100.0
    assert cg_summary.future_leakage_rate == 0.0
    assert cg_summary.contradiction_detection_rate == 100.0
    assert cg_summary.unknown_abstention_accuracy == 100.0
    assert cg_summary.cancellation_accuracy == 100.0

    # Baseline overall accuracy should be significantly lower (e.g. 20.0%)
    assert base_summary.overall_accuracy < 50.0


def test_benchmark_determinism():
    """4. Verify benchmark execution is 100% deterministic across consecutive runs."""
    runner = BenchmarkRunner()
    cg1, base1 = runner.run_full_benchmark()
    cg2, base2 = runner.run_full_benchmark()

    assert cg1.overall_accuracy == cg2.overall_accuracy
    assert base1.overall_accuracy == base2.overall_accuracy
    for i in range(len(cg1.scenario_evaluations)):
        assert cg1.scenario_evaluations[i].actual_value == cg2.scenario_evaluations[i].actual_value
