"""Phase 9 Evaluation Scenarios.

Defines 10 controlled, deterministic benchmark scenarios with ground-truth expectations.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ObservationData:
    id: str
    source_text: str
    observed_at: datetime
    valid_from: datetime
    valid_until: datetime | None = None
    subject_id: str = "user"
    predicate: str = "favorite_editor"
    object_value: str = ""
    version: int = 1
    is_cancellation: bool = False
    target_belief_id: str | None = None
    is_supersession: bool = False
    supersedes_id: str | None = None


@dataclass
class BenchmarkScenario:
    id: str
    name: str
    description: str
    subject_id: str
    predicate: str
    query_timestamp: datetime
    expected_status: str  # SUPPORTED, UNKNOWN, CONFLICTED, CANCELLED
    expected_value: str | None
    expected_lineage_depth: int = 1
    observations: list[ObservationData] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


def get_all_scenarios() -> list[BenchmarkScenario]:
    """Returns the suite of 10 deterministic benchmark scenarios."""
    scenarios: list[BenchmarkScenario] = []

    # -------------------------------------------------------------------------
    # Scenario 1: SEQUENTIAL BELIEF CHANGE (VS Code -> Cursor -> VS Code)
    # -------------------------------------------------------------------------
    scenarios.append(
        BenchmarkScenario(
            id="scenario_1_sequential_belief_change",
            name="Sequential Belief Change",
            description="Tests historical point-in-time state resolution across a sequence of belief transitions.",
            subject_id="user",
            predicate="favorite_editor",
            query_timestamp=datetime(2025, 2, 15, tzinfo=timezone.utc),
            expected_status="SUPPORTED",
            expected_value="Cursor",
            expected_lineage_depth=2,
            observations=[
                ObservationData(
                    id="o1", source_text="I use VS Code",
                    observed_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
                    valid_from=datetime(2025, 1, 1, tzinfo=timezone.utc),
                    valid_until=datetime(2025, 2, 1, tzinfo=timezone.utc),
                    object_value="VS Code", version=1
                ),
                ObservationData(
                    id="o2", source_text="I switched to Cursor",
                    observed_at=datetime(2025, 2, 1, tzinfo=timezone.utc),
                    valid_from=datetime(2025, 2, 1, tzinfo=timezone.utc),
                    valid_until=datetime(2025, 3, 1, tzinfo=timezone.utc),
                    object_value="Cursor", version=2,
                    is_supersession=True, supersedes_id="o1"
                ),
                ObservationData(
                    id="o3", source_text="I switched back to VS Code",
                    observed_at=datetime(2025, 3, 1, tzinfo=timezone.utc),
                    valid_from=datetime(2025, 3, 1, tzinfo=timezone.utc),
                    object_value="VS Code", version=3,
                    is_supersession=True, supersedes_id="o2"
                ),
            ],
        )
    )

    # -------------------------------------------------------------------------
    # Scenario 2: OVERLAPPING CONTRADICTION (Delhi vs Bangalore)
    # -------------------------------------------------------------------------
    scenarios.append(
        BenchmarkScenario(
            id="scenario_2_overlapping_contradiction",
            name="Overlapping Contradiction",
            description="Tests detection of overlapping active contradictory beliefs without picking an arbitrary winner.",
            subject_id="user",
            predicate="location",
            query_timestamp=datetime(2025, 2, 15, tzinfo=timezone.utc),
            expected_status="CONFLICTED",
            expected_value=None,
            expected_lineage_depth=1,
            observations=[
                ObservationData(
                    id="o1_delhi", source_text="I live in Delhi",
                    observed_at=datetime(2025, 1, 10, tzinfo=timezone.utc),
                    valid_from=datetime(2025, 1, 1, tzinfo=timezone.utc),
                    valid_until=datetime(2025, 3, 1, tzinfo=timezone.utc),
                    predicate="location", object_value="Delhi", version=1,
                    is_supersession=False
                ),
                ObservationData(
                    id="o2_blr", source_text="I live in Bangalore",
                    observed_at=datetime(2025, 2, 10, tzinfo=timezone.utc),
                    valid_from=datetime(2025, 2, 1, tzinfo=timezone.utc),
                    valid_until=datetime(2025, 4, 1, tzinfo=timezone.utc),
                    predicate="location", object_value="Bangalore", version=2,
                    is_supersession=False
                ),
            ],
        )
    )

    # -------------------------------------------------------------------------
    # Scenario 3: FUTURE KNOWLEDGE LEAKAGE (Jan query with March evidence)
    # -------------------------------------------------------------------------
    scenarios.append(
        BenchmarkScenario(
            id="scenario_3_future_knowledge_leakage",
            name="Future Knowledge Leakage Prevention",
            description="Ensures future observations (observed in March) do not alter historical query evaluated at Jan 15.",
            subject_id="user",
            predicate="favorite_editor",
            query_timestamp=datetime(2025, 1, 15, tzinfo=timezone.utc),
            expected_status="SUPPORTED",
            expected_value="VS Code",
            expected_lineage_depth=1,
            observations=[
                ObservationData(
                    id="o1_jan", source_text="I use VS Code",
                    observed_at=datetime(2025, 1, 5, tzinfo=timezone.utc),
                    valid_from=datetime(2025, 1, 1, tzinfo=timezone.utc),
                    valid_until=datetime(2025, 2, 1, tzinfo=timezone.utc),
                    object_value="VS Code", version=1
                ),
                ObservationData(
                    id="o2_mar", source_text="I switched to Cursor",
                    observed_at=datetime(2025, 3, 5, tzinfo=timezone.utc),
                    valid_from=datetime(2025, 2, 1, tzinfo=timezone.utc),
                    object_value="Cursor", version=2,
                    is_supersession=True, supersedes_id="o1_jan"
                ),
            ],
        )
    )

    # -------------------------------------------------------------------------
    # Scenario 4: UNKNOWN / ABSENT FACT (Query unrecorded predicate)
    # -------------------------------------------------------------------------
    scenarios.append(
        BenchmarkScenario(
            id="scenario_4_unknown_absent_fact",
            name="UNKNOWN Epistemic Abstention",
            description="Tests deterministic abstention (UNKNOWN, confidence 0.0) when evidence for predicate is completely absent.",
            subject_id="user",
            predicate="favorite_language",
            query_timestamp=datetime(2025, 1, 15, tzinfo=timezone.utc),
            expected_status="UNKNOWN",
            expected_value=None,
            expected_lineage_depth=0,
            observations=[
                # Unrelated observations for favorite_editor
                ObservationData(
                    id="o1", source_text="I use VS Code",
                    observed_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
                    valid_from=datetime(2025, 1, 1, tzinfo=timezone.utc),
                    object_value="VS Code", version=1
                )
            ],
        )
    )

    # -------------------------------------------------------------------------
    # Scenario 5: CANCELLATION (Planned move -> Cancelled)
    # -------------------------------------------------------------------------
    scenarios.append(
        BenchmarkScenario(
            id="scenario_5_cancellation",
            name="Planned Belief Cancellation",
            description="Tests explicit cancellation of a planned belief, ensuring it is not returned as supported active truth.",
            subject_id="user",
            predicate="planned_trip",
            query_timestamp=datetime(2025, 4, 15, tzinfo=timezone.utc),
            expected_status="CANCELLED",
            expected_value=None,
            expected_lineage_depth=2,
            observations=[
                ObservationData(
                    id="b_plan", source_text="Planning trip to Paris in April",
                    observed_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
                    valid_from=datetime(2025, 4, 1, tzinfo=timezone.utc),
                    predicate="planned_trip", object_value="Paris", version=1
                ),
                ObservationData(
                    id="b_cancel", source_text="Cancelled Paris trip",
                    observed_at=datetime(2025, 2, 1, tzinfo=timezone.utc),
                    valid_from=datetime(2025, 2, 1, tzinfo=timezone.utc),
                    predicate="planned_trip", object_value="Cancelled", version=1,
                    is_cancellation=True, target_belief_id="b_plan"
                ),
            ],
        )
    )

    # -------------------------------------------------------------------------
    # Scenario 6: SAME-VALUE REASSERTION (Same value across overlapping intervals)
    # -------------------------------------------------------------------------
    scenarios.append(
        BenchmarkScenario(
            id="scenario_6_same_value_reassertion",
            name="Same-Value Reassertion",
            description="Verifies that re-asserting the same value across overlapping intervals does NOT trigger a false contradiction.",
            subject_id="user",
            predicate="favorite_editor",
            query_timestamp=datetime(2025, 1, 20, tzinfo=timezone.utc),
            expected_status="SUPPORTED",
            expected_value="VS Code",
            expected_lineage_depth=1,
            observations=[
                ObservationData(
                    id="o1", source_text="I use VS Code",
                    observed_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
                    valid_from=datetime(2025, 1, 1, tzinfo=timezone.utc),
                    object_value="VS Code", version=1
                ),
                ObservationData(
                    id="o2", source_text="Still using VS Code",
                    observed_at=datetime(2025, 1, 15, tzinfo=timezone.utc),
                    valid_from=datetime(2025, 1, 15, tzinfo=timezone.utc),
                    object_value="VS Code", version=2
                ),
            ],
        )
    )

    # -------------------------------------------------------------------------
    # Scenario 7: EXPLICIT SUPERSESSION (B2 explicitly supersedes B1)
    # -------------------------------------------------------------------------
    scenarios.append(
        BenchmarkScenario(
            id="scenario_7_explicit_supersession",
            name="Explicit State Supersession",
            description="Verifies that explicit state machine supersession updates old valid_until and forms a lineage graph.",
            subject_id="user",
            predicate="location",
            query_timestamp=datetime(2025, 2, 15, tzinfo=timezone.utc),
            expected_status="SUPPORTED",
            expected_value="Bangalore",
            expected_lineage_depth=2,
            observations=[
                ObservationData(
                    id="b1", source_text="Living in Delhi",
                    observed_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
                    valid_from=datetime(2025, 1, 1, tzinfo=timezone.utc),
                    predicate="location", object_value="Delhi", version=1
                ),
                ObservationData(
                    id="b2", source_text="Moved to Bangalore",
                    observed_at=datetime(2025, 2, 1, tzinfo=timezone.utc),
                    valid_from=datetime(2025, 2, 1, tzinfo=timezone.utc),
                    predicate="location", object_value="Bangalore", version=2,
                    is_supersession=True, supersedes_id="b1"
                ),
            ],
        )
    )

    # -------------------------------------------------------------------------
    # Scenario 8: OUT-OF-ORDER OBSERVATIONS (Observed out of valid order)
    # -------------------------------------------------------------------------
    scenarios.append(
        BenchmarkScenario(
            id="scenario_8_out_of_order_observations",
            name="Out-of-Order Observation Processing",
            description="Ensures ChronoGraph orders validity by valid_from timestamps rather than ingestion/observation sequence.",
            subject_id="user",
            predicate="location",
            query_timestamp=datetime(2025, 1, 15, tzinfo=timezone.utc),
            expected_status="SUPPORTED",
            expected_value="Delhi",
            expected_lineage_depth=1,
            observations=[
                # Ingested FIRST, but valid in Feb
                ObservationData(
                    id="o2_feb", source_text="Moved to Bangalore",
                    observed_at=datetime(2025, 3, 1, tzinfo=timezone.utc),
                    valid_from=datetime(2025, 2, 1, tzinfo=timezone.utc),
                    predicate="location", object_value="Bangalore", version=2,
                    is_supersession=True, supersedes_id="o1_jan"
                ),
                # Ingested SECOND, but valid in Jan
                ObservationData(
                    id="o1_jan", source_text="Lived in Delhi",
                    observed_at=datetime(2025, 3, 2, tzinfo=timezone.utc),
                    valid_from=datetime(2025, 1, 1, tzinfo=timezone.utc),
                    valid_until=datetime(2025, 2, 1, tzinfo=timezone.utc),
                    predicate="location", object_value="Delhi", version=1
                ),
            ],
        )
    )

    # -------------------------------------------------------------------------
    # Scenario 9: CONFLICTING EVIDENCE (Overlapping validity disagreement)
    # -------------------------------------------------------------------------
    scenarios.append(
        BenchmarkScenario(
            id="scenario_9_conflicting_evidence",
            name="Simultaneous Disagreeing Evidence",
            description="Verifies that active disagreeing evidence valid at the same timestamp yields CONFLICTED status.",
            subject_id="user",
            predicate="favorite_editor",
            query_timestamp=datetime(2025, 1, 15, tzinfo=timezone.utc),
            expected_status="CONFLICTED",
            expected_value=None,
            expected_lineage_depth=1,
            observations=[
                ObservationData(
                    id="o1", source_text="My editor is VS Code",
                    observed_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
                    valid_from=datetime(2025, 1, 1, tzinfo=timezone.utc),
                    object_value="VS Code", version=1, is_supersession=False
                ),
                ObservationData(
                    id="o2", source_text="My editor is Cursor",
                    observed_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
                    valid_from=datetime(2025, 1, 1, tzinfo=timezone.utc),
                    object_value="Cursor", version=1, is_supersession=False
                ),
            ],
        )
    )

    # -------------------------------------------------------------------------
    # Scenario 10: LONG LINEAGE (6 sequential belief transitions)
    # -------------------------------------------------------------------------
    tools = ["ToolA", "ToolB", "ToolC", "ToolD", "ToolE", "ToolF"]
    obs_long: list[ObservationData] = []
    for idx, tool in enumerate(tools):
        month = idx + 1
        prev_id = f"o_tool_{month-1}" if month > 1 else None
        obs_long.append(
            ObservationData(
                id=f"o_tool_{month}",
                source_text=f"Switched to {tool}",
                observed_at=datetime(2025, month, 1, tzinfo=timezone.utc),
                valid_from=datetime(2025, month, 1, tzinfo=timezone.utc),
                valid_until=datetime(2025, month + 1, 1, tzinfo=timezone.utc) if month < 6 else None,
                predicate="primary_tool",
                object_value=tool,
                version=month,
                is_supersession=True if prev_id else False,
                supersedes_id=prev_id,
            )
        )

    scenarios.append(
        BenchmarkScenario(
            id="scenario_10_long_lineage",
            name="Deep Lineage Chain Traversal",
            description="Evaluates historical resolution and lineage depth across 6 sequential transitions (ToolA -> ToolF).",
            subject_id="user",
            predicate="primary_tool",
            query_timestamp=datetime(2025, 3, 15, tzinfo=timezone.utc),
            expected_status="SUPPORTED",
            expected_value="ToolC",
            expected_lineage_depth=3,
            observations=obs_long,
        )
    )

    return scenarios
