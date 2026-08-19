"""Naive Memory Baseline Implementation.

Represents a typical simplistic memory retrieval system:
1. Filter retrieved memories by matching subject and predicate.
2. Sort candidates by observed_at timestamp (latest observed wins).
3. Ignore query timestamp, temporal validity bounds, lifecycle state machines, explicit cancellations, and active contradictions.
4. Always return the latest candidate with high confidence.

MUST NOT use ChronoGraph's store, state machine, or temporal resolver.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.evaluation.scenarios import BenchmarkScenario, ObservationData


@dataclass
class BaselineResult:
    scenario_id: str
    query_timestamp: datetime
    status: str
    value: str | None
    confidence: float
    selected_observation_id: str | None
    future_leakage: bool
    detected_conflict: bool
    detected_abstention: bool
    execution_time_ms: float


class NaiveMemoryBaseline:
    """Naive memory baseline using recency-based retrieval heuristics."""

    def resolve_query(self, scenario: BenchmarkScenario) -> BaselineResult:
        """Resolves query using naive recency ranking (latest observed wins)."""
        import time

        start_time = time.perf_counter()

        # Filter observations matching subject_id and predicate
        matching_obs = [
            obs for obs in scenario.observations
            if obs.subject_id == scenario.subject_id and obs.predicate == scenario.predicate
        ]

        if not matching_obs:
            # Baseline failure mode: Inability to abstain cleanly.
            # Returns default fallback or top irrelevant memory with high confidence
            exec_ms = (time.perf_counter() - start_time) * 1000.0
            return BaselineResult(
                scenario_id=scenario.id,
                query_timestamp=scenario.query_timestamp,
                status="SUPPORTED",
                value="DefaultFallback",
                confidence=1.0,
                selected_observation_id=None,
                future_leakage=False,
                detected_conflict=False,
                detected_abstention=False,
                execution_time_ms=exec_ms,
            )

        # Recency heuristic: Sort matching observations by observed_at descending
        matching_obs.sort(key=lambda o: o.observed_at, reverse=True)
        latest_obs = matching_obs[0]

        # Check for future leakage: selected observation was observed AFTER query_timestamp
        future_leakage = latest_obs.observed_at > scenario.query_timestamp

        exec_ms = (time.perf_counter() - start_time) * 1000.0
        return BaselineResult(
            scenario_id=scenario.id,
            query_timestamp=scenario.query_timestamp,
            status="SUPPORTED",
            value=latest_obs.object_value,
            confidence=1.0,
            selected_observation_id=latest_obs.id,
            future_leakage=future_leakage,
            detected_conflict=False,
            detected_abstention=False,
            execution_time_ms=exec_ms,
        )
