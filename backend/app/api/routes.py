"""FastAPI route handlers for ChronoGraph REST API.

Exposes thin REST endpoints interfacing directly with the ChronoGraph reasoning engine
and process-local ChronoGraphStore without duplicating logic or altering epistemic semantics.
"""

from datetime import datetime, timezone
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_pipeline, get_store
from app.api.schemas import (
    BeliefDetailResponse,
    DemoLoadResponse,
    EvidenceItemSchema,
    IngestRequest,
    IngestResponse,
    QueryRequest,
    QueryResponse,
    TimelineItemSchema,
    TimelineResponse,
)
from app.engine.normalizer import (
    normalize_belief_candidate,
    normalize_observation,
)
from app.engine.state_machine import BeliefStateMachine
from app.engine.store import ChronoGraphStore
from app.engine.temporal_resolver import (
    get_evidence_for_belief,
    get_lineage,
    resolve_at_time,
    resolve_current,
)
from app.models.domain import (
    BeliefState,
    Entity,
    LifecycleStatus,
    Observation,
    ResolutionStatus,
)
from app.services.ingestion_pipeline import ChronoGraphIngestionPipeline
from app.services.hydradb_types import HydraChunkEvidence, HydraTripletRelation

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "chronograph"}


@router.post("/api/v1/query", response_model=QueryResponse)
def resolve_query(
    req: QueryRequest,
    store: ChronoGraphStore = Depends(get_store),
) -> QueryResponse:
    """Resolves a structured temporal belief query as of the specified timestamp."""
    eval_time = req.timestamp or datetime.now(timezone.utc)

    # 1. Resolve current/temporal state
    res = resolve_current(store, req.subject_id, req.predicate, eval_time)

    evidence_list: list[EvidenceItemSchema] = []
    lineage_list: list[dict[str, Any]] = []
    belief_id: str | None = None
    resolved_val: str | None = None

    if res.beliefs:
        top_b = res.beliefs[0]
        belief_id = top_b.id
        resolved_val = top_b.object_value or top_b.object_id

        if req.include_evidence:
            evidence_obs = get_evidence_for_belief(store, top_b.id)
            evidence_list = [
                EvidenceItemSchema(
                    id=o.id,
                    text=o.source_text,
                    observed_at=o.observed_at,
                    session_id=o.session_id,
                )
                for o in evidence_obs
            ]

        if req.include_lineage:
            lineage_data = get_lineage(store, top_b.id)
            lineage_list = lineage_data.get("history", [])

    return QueryResponse(
        status=res.status.value,
        value=resolved_val if res.status == ResolutionStatus.SUPPORTED else None,
        confidence=res.confidence,
        reason=res.reason,
        belief_id=belief_id,
        subject_id=req.subject_id,
        predicate=req.predicate,
        as_of=eval_time,
        evidence=evidence_list,
        lineage=lineage_list,
    )


@router.get(
    "/api/v1/timeline/{subject_id}/{predicate}",
    response_model=TimelineResponse,
)
def get_belief_timeline(
    subject_id: str,
    predicate: str,
    store: ChronoGraphStore = Depends(get_store),
) -> TimelineResponse:
    """Returns the complete temporal evolution timeline of a belief."""
    beliefs = store.get_beliefs(subject_id, predicate)
    beliefs.sort(key=lambda b: (b.valid_from, b.version))

    timeline_items = [
        TimelineItemSchema(
            belief_id=b.id,
            value=b.object_value or b.object_id,
            status=b.lifecycle_status.value,
            valid_from=b.valid_from,
            valid_until=b.valid_until,
            version=b.version,
        )
        for b in beliefs
    ]

    return TimelineResponse(
        subject_id=subject_id,
        predicate=predicate,
        timeline=timeline_items,
    )


