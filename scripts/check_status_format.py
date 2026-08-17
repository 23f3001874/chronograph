import os
import time

env_file = r"C:\Users\91877\chronograph\.env"
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip("\"'")

import sys
backend_path = os.path.join(os.path.dirname(__file__), "..", "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.services.hydradb_service import HydraDBService
service = HydraDBService()

coll = f"status_check_{int(time.time())}"
m_id = f"mem_st_{int(time.time())}"
service.ingest_memory(collection=coll, memories=[{"id": m_id, "text": "Testing status response shape."}])

for i in range(5):
    res = service.get_memory_status(collection=coll, memory_ids=[m_id])
    print(f"Status check {i}:", res)
    time.sleep(2.0)
