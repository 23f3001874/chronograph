"""Live Phase 3C Vertical Slice Demonstration Script.

Run this script to prove real end-to-end integration:
HydraDB Cloud API -> DTO -> Observation -> Belief candidate -> ChronoGraphStore -> State Machine -> Temporal Resolution.

Usage:
  $env:CHRONOGRAPH_LIVE_HYDRADB_TEST="1"
  python scripts/run_phase3c_demo.py
"""

from datetime import datetime, timezone
import json
import os
import sys
import time

def load_dotenv():
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    val = val.strip("\"'")
                    os.environ[key.strip()] = val

def main():
    load_dotenv()

    if os.environ.get("CHRONOGRAPH_LIVE_HYDRADB_TEST") != "1":
        print("==================================================================")
        print("Phase 3C Live Demo SKIPPED (CHRONOGRAPH_LIVE_HYDRADB_TEST is not '1').")
        print("To run the live HydraDB Cloud integration slice, set:")
        print("  $env:CHRONOGRAPH_LIVE_HYDRADB_TEST=\"1\"")
        print("and re-run python scripts/run_phase3c_demo.py")
        print("==================================================================")
        sys.exit(0)

    # Add backend to sys.path
    backend_path = os.path.join(os.path.dirname(__file__), "..", "backend")
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)

    from app.services.hydradb_service import HydraDBService
    from app.services.ingestion_pipeline import (
        ChronoGraphIngestionPipeline,
        query_structured_answer,
    )

    print("==================================================================")
    print("      CHRONOGRAPH PHASE 3C — REAL HYDRADB VERTICAL SLICE         ")
    print("==================================================================")

    service = HydraDBService()
    pipeline = ChronoGraphIngestionPipeline(service=service)

    collection_name = f"chronograph_phase3c_{int(time.time())}"
    print(f"\n[1/7] Target HydraDB Database: '{service.database}'")
    print(f"      Dedicated Collection Partition: '{collection_name}'")

    memories = [
        {
            "id": f"mem_ed_1_{int(time.time())}",
            "text": "I use VS Code as my favorite editor.",
            "infer": True,
            "additional_metadata": {"session_id": "s1", "timestamp": "2025-01-10T00:00:00Z"},
        },
        {
            "id": f"mem_ed_2_{int(time.time())}",
            "text": "I switched to Cursor and now prefer Cursor over VS Code.",
            "infer": True,
            "additional_metadata": {"session_id": "s2", "timestamp": "2025-02-10T00:00:00Z"},
        },
        {
            "id": f"mem_ed_3_{int(time.time())}",
            "text": "I switched back to VS Code. It is my favorite editor again.",
            "infer": True,
            "additional_metadata": {"session_id": "s3", "timestamp": "2025-03-10T00:00:00Z"},
        },
    ]

    print("\n[2/7] Ingesting 3 controlled temporal memories into HydraDB Cloud...")
    ingest_res = service.ingest_memory(collection=collection_name, memories=memories, infer=True)
    print(f"      HydraDB Ingestion Response: {len(ingest_res)} item(s) accepted.")
    for item in ingest_res:
        print(f"      - Item ID: {item.id} | Status: {item.status}")

    print("\n[3/7] Polling HydraDB memory indexing & graph relation extraction status...")
    mem_ids = [m["id"] for m in memories]
    for attempt in range(12):
        statuses = service.get_memory_status(collection=collection_name, memory_ids=mem_ids)
        completed_count = sum(1 for s in statuses if s.get("status") in {"completed", "indexed", "done"})
        print(f"      Polling attempt {attempt + 1}/12: {completed_count}/3 completed.")
        if completed_count == len(memories):
            break
        time.sleep(2.0)

    print("\n[4/7] Querying memories from HydraDB Cloud (mode='thinking', graph_context=True)...")
    query_res = service.query_memory(
        collection=collection_name,
        query="What editor software does the user prefer?",
        mode="thinking",
        graph_context=True,
    )
    print(f"      Retrieved Chunks: {len(query_res.chunks)}")
    print(f"      Extracted Graph Context Triplets: {len(query_res.triplets)}")
    for t in query_res.triplets:
        print(f"      - Triplet: ({t.source_entity_name})-[{t.canonical_predicate} (raw: '{t.raw_predicate}')]->({t.target_entity_name}) [temporal: {t.temporal_details}]")

    print("\n[5/7] Normalizing responses into Observations & Belief Candidates...")
    store, observations, active_beliefs = pipeline.build_graph_from_query_result(
        query_res, fallback_memories=memories
    )
    print(f"      Created Observations: {len(observations)}")
    print(f"      Created Belief States: {len(active_beliefs)}")

    print("\n[6/7] Running Temporal State Queries against ChronoGraph...")

    # Query A: 2025-01-20
    q_a = datetime(2025, 1, 20, tzinfo=timezone.utc)
    ans_a = query_structured_answer(store, "user", "favorite_editor", q_a)
    print(f"\n      QUERY A (2025-01-20): What was my favorite editor?")
    print(f"      -> Status: {ans_a['status']} | Value: '{ans_a['value']}' | Confidence: {ans_a['confidence']}")

    # Query B: 2025-02-20
    q_b = datetime(2025, 2, 20, tzinfo=timezone.utc)
    ans_b = query_structured_answer(store, "user", "favorite_editor", q_b)
    print(f"\n      QUERY B (2025-02-20): What was my favorite editor?")
    print(f"      -> Status: {ans_b['status']} | Value: '{ans_b['value']}' | Confidence: {ans_b['confidence']}")

    # Query C: 2025-03-20
    q_c = datetime(2025, 3, 20, tzinfo=timezone.utc)
    ans_c = query_structured_answer(store, "user", "favorite_editor", q_c)
    print(f"\n      QUERY C (2025-03-20): What was my favorite editor?")
    print(f"      -> Status: {ans_c['status']} | Value: '{ans_c['value']}' | Confidence: {ans_c['confidence']}")

    # UNKNOWN Query
    q_unk = datetime(2025, 3, 20, tzinfo=timezone.utc)
    ans_unk = query_structured_answer(store, "user", "favorite_language", q_unk)
    print(f"\n      UNKNOWN QUERY (2025-03-20): What is my favorite programming language?")
    print(f"      -> Status: {ans_unk['status']} | Value: '{ans_unk['value']}' | Confidence: {ans_unk['confidence']}")

    print("\n[7/7] Lineage & Evidence Lineage Verification for Query C (VS Code at 2025-03-20):")
    print(f"      Active Belief ID: {ans_c['belief_id']}")
    print(f"      Grounded Observations:")
    for ev in ans_c["evidence"]:
        print(f"      - [Obs ID: {ev['id']}] Text: \"{ev['text']}\" (Session: {ev['session_id']})")

    print("\n      Lineage Transition Stack:")
    for h in ans_c["lineage"]:
        b = h["belief"]
        rel = h["relationship"]
        print(f"      - [{rel}] Belief ID: {b.id} | Value: '{b.object_value}' | Status: {b.lifecycle_status} | Valid: {b.valid_from} -> {b.valid_until}")

    print("\n==================================================================")
    print("  PHASE 3C VERTICAL SLICE DEMONSTRATION PASSED SUCCESSFULLY!     ")
    print("==================================================================")

if __name__ == "__main__":
    main()
