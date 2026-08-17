"""HydraDB Cloud API adapter service for ChronoGraph.

Encapsulates all interaction with the hydradb-sdk (v2.1.2) while enforcing collection
isolation, configuration validation, and DTO transformation.
"""

import json
import os
from typing import Any, Literal

from app.services.hydradb_types import (
    HydraChunkEvidence,
    HydraMemoryResultItem,
    HydraQueryResult,
    HydraTripletRelation,
)


def load_dotenv():
    """Attempts to load .env from parent directory if present."""
    env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    val = val.strip("\"'")
                    os.environ[key.strip()] = val


class HydraDBService:
    """Service wrapper for HydraDB Cloud SDK operations."""

    def __init__(self, api_key: str | None = None, database: str | None = None) -> None:
        load_dotenv()
        self.api_key = api_key if api_key is not None else os.environ.get("HYDRA_DB_API_KEY")
        self.database = database if database is not None else os.environ.get("HYDRA_DB_DATABASE", "chronograph_exp_db")

        if not self.api_key:
            raise ValueError(
                "HYDRA_DB_API_KEY is missing. Configure it in .env or pass it explicitly to HydraDBService."
            )
        if not self.database or not self.database.strip():
            raise ValueError("HYDRA_DB_DATABASE configuration is missing.")

        # Lazy client instantiation to facilitate unit testing with mocks
        self._client = None

    @property
    def client(self):
        """Lazily initializes and returns the HydraDB client instance."""
        if self._client is None:
            try:
                from hydra_db import HydraDB
                self._client = HydraDB(token=self.api_key)
            except ImportError as e:
                raise RuntimeError(f"Could not import hydra_db package: {e}")
        return self._client

    def _validate_collection(self, collection: str) -> None:
        """Enforces that collection is explicitly provided to prevent cross-user leakage."""
        if not collection or not collection.strip():
            raise ValueError("Explicit collection partition identifier is required for isolation.")

    def ingest_memory(
        self,
        *,
        collection: str,
        memories: list[dict[str, Any]],
        infer: bool = True,
        custom_instructions: str | None = None,
    ) -> list[HydraMemoryResultItem]:
        """Ingests a list of memory dict items into the specified collection."""
        self._validate_collection(collection)
        if not memories:
            return []

        # Format memory payloads ensuring infer flag and optional instructions
        formatted_memories = []
        for mem in memories:
            item = dict(mem)
            if "infer" not in item:
                item["infer"] = infer
            if custom_instructions and "custom_instructions" not in item:
                item["custom_instructions"] = custom_instructions
            formatted_memories.append(item)

        response = self.client.context.ingest(
            type="memory",
            database=self.database,
            collection=collection,
            memories=json.dumps(formatted_memories),
        )

        results: list[HydraMemoryResultItem] = []
        data = getattr(response, "data", response)
        raw_results = getattr(data, "results", [])

        for r in raw_results:
            results.append(
                HydraMemoryResultItem(
                    id=getattr(r, "id", "unknown"),
                    status=getattr(r, "status", "unknown"),
                    error_code=getattr(r, "error_code", None),
                    error_message=getattr(r, "error", None),
                )
            )

        return results

    def query_memory(
        self,
        *,
        collection: str,
        query: str,
        mode: Literal["fast", "thinking"] = "thinking",
        max_results: int = 10,
        graph_context: bool = True,
        recency_bias: float | None = None,
    ) -> HydraQueryResult:
        """Queries memories from the specified collection, returning a HydraQueryResult DTO."""
        self._validate_collection(collection)
        if not query or not query.strip():
            raise ValueError("Query string cannot be empty.")

        response = self.client.query(
            database=self.database,
            collection=collection,
            query=query,
            type="memory",
            query_by="hybrid",
            mode=mode,
            max_results=max_results,
            graph_context=graph_context,
            recency_bias=recency_bias,
        )

        data = getattr(response, "data", response)

        # 1. Parse chunks
        chunks: list[HydraChunkEvidence] = []
        raw_chunks = getattr(data, "chunks", []) or []
        for c in raw_chunks:
            chunks.append(
                HydraChunkEvidence(
                    id=getattr(c, "id", getattr(c, "chunk_uuid", "unknown")),
                    chunk_uuid=getattr(c, "chunk_uuid", getattr(c, "id", "unknown")),
                    chunk_content=getattr(c, "chunk_content", ""),
                    relevancy_score=float(getattr(c, "relevancy_score", 0.0)),
                    source_title=getattr(c, "source_title", None),
                    source_type=getattr(c, "source_type", None),
                    metadata=getattr(c, "metadata", {}) or {},
                    additional_metadata=getattr(c, "additional_metadata", {}) or {},
                )
            )

        # 2. Parse triplets from graph_context
        triplets: list[HydraTripletRelation] = []
        g_ctx = getattr(data, "graph_context", None)
        if g_ctx:
            chunk_rels = getattr(g_ctx, "chunk_relations", []) or []
            for path_res in chunk_rels:
                path_triplets = getattr(path_res, "triplets", []) or []
                for t in path_triplets:
                    src = getattr(t, "source", {}) or {}
                    tgt = getattr(t, "target", {}) or {}
                    rel = getattr(t, "relation", {}) or {}

                    # Safe dictionary / object property access
                    src_name = getattr(src, "name", src.get("name") if isinstance(src, dict) else "unknown")
                    src_type = getattr(src, "type", src.get("type") if isinstance(src, dict) else "CONCEPT")
                    tgt_name = getattr(tgt, "name", tgt.get("name") if isinstance(tgt, dict) else "unknown")
                    tgt_type = getattr(tgt, "type", tgt.get("type") if isinstance(tgt, dict) else "CONCEPT")

                    raw_pred = getattr(rel, "raw_predicate", rel.get("raw_predicate") if isinstance(rel, dict) else "related_to")
                    can_pred = getattr(rel, "canonical_predicate", rel.get("canonical_predicate") if isinstance(rel, dict) else raw_pred)
                    temp_det = getattr(rel, "temporal_details", rel.get("temporal_details") if isinstance(rel, dict) else None)
                    t_stamp = getattr(rel, "timestamp", rel.get("timestamp") if isinstance(rel, dict) else None)
                    c_id = getattr(rel, "chunk_id", rel.get("chunk_id") if isinstance(rel, dict) else None)

                    triplets.append(
                        HydraTripletRelation(
                            source_entity_name=str(src_name or "unknown"),
                            source_entity_type=str(src_type or "CONCEPT"),
                            raw_predicate=str(raw_pred or "related_to"),
                            canonical_predicate=str(can_pred or raw_pred or "related_to"),
                            target_entity_name=str(tgt_name or "unknown"),
                            target_entity_type=str(tgt_type or "CONCEPT"),
                            temporal_details=temp_det,
                            timestamp=float(t_stamp) if t_stamp is not None else None,
                            chunk_id=c_id,
                        )
                    )

        add_ctx = getattr(data, "additional_context", None)

        return HydraQueryResult(
            database=self.database,
            collection=collection,
            chunks=chunks,
            triplets=triplets,
            additional_context=str(add_ctx) if add_ctx else None,
        )

    def inspect_memory(self, *, collection: str, memory_id: str, mode: str | None = None) -> dict[str, Any]:
        """Inspects source content of a memory ID."""
        self._validate_collection(collection)
        response = self.client.context.inspect(
            id=memory_id,
            database=self.database,
            collection=collection,
            mode=mode,
        )
        data = getattr(response, "data", response)
        return {"id": memory_id, "data": data}

    def get_memory_status(self, *, collection: str, memory_ids: list[str]) -> list[dict[str, Any]]:
        """Retrieves processing statuses for specified memory IDs."""
        self._validate_collection(collection)
        response = self.client.context.status(
            database=self.database,
            collection=collection,
            ids=memory_ids,
        )
        data = getattr(response, "data", response)
        raw_statuses = getattr(data, "statuses", []) or []
        res = []
        for s in raw_statuses:
            res.append({
                "id": getattr(s, "id", "unknown"),
                "status": getattr(s, "indexing_status", getattr(s, "status", "unknown")),
                "error_code": getattr(s, "error_code", None),
            })
        return res

    def delete_memory(self, *, collection: str, memory_ids: list[str]) -> bool:
        """Deletes specified memory IDs from the collection."""
        self._validate_collection(collection)
        if not memory_ids:
            return True
        response = self.client.context.delete(
            type="memory",
            database=self.database,
            collection=collection,
            ids=memory_ids,
        )
        data = getattr(response, "data", response)
        return bool(getattr(data, "success", True))

    def get_relations(self, *, collection: str, memory_id: str, limit: int = 50) -> list[dict[str, Any]]:
        """Retrieves explicit relations for a memory ID."""
        self._validate_collection(collection)
        response = self.client.context.relations(
            database=self.database,
            collection=collection,
            id=memory_id,
            type="memory",
            limit=limit,
        )
        data = getattr(response, "data", response)
        return getattr(data, "relations", []) or []
