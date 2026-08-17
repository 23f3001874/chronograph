"""Domain models for ChronoGraph.

Provides Pydantic schemas for Entities, Observations, BeliefStates, GraphEdges,
and ResolutionResults with strict validation rules for temporal boundaries.
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, model_validator


class LifecycleStatus(str, Enum):
    """Lifecycle status of a belief state within the system's epistemic model."""

    OBSERVED = "OBSERVED"
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    PLANNED = "PLANNED"
    CANCELLED = "CANCELLED"
    CONFLICTED = "CONFLICTED"


class EdgeType(str, Enum):
    """Relationship types supported in the ChronoGraph belief graph."""

    SUBJECT = "SUBJECT"
    OBJECT = "OBJECT"
    GROUNDED_IN = "GROUNDED_IN"
    SUPERSEDES = "SUPERSEDES"
    INVALIDATES = "INVALIDATES"
    CONTRADICTS = "CONTRADICTS"


class ResolutionStatus(str, Enum):
    """Epistemic resolution status returned by current/temporal query resolver."""

    SUPPORTED = "SUPPORTED"
    CONFLICTED = "CONFLICTED"
    UNKNOWN = "UNKNOWN"
    CANCELLED = "CANCELLED"


class Entity(BaseModel):
    """Represents a domain entity node (e.g. Person, Location, Product)."""

    id: str = Field(..., description="Unique entity identifier")
    name: str = Field(..., description="Human readable name of the entity")
    entity_type: str = Field(..., description="Category or type of the entity")


class Observation(BaseModel):
    """Represents raw source evidence from an interaction or session."""

    id: str = Field(..., description="Unique observation identifier")
    source_text: str = Field(..., description="Raw text statement from session")
    session_id: str = Field(..., description="Session or interaction ID")
    observed_at: datetime = Field(..., description="Timestamp when statement occurred")
    hydradb_chunk_id: str | None = Field(
        default=None, description="Optional associated HydraDB chunk ID"
    )


class BeliefState(BaseModel):
    """Represents a normalized, state-versioned assertion held by the system."""

    id: str = Field(..., description="Unique belief state identifier")
    subject_id: str = Field(..., description="ID of subject Entity")
    predicate: str = Field(..., description="Canonical predicate/relationship name")
    object_id: str | None = Field(
        default=None, description="ID of object Entity if entity-linked"
    )
    object_value: str | None = Field(
        default=None, description="Literal text value if scalar value"
    )
    lifecycle_status: LifecycleStatus = Field(
        ..., description="Current epistemic lifecycle status"
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0"
    )
    observed_at: datetime = Field(
        ..., description="Timestamp when evidence was observed"
    )
    valid_from: datetime = Field(
        ..., description="Timestamp marking start of temporal validity"
    )
    valid_until: datetime | None = Field(
        default=None, description="Timestamp marking end of temporal validity"
    )
    version: int = Field(..., ge=1, description="Version number (>= 1)")
    observation_ids: list[str] = Field(
        default_factory=list, description="IDs of supporting Observations"
    )

    @model_validator(mode="after")
    def validate_object_presence_and_temporal_range(self) -> "BeliefState":
        """Ensures object payload is present and valid_until >= valid_from."""
        if not self.object_id and not self.object_value:
            raise ValueError(
                "BeliefState must have at least one of object_id or object_value specified."
            )

        if self.valid_until is not None and self.valid_until < self.valid_from:
            raise ValueError(
                f"valid_until ({self.valid_until}) must be greater than or equal to valid_from ({self.valid_from})."
            )

        return self


class GraphEdge(BaseModel):
    """Represents a directed typed relationship edge between graph nodes."""

    id: str = Field(..., description="Unique edge identifier")
    source_id: str = Field(..., description="Source node identifier")
    target_id: str = Field(..., description="Target node identifier")
    edge_type: EdgeType = Field(..., description="Edge relationship type")
    created_at: datetime = Field(..., description="Timestamp when edge was created")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Arbitrary edge metadata"
    )


class ResolutionResult(BaseModel):
    """Structured result returned by the temporal state resolver."""

    status: ResolutionStatus = Field(..., description="Resolution outcome status")
    beliefs: list[BeliefState] = Field(
        default_factory=list, description="Resolved belief states"
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Overall resolution confidence"
    )
    reason: str = Field(..., description="Human readable resolution explanation")
    evidence_ids: list[str] = Field(
        default_factory=list, description="IDs of supporting observations"
    )
