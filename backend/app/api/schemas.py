"""Pydantic API request and response schemas for ChronoGraph REST endpoints."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request schema for temporal belief query resolution."""

    subject_id: str = Field(..., description="Target entity ID (e.g. 'user' or 'ent_user')")
    predicate: str = Field(..., description="Target predicate attribute (e.g. 'favorite_editor')")
    timestamp: datetime | None = Field(
        default=None, description="Optional point-in-time timestamp (ISO-8601). Defaults to current time."
    )
    include_evidence: bool = Field(default=True, description="Whether to include grounded evidence observations.")
    include_lineage: bool = Field(default=False, description="Whether to include transition lineage stack.")


class EvidenceItemSchema(BaseModel):
    """Grounded evidence observation item."""

    id: str = Field(..., description="Observation identifier")
    text: str = Field(..., description="Source statement text")
    observed_at: datetime = Field(..., description="Timestamp when evidence was observed")
    session_id: str = Field(..., description="Session identifier")


class QueryResponse(BaseModel):
    """Structured response object for temporal belief queries."""

    status: str = Field(..., description="Resolution status (SUPPORTED, CONFLICTED, UNKNOWN, CANCELLED)")
    value: str | None = Field(default=None, description="Resolved scalar attribute value")
    confidence: float = Field(..., description="Resolution confidence score (0.0 to 1.0)")
    reason: str = Field(..., description="Human readable explanation")
    belief_id: str | None = Field(default=None, description="ID of resolved active belief")
    subject_id: str = Field(..., description="Subject entity identifier")
    predicate: str = Field(..., description="Predicate attribute name")
    as_of: datetime = Field(..., description="Effective query evaluation timestamp")
    evidence: list[EvidenceItemSchema] = Field(default_factory=list, description="Supporting evidence observations")
    lineage: list[dict[str, Any]] = Field(default_factory=list, description="Belief state transition history")


class TimelineItemSchema(BaseModel):
    """Single timeline entry representing belief evolution."""

    belief_id: str = Field(..., description="Belief state ID")
    value: str | None = Field(default=None, description="Scalar attribute value")
    status: str = Field(..., description="Epistemic status (ACTIVE, SUPERSEDED, CANCELLED, CONFLICTED)")
    valid_from: datetime = Field(..., description="Start of temporal validity")
    valid_until: datetime | None = Field(default=None, description="End of temporal validity (None = ongoing)")
    version: int = Field(..., description="State version number")


class TimelineResponse(BaseModel):
    """Complete temporal evolution timeline for a subject-predicate attribute."""

    subject_id: str = Field(..., description="Subject entity ID")
    predicate: str = Field(..., description="Predicate attribute name")
    timeline: list[TimelineItemSchema] = Field(default_factory=list, description="Ordered timeline entries")


class BeliefDetailResponse(BaseModel):
    """Detailed view of a single belief state."""

    id: str = Field(..., description="Belief state ID")
    subject_id: str = Field(..., description="Subject entity ID")
    predicate: str = Field(..., description="Predicate attribute name")
    object_id: str | None = Field(default=None, description="Object entity ID")
    object_value: str | None = Field(default=None, description="Literal object value")
    lifecycle_status: str = Field(..., description="Current epistemic status")
    confidence: float = Field(..., description="Confidence score")
    observed_at: datetime = Field(..., description="Observation timestamp")
    valid_from: datetime = Field(..., description="Validity start timestamp")
    valid_until: datetime | None = Field(default=None, description="Validity end timestamp")
    version: int = Field(..., description="Version number")
    observation_ids: list[str] = Field(default_factory=list, description="IDs of supporting observations")


class IngestRequest(BaseModel):
    """Request schema for ingesting a memory statement into ChronoGraph."""

    collection: str = Field(..., description="Target collection partition name")
    session_id: str = Field(default="default_session", description="Session identifier")
    text: str = Field(..., description="Raw memory statement text")
    timestamp: datetime | None = Field(default=None, description="Optional observation timestamp")


class IngestResponse(BaseModel):
    """Response schema for memory ingestion."""

    success: bool = Field(..., description="Whether ingestion completed successfully")
    observations_created: int = Field(..., description="Number of observations created")
    beliefs_created: int = Field(..., description="Number of candidate beliefs created")
    observation_ids: list[str] = Field(default_factory=list, description="IDs of created observations")
    belief_ids: list[str] = Field(default_factory=list, description="IDs of created belief states")
    message: str = Field(..., description="Human readable summary message")


class DemoLoadResponse(BaseModel):
    """Response schema for loading demo scenario."""

    success: bool = Field(..., description="Whether demo scenario was loaded")
    message: str = Field(..., description="Summary message")
    observations_loaded: int = Field(..., description="Count of observations loaded")
    beliefs_loaded: int = Field(..., description="Count of belief states populated")
