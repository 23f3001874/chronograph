import os
import sys
import json
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
    from hydra_db import HydraDB
    api_key = os.environ.get("HYDRA_DB_API_KEY")
    if not api_key:
        print("API Key missing.")
        sys.exit(1)

    client = HydraDB(token=api_key)
    print("=== HYDRA_DB SDK INTROSPECTION ===")
    print("Client attributes:", [m for m in dir(client) if not m.startswith("_")])
    print("Context methods:", [m for m in dir(client.context) if not m.startswith("_")])
    print("Databases methods:", [m for m in dir(client.databases) if not m.startswith("_")])

    db_name = "chronograph_exp_db"
    coll_name = "temporal_experiment"

    # 1. Provision DB & Wait for Readiness
    try:
        client.databases.create(database=db_name)
    except Exception:
        pass

    print("\n=== WAITING FOR DB INFRASTRUCTURE READINESS ===")
    for _ in range(10):
        try:
            st = client.databases.status(database=db_name)
            if hasattr(st, 'data') and hasattr(st.data, 'infra') and st.data.infra.ready_for_ingestion:
                print("DB Infra Ready!")
                break
        except Exception as e:
            pass
        time.sleep(2)

    # 2. Ingest Synthetic Sessions with timestamps & explicit session markers
    sessions = [
        {"id": "sess_1", "text": "Session 1 (2025-01-01): My favorite editor is VS Code.", "infer": True, "additional_metadata": {"session": 1, "timestamp": "2025-01-01"}},
        {"id": "sess_2", "text": "Session 2 (2025-02-01): I've started using Cursor.", "infer": True, "additional_metadata": {"session": 2, "timestamp": "2025-02-01"}},
        {"id": "sess_3", "text": "Session 3 (2025-03-01): Actually, I'm back to VS Code.", "infer": True, "additional_metadata": {"session": 3, "timestamp": "2025-03-01"}},
        {"id": "sess_4", "text": "Session 4 (2025-04-01): I might switch to Zed next month.", "infer": True, "additional_metadata": {"session": 4, "timestamp": "2025-04-01"}},
        {"id": "sess_5", "text": "Session 5 (2025-05-01): I live in Delhi.", "infer": True, "additional_metadata": {"session": 5, "timestamp": "2025-05-01"}},
        {"id": "sess_6", "text": "Session 6 (2025-06-01): I'm planning to move to Bangalore.", "infer": True, "additional_metadata": {"session": 6, "timestamp": "2025-06-01"}},
        {"id": "sess_7", "text": "Session 7 (2025-07-01): The Bangalore move was cancelled.", "infer": True, "additional_metadata": {"session": 7, "timestamp": "2025-07-01"}},
        {"id": "sess_8", "text": "Session 8 (2025-08-01): I'll remain in Delhi.", "infer": True, "additional_metadata": {"session": 8, "timestamp": "2025-08-01"}}
    ]

    print("\n=== INGESTING SYNTHETIC MEMORIES ===")
    ingest_res = client.context.ingest(
        type="memory",
        database=db_name,
        collection=coll_name,
        memories=json.dumps(sessions)
    )
    print("Ingest raw result:", ingest_res)

    ingest_ids = [s["id"] for s in sessions]
    if hasattr(ingest_res, 'data') and hasattr(ingest_res.data, 'results'):
        ingest_ids = [r.id for r in ingest_res.data.results]

    print("\n=== WAITING FOR INDEXING STATUS ===")
    for _ in range(12):
        try:
            status_res = client.context.status(
                database=db_name,
                collection=coll_name,
                ids=ingest_ids
            )
            statuses = [s.indexing_status for s in status_res.data.statuses] if hasattr(status_res, 'data') else []
            print("Indexing statuses:", statuses)
            if all(s in ["graph_creation", "completed"] for s in statuses):
                print("All items indexed!")
                break
        except Exception as e:
            print("Status poll exception:", e)
        time.sleep(3)

    # 3. Test Questions A through J
    questions = {
        "A": "What is the user's current favorite editor?",
        "B": "What editors has the user used over time?",
        "C": "What was the user's favorite editor before they returned to VS Code?",
        "D": "Where does the user currently live?",
        "E": "Did the user ever plan to move to Bangalore?",
        "F": "What happened to the Bangalore move?",
        "G": "What is the user's favorite programming language?",
        "H": "What facts about the user changed over time?",
        "I": "Show the evidence supporting the current location.",
        "J": "What did the system previously believe that is no longer true?"
    }

    print("\n=== EXECUTING TEST QUESTIONS (A-J) ===")
    results_summary = {}
    for letter, q in questions.items():
        print(f"\n--- Question {letter}: '{q}' ---")
        try:
            res = client.query(
                database=db_name,
                collection=coll_name,
                query=q,
                type="memory",
                query_by="hybrid",
                mode="thinking",
                graph_context=True
            )
            data = res.data if hasattr(res, 'data') else res
            
            chunks = []
            if hasattr(data, 'chunks') and data.chunks:
                for c in data.chunks:
                    chunk_text = getattr(c, 'chunk_content', str(c))
                    score = getattr(c, 'relevancy_score', None)
                    chunks.append({"content": chunk_text, "score": score})
            
            graph_ctx = {}
            if hasattr(data, 'graph_context') and data.graph_context:
                g = data.graph_context
                graph_ctx = {
                    "query_paths": getattr(g, 'query_paths', []),
                    "chunk_relations": getattr(g, 'chunk_relations', []),
                    "chunk_id_to_group_ids": getattr(g, 'chunk_id_to_group_ids', {})
                }

            results_summary[letter] = {
                "question": q,
                "chunks_returned": len(chunks),
                "top_chunks": chunks[:3],
                "graph_context": graph_ctx
            }
            print(f"Top Chunks ({len(chunks)} total):")
            for c in chunks[:3]:
                print(f"  - [{c['score']}] {c['content']}")
            print("Graph Context:", graph_ctx)
        except Exception as e:
            print(f"Query error: {e}")
            results_summary[letter] = {"question": q, "error": str(e)}

    # 4. Investigate Graph Relations Endpoint
    print("\n=== INVESTIGATING CLIENT.CONTEXT.RELATIONS ENDPOINT ===")
    for item_id in ingest_ids[:3]:
        try:
            rel_res = client.context.relations(
                database=db_name,
                id=item_id,
                type="memory"
            )
            print(f"Relations for {item_id}:", rel_res)
        except Exception as e:
            print(f"Relations call failed for {item_id}: {e}")

    # Output full summary to file for complete auditing
    audit_file = os.path.join(os.path.dirname(__file__), "experiment_results.json")
    with open(audit_file, "w", encoding="utf-8") as f:
        json.dump(results_summary, f, indent=2, default=str)
    print(f"\nFull experiment results saved to: {audit_file}")

if __name__ == "__main__":
    main()
