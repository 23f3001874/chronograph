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

def inspect_sdk():
    load_dotenv()
    import hydra_db
    from hydra_db import HydraDB

    print("=== HYDRADB PACKAGE INFO ===")
    print("Package file:", hydra_db.__file__)
    print("Package version:", getattr(hydra_db, "__version__", "2.1.2"))

    print("\n=== HYDRADB CLIENT SIGNATURE ===")
    print("HydraDB.__init__:", inspect.signature(HydraDB.__init__))

    api_key = os.environ.get("HYDRA_DB_API_KEY", "dummy_key")
    client = HydraDB(token=api_key)

    resources = {
        "client.databases": client.databases,
        "client.context": client.context,
        "client": client, # for query/feedback if attached directly
    }

    for name, obj in resources.items():
        print(f"\n=== RESOURCE: {name} ===")
        methods = [m for m in dir(obj) if not m.startswith("_")]
        for m in methods:
            func = getattr(obj, m)
            if callable(func):
                try:
                    sig = inspect.signature(func)
                    print(f"  {m}{sig}")
                except Exception as e:
                    print(f"  {m}: signature error {e}")

if __name__ == "__main__":
    inspect_sdk()
