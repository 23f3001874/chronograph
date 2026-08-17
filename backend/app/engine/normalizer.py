"""Normalization pipeline for ChronoGraph.

Transforms HydraDB DTO responses into ChronoGraph domain objects (Observation and
BeliefState candidates in OBSERVED status) without fabricating timestamps or
automatically mutating belief states into truth.
"""

from datetime import datetime, timezone
from typing import Any

from app.models.domain import (
    BeliefState,
    LifecycleStatus,
    Observation,
)
from app.services.hydradb_types import (
    HydraChunkEvidence,
    HydraQueryResult,
    HydraTripletRelation,
)


def _parse_iso_timestamp(ts_val: Any) -> datetime | None:
    """Safely parses string/float ISO timestamp into timezone-aware datetime."""
    if not ts_val:
        return None

    if isinstance(ts_val, datetime):
        if ts_val.tzinfo is None:
            return ts_val.replace(tzinfo=timezone.utc)
        return ts_val

    if isinstance(ts_val, (int, float)):
        try:
            return datetime.fromtimestamp(ts_val, tz=timezone.utc)
        except Exception:
            return None

    if isinstance(ts_val, str):
        try:
            clean_str = ts_val.strip()
            if clean_str.endswith("Z"):
                clean_str = clean_str[:-1] + "+00:00"
            dt = datetime.fromisoformat(clean_str)
            if dt.tzinfo is None:
                return dt.replace(tzinfo=timezone.utc)
            return dt
        except Exception:
            return None

    return None



def normalize_observation(
    chunk: HydraChunkEvidence,
    session_id: str | None = None,
    observed_at: datetime | None = None,
) -> Observation:
    """Transforms a HydraDB chunk DTO into a ChronoGraph Observation domain object.

    Raises ValueError if a valid timestamp cannot be established. Never fabricates dates.
    """
    if not chunk.chunk_content or not chunk.chunk_content.strip():
        raise ValueError(f"Cannot normalize chunk {chunk.id}: source text is empty.")

    # 1. Establish observation ID & chunk UUID
    obs_id = chunk.id or chunk.chunk_uuid
    if not obs_id or obs_id == "unknown":
        raise ValueError("Cannot normalize chunk: missing valid source ID or chunk_uuid.")

    # 2. Extract session_id
    sess_id = (
        chunk.additional_metadata.get("session_id")
        or chunk.metadata.get("session_id")
        or session_id
        or "unknown_session"
    )

    # 3. Establish timestamp (NO fabrication)
    ts = (
        _parse_iso_timestamp(chunk.additional_metadata.get("timestamp"))
        or _parse_iso_timestamp(chunk.additional_metadata.get("observed_at"))
        or _parse_iso_timestamp(chunk.metadata.get("timestamp"))
        or _parse_iso_timestamp(observed_at)
    )

    if ts is None:
        raise ValueError(
            f"Cannot establish observation timestamp for chunk '{obs_id}'. "
            "HydraDB metadata lacks valid timestamp and no fallback was supplied."
        )

    return Observation(
        id=str(obs_id),
        source_text=chunk.chunk_content,
        session_id=str(sess_id),
        observed_at=ts,
        hydradb_chunk_id=chunk.chunk_uuid,
    )


def normalize_belief_candidate(
    triplet: HydraTripletRelation,
    observation: Observation,
    default_subject_id: str = "user",
    confidence: float = 0.8,
) -> BeliefState:
    """Transforms a HydraDB extracted triplet into a ChronoGraph candidate BeliefState.

    Candidate is ALWAYS initialized in status OBSERVED.
    Does NOT automatically mark as ACTIVE or TRUTH.
    """
    subject = triplet.source_entity_name or default_subject_id
    predicate = triplet.canonical_predicate or triplet.raw_predicate or "related_to"
    target_val = triplet.target_entity_name or "unknown"

    # Establish valid_from from temporal_details if present, else fallback to observation.observed_at
    valid_from_dt = _parse_iso_timestamp(triplet.temporal_details) or observation.observed_at

    if valid_from_dt is None:
        raise ValueError(
            f"Cannot establish valid_from timestamp for triplet on predicate '{predicate}'."
        )

    belief_id = f"bel_cand_{observation.id}_{predicate}_{hash(target_val) & 0xFFFFFFFF:08x}"

    return BeliefState(
        id=belief_id,
        subject_id=subject.lower(),
        predicate=predicate.lower(),
        object_value=target_val,
        lifecycle_status=LifecycleStatus.OBSERVED,
        confidence=confidence,
        observed_at=observation.observed_at,
        valid_from=valid_from_dt,
        valid_until=None,
        version=1,
        observation_ids=[observation.id],
    )


def normalize_graph_context(query_result: HydraQueryResult) -> list[HydraTripletRelation]:
    """Extracts graph relations from HydraQueryResult as external evidence context.

    Note: HydraDB graph relations are NOT automatically converted into ChronoGraph
    SUPERSEDES, INVALIDATES, or CONTRADICTS semantic edges.
    """
    return query_result.triplets
