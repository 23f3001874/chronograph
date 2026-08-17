"""Internal typed Data Transfer Objects (DTOs) for HydraDB Cloud SDK responses.

Encapsulates raw SDK responses into typed schemas used across ChronoGraph.
"""

from typing import Any
from pydantic import BaseModel, Field


class HydraMemoryResultItem(BaseModel):
    """Represents the status of an ingested memory item."""

    id: str = Field(..., description="Memory source item ID")
    status: str = Field(..., description="Ingestion status (queued, completed, etc.)")
    error_code: str | None = Field(default=None, description="Optional error code")
    error_message: str | None = Field(default=None, description="Optional error message")


class HydraTripletRelation(BaseModel):
    """Represents an entity-predicate-entity triplet extracted by HydraDB graph inference."""

    source_entity_name: str = Field(..., description="Source entity name/identifier")
    source_entity_type: str = Field(..., description="Source entity category (PERSON, etc.)")
    raw_predicate: str = Field(..., description="Raw predicate string extracted from text")
    canonical_predicate: str = Field(..., description="Normalized predicate name")
    target_entity_name: str = Field(..., description="Target entity name/value")
    target_entity_type: str = Field(..., description="Target entity category (LOCATION, etc.)")
    temporal_details: str | None = Field(default=None, description="Extracted temporal string (e.g. 2025-02-01)")
    timestamp: float | None = Field(default=None, description="Extracted unix timestamp if present")
    chunk_id: str | None = Field(default=None, description="Associated source chunk ID")


class HydraChunkEvidence(BaseModel):
    """Represents a text chunk and associated metadata retrieved from HydraDB."""

    id: str = Field(..., description="Chunk source ID")
    chunk_uuid: str = Field(..., description="Unique chunk UUID in HydraDB")
    chunk_content: str = Field(..., description="Raw text content of the chunk")
    relevancy_score: float = Field(..., description="Similarity/relevance score")
    source_title: str | None = Field(default=None, description="Source title")
    source_type: str | None = Field(default=None, description="Source category (memory, etc.)")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Tenant schema metadata")
    additional_metadata: dict[str, Any] = Field(default_factory=dict, description="Free-form metadata dict")


class HydraQueryResult(BaseModel):
    """Represents the consolidated response from a HydraDB query."""

    database: str = Field(..., description="Target database name")
    collection: str = Field(..., description="Target collection partition")
    chunks: list[HydraChunkEvidence] = Field(default_factory=list, description="Retrieved text chunks")
    triplets: list[HydraTripletRelation] = Field(default_factory=list, description="Extracted graph triplets")
    additional_context: str | None = Field(default=None, description="Optional extra context string")
