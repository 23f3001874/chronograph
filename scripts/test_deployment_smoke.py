"""Dedicated Deployment Smoke Test Script for ChronoGraph.

Verifies end-to-end REST API contract on local or live production endpoints.
Usage:
    python scripts/test_deployment_smoke.py [BASE_URL]
Example:
    python scripts/test_deployment_smoke.py https://chronograph.vercel.app
"""

from datetime import datetime, timezone
import json
import sys
from pathlib import Path
import urllib.request
import urllib.parse

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))


def http_get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "ChronoGraph-SmokeTest/1.0"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_post(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "ChronoGraph-SmokeTest/1.0"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def run_deployment_smoke_test(base_url: str | None = None) -> None:
    print("=" * 70)
    print("      CHRONOGRAPH PHASE 11 — PRODUCTION DEPLOYMENT SMOKE TEST")
    print("=" * 70)

    use_live_http = base_url is not None and base_url.startswith("http")

    if not use_live_http:
        print("\n[Mode] Running against local FastAPI TestClient...")
        from fastapi.testclient import TestClient
        from app.main import app

        client = TestClient(app)

        def get_fn(path: str) -> dict:
            r = client.get(path)
            assert r.status_code == 200, f"GET {path} failed: {r.status_code} {r.text}"
            return r.json()

        def post_fn(path: str, body: dict) -> dict:
            r = client.post(path, json=body)
            assert r.status_code == 200, f"POST {path} failed: {r.status_code} {r.text}"
            return r.json()

    else:
        clean_url = base_url.rstrip("/")
        print(f"\n[Mode] Running HTTP smoke test against live target: {clean_url}")

        def get_fn(path: str) -> dict:
            return http_get(f"{clean_url}{path}")

        def post_fn(path: str, body: dict) -> dict:
            return http_post(f"{clean_url}{path}", body)

    # 1. Health Check
    print("\n[1/8] Checking GET /health...")
    h = get_fn("/health")
    assert h.get("status") == "ok"
    print(f"      - Health Response: {h} (PASS)")

    # 2. Demo Load
    print("[2/8] Loading Demo Scenario (POST /api/v1/demo/load)...")
    demo_res = post_fn("/api/v1/demo/load", {})
    assert demo_res.get("success") is True
    print(f"      - Demo Load: {demo_res.get('message')} (PASS)")

    # 3. Point-in-Time Temporal Query (SUPPORTED)
    print("[3/8] Resolving Query Jan 20 (POST /api/v1/query)...")
    q1 = post_fn(
        "/api/v1/query",
        {
            "subject_id": "user",
            "predicate": "favorite_editor",
            "timestamp": "2025-01-20T00:00:00Z",
            "include_evidence": True,
            "include_lineage": True,
        },
    )
    assert q1["status"] == "SUPPORTED"
    assert q1["value"] == "VS Code"
    print(f"      - Query Jan 20 Output: Value='{q1['value']}' | Status={q1['status']} (PASS)")

    # 4. Timeline Endpoint
    print("[4/8] Retrieving Timeline (GET /api/v1/timeline/user/favorite_editor)...")
    tl = get_fn("/api/v1/timeline/user/favorite_editor")
    assert len(tl.get("timeline", [])) >= 3
    print(f"      - Timeline Entries Count: {len(tl['timeline'])} (PASS)")

    # 5. Lineage Endpoint
    b_id = q1["belief_id"]
    print(f"[5/8] Retrieving Lineage Stack (GET /api/v1/beliefs/{b_id}/lineage)...")
    lin = get_fn(f"/api/v1/beliefs/{b_id}/lineage")
    assert "history" in lin
    print(f"      - Lineage History Nodes: {len(lin['history'])} (PASS)")

    # 6. Evidence Endpoint
    print(f"[6/8] Retrieving Evidence (GET /api/v1/beliefs/{b_id}/evidence)...")
    ev = get_fn(f"/api/v1/beliefs/{b_id}/evidence")
    assert len(ev) >= 1
    print(f"      - Evidence Observations: {len(ev)} (PASS)")

    # 7. UNKNOWN Epistemic Abstention
    print("[7/8] Querying Absent Fact 'favorite_language'...")
    q_unk = post_fn(
        "/api/v1/query",
        {
            "subject_id": "user",
            "predicate": "favorite_language",
            "timestamp": "2025-01-20T00:00:00Z",
        },
    )
    assert q_unk["status"] == "UNKNOWN"
    assert q_unk["value"] is None
    assert q_unk["confidence"] == 0.0
    print(f"      - UNKNOWN Output: Value={q_unk['value']} | Status={q_unk['status']} | Confidence={q_unk['confidence']} (PASS)")

    # 8. CONFLICTED State Handling
    print("[8/8] Querying Contradiction 'location' at Feb 15...")
    q_conf = post_fn(
        "/api/v1/query",
        {
            "subject_id": "user",
            "predicate": "location",
            "timestamp": "2025-02-15T00:00:00Z",
        },
    )
    assert q_conf["status"] == "CONFLICTED"
    assert q_conf["value"] is None
    assert q_conf["confidence"] == 0.5
    print(f"      - CONFLICTED Output: Value={q_conf['value']} | Status={q_conf['status']} | Confidence={q_conf['confidence']} (PASS)")

    print("\n" + "=" * 70)
    print("      CHRONOGRAPH DEPLOYMENT SMOKE TEST PASSED 100%!")
    print("=" * 70)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    run_deployment_smoke_test(target)
