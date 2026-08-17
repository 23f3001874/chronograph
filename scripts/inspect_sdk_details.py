import inspect
import sys
import os

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
    import hydra_db.types as types

    print("=== SEARCH RETRIEVAL RESULT MODEL FIELDS ===")
    try:
        from hydra_db.types import SearchV2RetrievalResult
        print("SearchV2RetrievalResult fields:", list(SearchV2RetrievalResult.model_fields.keys()))
    except Exception as e:
        print("Error fetching SearchV2RetrievalResult:", e)

    try:
        from hydra_db.types import SearchV2Chunk
        print("SearchV2Chunk fields:", list(SearchV2Chunk.model_fields.keys()))
    except Exception as e:
        print("Error fetching SearchV2Chunk:", e)

    try:
        from hydra_db.types import SearchV2GraphContext
        print("SearchV2GraphContext fields:", list(SearchV2GraphContext.model_fields.keys()))
    except Exception as e:
        print("Error fetching SearchV2GraphContext:", e)

    try:
        from hydra_db.types import SearchPathTriplet
        print("SearchPathTriplet fields:", list(SearchPathTriplet.model_fields.keys()))
    except Exception as e:
        print("Error fetching SearchPathTriplet:", e)

    try:
        from hydra_db.types import IngestionV2SourceUploadResultItem
        print("IngestionV2SourceUploadResultItem fields:", list(IngestionV2SourceUploadResultItem.model_fields.keys()))
    except Exception as e:
        print("Error fetching IngestionV2SourceUploadResultItem:", e)

if __name__ == "__main__":
    main()