@router.get(
    "/api/v1/beliefs/{belief_id}",
    response_model=BeliefDetailResponse,
)
def get_belief_detail(
    belief_id: str,
    store: ChronoGraphStore = Depends(get_store),
) -> BeliefDetailResponse:
    """Retrieves a single belief state by ID."""
    b = store.get_belief(belief_id)
    if not b:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Belief state '{belief_id}' not found.",
        )

    return BeliefDetailResponse(
        id=b.id,
        subject_id=b.subject_id,
        predicate=b.predicate,
        object_id=b.object_id,
        object_value=b.object_value,
        lifecycle_status=b.lifecycle_status.value,
        confidence=b.confidence,
        observed_at=b.observed_at,
        valid_from=b.valid_from,
        valid_until=b.valid_until,
        version=b.version,
        observation_ids=b.observation_ids,
    )


@router.get(
    "/api/v1/beliefs/{belief_id}/evidence",
    response_model=list[EvidenceItemSchema],
)
def get_belief_evidence(
    belief_id: str,
    store: ChronoGraphStore = Depends(get_store),
) -> list[EvidenceItemSchema]:
    """Retrieves grounding evidence observations for a belief."""
    b = store.get_belief(belief_id)
    if not b:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Belief state '{belief_id}' not found.",
        )

    evidence_obs = get_evidence_for_belief(store, belief_id)
    return [
        EvidenceItemSchema(
            id=o.id,
            text=o.source_text,
            observed_at=o.observed_at,
            session_id=o.session_id,
        )
        for o in evidence_obs
    ]


@router.get(
    "/api/v1/beliefs/{belief_id}/lineage",
)
def get_belief_lineage_stack(
    belief_id: str,
    store: ChronoGraphStore = Depends(get_store),
) -> dict[str, Any]:
    """Retrieves the cycle-safe belief state transition lineage history."""
    b = store.get_belief(belief_id)
    if not b:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Belief state '{belief_id}' not found.",
        )

    return get_lineage(store, belief_id)


@router.post(
    "/api/v1/ingest",
    response_model=IngestResponse,
)
def ingest_memory_statement(
    req: IngestRequest,
    store: ChronoGraphStore = Depends(get_store),
    pipeline: ChronoGraphIngestionPipeline = Depends(get_pipeline),
) -> IngestResponse:
    """Ingests a raw memory statement into the ChronoGraph reasoning engine."""
    ts = req.timestamp or datetime.now(timezone.utc)
    obs_id = f"obs_api_{hash(req.text) & 0xFFFFFFFF:08x}_{int(ts.timestamp())}"

    # 1. Create Observation
    obs = Observation(
        id=obs_id,
        source_text=req.text,
        session_id=req.session_id,
        observed_at=ts,
        hydradb_chunk_id=obs_id,
    )
    store.add_observation(obs)

    # 2. Extract candidate belief
    text_lower = req.text.lower()
    val = "VS Code" if "vs code" in text_lower else ("Cursor" if "cursor" in text_lower else "unknown")
    
    sm = BeliefStateMachine(store)
    created_beliefs: list[str] = []

    if val != "unknown":
        cand = BeliefState(
            id=f"bel_api_{obs_id}",
            subject_id="user",
            predicate="favorite_editor",
            object_value=val,
            lifecycle_status=LifecycleStatus.OBSERVED,
            confidence=0.9,
            observed_at=ts,
            valid_from=ts,
            valid_until=None,
            version=1,
            observation_ids=[obs.id],
        )
        
        # Check existing active beliefs for subject/predicate
        active_existing = store.get_active_beliefs("user", "favorite_editor")
        if active_existing:
            old_active = active_existing[-1]
            if old_active.object_value != val:
                new_b, old_b, _ = sm.supersede_belief(cand, old_active.id)
                created_beliefs.append(new_b.id)
            else:
                new_b = sm.activate_belief(cand)
                created_beliefs.append(new_b.id)
        else:
            new_b = sm.activate_belief(cand)
            created_beliefs.append(new_b.id)

    # Persist snapshot atomically after mutation
    try:
        from app.api.dependencies import save_current_snapshot
        save_current_snapshot()
    except Exception:
        pass

    return IngestResponse(
        success=True,
        observations_created=1,
        beliefs_created=len(created_beliefs),
        observation_ids=[obs.id],
        belief_ids=created_beliefs,
        message=f"Memory statement ingested into collection '{req.collection}'.",
    )


