"""Benchmark Runner Orchestrator.

Runs all 10 benchmark scenarios through both the Naive Memory Baseline and ChronoGraph Engine.
Collects metrics and computes comparative evaluation summaries.
"""

from datetime import datetime, timezone
import time
from typing import Any

from app.engine.contradiction import detect_conflicts
from app.engine.state_machine import BeliefStateMachine
from app.engine.store import ChronoGraphStore
from app.engine.temporal_resolver import (
    get_evidence_for_belief,
    get_lineage,
    resolve_at_time,
    resolve_current,
)
from app.services.ingestion_pipeline import query_structured_answer
from app.evaluation.baseline import NaiveMemoryBaseline
from app.evaluation.metrics import (
    EvaluationSummary,
    ScenarioEvaluation,
    compute_aggregate_summary,
    evaluate_scenario_result,
)
from app.evaluation.scenarios import BenchmarkScenario, get_all_scenarios
from app.models.domain import (
    BeliefState,
    Entity,
    LifecycleStatus,
    Observation,
)


class BenchmarkRunner:
    """Orchestrates comparative evaluation of Baseline vs ChronoGraph."""

    def __init__(self, scenarios: list[BenchmarkScenario] | None = None) -> None:
        self.scenarios = scenarios or get_all_scenarios()
        self.baseline_engine = NaiveMemoryBaseline()

    def run_chronograph_scenario(self, scenario: BenchmarkScenario) -> ScenarioEvaluation:
        """Executes a benchmark scenario using ChronoGraph Engine."""
        start_time = time.perf_counter()

        store = ChronoGraphStore()
        sm = BeliefStateMachine(store)

        # Base user entity
        store.add_entity(Entity(id=scenario.subject_id, name="User", entity_type="PERSON"))

        # Ingest observations
        obs_map: dict[str, Observation] = {}
        for o_data in scenario.observations:
            obs = Observation(
                id=o_data.id,
                source_text=o_data.source_text,
                session_id="s1",
                observed_at=o_data.observed_at,
                valid_from=o_data.valid_from,
                valid_until=o_data.valid_until,
            )
            store.add_observation(obs)
            obs_map[o_data.id] = obs

        # Build belief states and state machine transitions
        # 1. Add all observations and initial OBSERVED belief candidates into store
        b_map: dict[str, BeliefState] = {}
        cancellations: list[tuple[BeliefState, str]] = []

        for o_data in scenario.observations:
            b_state = store.add_belief(
                BeliefState(
                    id=o_data.id,
                    subject_id=scenario.subject_id,
                    predicate=o_data.predicate,
                    object_value=o_data.object_value,
                    lifecycle_status=LifecycleStatus.OBSERVED,
                    confidence=0.9,
                    observed_at=o_data.observed_at,
                    valid_from=o_data.valid_from,
                    valid_until=o_data.valid_until,
                    version=o_data.version,
                    observation_ids=[o_data.id],
                )
            )
            b_map[o_data.id] = b_state

            if o_data.is_cancellation and o_data.target_belief_id:
                cancellations.append((b_state, o_data.target_belief_id))

        # 2. Sort candidate beliefs chronologically by valid_from, then observed_at
        non_cancellations = [o for o in scenario.observations if not o.is_cancellation]
        non_cancellations.sort(key=lambda o: (o.valid_from, o.observed_at))

        # 3. Apply state machine transitions in valid_from order
        for o_data in non_cancellations:
            b_cand = b_map[o_data.id]
            if o_data.is_supersession and o_data.supersedes_id and o_data.supersedes_id in b_map:
                target_b = b_map[o_data.supersedes_id]
                sm.supersede_belief(b_cand, target_b.id)
            else:
                sm.activate_belief(b_cand)

        # 4. Apply explicit cancellations
        for b_canc, target_id in cancellations:
            sm.cancel_belief(b_canc, target_id)

        # Detect conflicts for query predicate
        detect_conflicts(store, scenario.subject_id, scenario.predicate)

        # Execute ChronoGraph query
        res_data = query_structured_answer(
            store=store,
            subject_id=scenario.subject_id,
            predicate=scenario.predicate,
            query_time=scenario.query_timestamp,
        )

        exec_ms = (time.perf_counter() - start_time) * 1000.0

        actual_status = res_data["status"]
        actual_value = res_data["value"]
        evidence_count = len(res_data.get("evidence", []))
        lineage_depth = len(res_data.get("lineage", []))

        return evaluate_scenario_result(
            scenario_id=scenario.id,
            scenario_name=scenario.name,
            query_timestamp=scenario.query_timestamp,
            expected_status=scenario.expected_status,
            expected_value=scenario.expected_value,
            actual_status=actual_status,
            actual_value=actual_value,
            evidence_count=evidence_count,
            lineage_depth=lineage_depth,
            execution_time_ms=exec_ms,
        )

    def run_baseline_scenario(self, scenario: BenchmarkScenario) -> ScenarioEvaluation:
        """Executes a benchmark scenario using Naive Memory Baseline."""
        base_res = self.baseline_engine.resolve_query(scenario)

        # Get selected observation's observed_at if available
        sel_obs = next((o for o in scenario.observations if o.id == base_res.selected_observation_id), None)
        sel_ts = sel_obs.observed_at if sel_obs else None

        return evaluate_scenario_result(
            scenario_id=scenario.id,
            scenario_name=scenario.name,
            query_timestamp=scenario.query_timestamp,
            expected_status=scenario.expected_status,
            expected_value=scenario.expected_value,
            actual_status=base_res.status,
            actual_value=base_res.value,
            evidence_count=1 if base_res.selected_observation_id else 0,
            lineage_depth=1,
            execution_time_ms=base_res.execution_time_ms,
            selected_observed_at=sel_ts,
        )

    def run_full_benchmark(self) -> tuple[EvaluationSummary, EvaluationSummary]:
        """Runs the entire benchmark suite for both ChronoGraph and Baseline."""
        cg_evals: list[ScenarioEvaluation] = []
        base_evals: list[ScenarioEvaluation] = []

        for scenario in self.scenarios:
            cg_evals.append(self.run_chronograph_scenario(scenario))
            base_evals.append(self.run_baseline_scenario(scenario))

        cg_summary = compute_aggregate_summary("ChronoGraph Engine", cg_evals)
        base_summary = compute_aggregate_summary("Naive Memory Baseline", base_evals)

        return cg_summary, base_summary
