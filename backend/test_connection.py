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

def sanitize_error(e):
    msg = str(e)
    if "sk_live" in msg or "Bearer" in msg:
        return f"{type(e).__name__}: [credential detected - hidden]"
    return f"{type(e).__name__}: {msg[:100]}"

def main():
    load_dotenv()

    # 1. Verify SDK installation
    try:
        from hydra_db import HydraDB
        print("SDK installed successfully")
    except ImportError as e:
        print("SDK installed failed")
        print(f"ERRORS: Could not import hydra_db: {sanitize_error(e)}")
        sys.exit(1)

    # 2. Check environment variable securely
    api_key = os.environ.get("HYDRA_DB_API_KEY")
    if not api_key:
        print("Client initialized: failed (HYDRA_DB_API_KEY environment variable is missing)")
        print("Authentication: failed")
        print("Test write: failed")
        print("Test retrieval: failed")
        print("ERRORS: HYDRA_DB_API_KEY environment variable is not set")
        sys.exit(0)

    # 3. Client initialization
    try:
        client = HydraDB(token=api_key)
        print("Client initialized successfully")
    except Exception as e:
        print("Client initialized: failed")
        print("Authentication: failed")
        print("Test write: failed")
        print("Test retrieval: failed")
        print(f"ERRORS: {sanitize_error(e)}")
        sys.exit(1)

    # 4. Authentication & Database readiness
    test_db = "chronograph_smoke_test"
    try:
        db_list_res = client.databases.list()
        print("Authentication succeeded")
    except Exception as e:
        print("Authentication failed")
        print("Test write: failed")
        print("Test retrieval: failed")
        print(f"ERRORS: {sanitize_error(e)}")
        sys.exit(1)

    # Find existing ready database or create & wait for readiness
    try:
        target_db = None
        # Check existing databases
        if hasattr(db_list_res, 'data') and hasattr(db_list_res.data, 'databases') and db_list_res.data.databases:
            target_db = db_list_res.data.databases[0]
        elif hasattr(db_list_res, 'data') and isinstance(db_list_res.data, list) and db_list_res.data:
            target_db = db_list_res.data[0]

        if not target_db:
            target_db = test_db
            try:
                client.databases.create(database=target_db)
            except Exception:
                pass
        
        # Poll readiness (up to 15s)
        for _ in range(6):
            try:
                st = client.databases.status(database=target_db)
                if hasattr(st, 'data') and hasattr(st.data, 'infra') and st.data.infra.ready_for_ingestion:
                    break
            except Exception:
                pass
            time.sleep(2.5)

        # 5. Ingest 1 test memory
        ingest_res = client.context.ingest(
            type="memory",
            database=target_db,
            collection="smoke_test_coll",
            memories=json.dumps([
                {
                    "id": "smoke_test_001",
                    "text": "Chronograph smoke test verification entry.",
                    "infer": False
                }
            ])
        )
        print("Test write succeeded")
    except Exception as e:
        print("Test write failed")
        print("Test retrieval: failed")
        print(f"ERRORS: {sanitize_error(e)}")
        sys.exit(1)

    # 6. Test retrieval
    try:
        # Give indexing a moment if needed
        time.sleep(2)
        res = client.query(
            database=target_db,
            collection="smoke_test_coll",
            query="smoke test",
            type="memory"
        )
        print("Test retrieval succeeded")
        print("ERRORS: None")
    except Exception as e:
        print("Test retrieval failed")
        print(f"ERRORS: {sanitize_error(e)}")

if __name__ == "__main__":
    main()