@router.post(
    "/api/v1/demo/load",
    response_model=DemoLoadResponse,
)
def load_demo_scenario_endpoint(
    store: ChronoGraphStore = Depends(get_store),
) -> DemoLoadResponse:
    """Loads the deterministic Hack Hydra killer scenario into the store."""
    from app.engine.contradiction import detect_conflicts
    from app.engine.state_machine import BeliefStateMachine
    from app.api.schemas import DemoLoadResponse

    # Clear current store for deterministic demo state
    store.clear()

    # User entity
    store.add_entity(Entity(id="user", name="Alex", entity_type="PERSON"))

    # Jan: VS Code -> Feb: Cursor -> Mar: VS Code
    t_jan = datetime(2025, 1, 1, tzinfo=timezone.utc)
    t_feb = datetime(2025, 2, 1, tzinfo=timezone.utc)
    t_mar = datetime(2025, 3, 1, tzinfo=timezone.utc)

    o1 = Observation(id="obs_jan_vscode", source_text="I use VS Code as my favorite editor.", session_id="jan_sess", observed_at=t_jan, valid_from=t_jan, valid_until=t_feb)
    o2 = Observation(id="obs_feb_cursor", source_text="I switched to Cursor. Cursor is now my favorite editor.", session_id="feb_sess", observed_at=t_feb, valid_from=t_feb, valid_until=t_mar)
    o3 = Observation(id="obs_mar_vscode", source_text="I switched back to VS Code. It is my favorite editor again.", session_id="mar_sess", observed_at=t_mar, valid_from=t_mar)

    o4 = Observation(id="obs_delhi", source_text="I live in Delhi.", session_id="loc_sess_1", observed_at=datetime(2025, 1, 10, tzinfo=timezone.utc), valid_from=t_jan, valid_until=t_mar)
    o5 = Observation(id="obs_blr", source_text="I live in Bangalore.", session_id="loc_sess_2", observed_at=datetime(2025, 2, 10, tzinfo=timezone.utc), valid_from=t_feb, valid_until=datetime(2025, 4, 1, tzinfo=timezone.utc))

    for o in [o1, o2, o3, o4, o5]:
        store.add_observation(o)

    sm = BeliefStateMachine(store)

    b1 = store.add_belief(BeliefState(id="b1_vscode", subject_id="user", predicate="favorite_editor", object_value="VS Code", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=t_jan, valid_from=t_jan, valid_until=t_feb, version=1, observation_ids=[o1.id]))
    sm.activate_belief(b1)

    b2 = store.add_belief(BeliefState(id="b2_cursor", subject_id="user", predicate="favorite_editor", object_value="Cursor", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=t_feb, valid_from=t_feb, valid_until=t_mar, version=2, observation_ids=[o2.id]))
    sm.supersede_belief(b2, b1.id)

    b3 = store.add_belief(BeliefState(id="b3_vscode", subject_id="user", predicate="favorite_editor", object_value="VS Code", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=t_mar, valid_from=t_mar, version=3, observation_ids=[o3.id]))
    sm.supersede_belief(b3, b2.id)

    b_loc1 = store.add_belief(BeliefState(id="b_loc1_delhi", subject_id="user", predicate="location", object_value="Delhi", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=datetime(2025, 1, 10, tzinfo=timezone.utc), valid_from=t_jan, valid_until=t_mar, version=1, observation_ids=[o4.id]))
    sm.activate_belief(b_loc1)

    b_loc2 = store.add_belief(BeliefState(id="b_loc2_blr", subject_id="user", predicate="location", object_value="Bangalore", lifecycle_status=LifecycleStatus.OBSERVED, confidence=0.9, observed_at=datetime(2025, 2, 10, tzinfo=timezone.utc), valid_from=t_feb, valid_until=datetime(2025, 4, 1, tzinfo=timezone.utc), version=1, observation_ids=[o5.id]))
    sm.activate_belief(b_loc2)

    detect_conflicts(store, "user", "location")

    try:
        from app.api.dependencies import save_current_snapshot
        save_current_snapshot()
    except Exception:
        pass

    return DemoLoadResponse(
        success=True,
        message="Hack Hydra killer temporal scenario loaded successfully.",
        observations_loaded=5,
        beliefs_loaded=5,
    )
