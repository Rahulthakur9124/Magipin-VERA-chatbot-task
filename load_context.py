import json
from pathlib import Path
import urllib.request

BASE_URL = "http://localhost:8000"
ROOT = Path(__file__).resolve().parent
EXPANDED = ROOT / "expanded"

def post_context(scope, context_id, payload, version=1):
    body = {
        "scope": scope,
        "context_id": context_id,
        "version": version,
        "payload": payload,
        "delivered_at": "2026-04-26T10:00:00Z",
    }
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        BASE_URL + "/v1/context",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.status, json.loads(r.read().decode("utf-8"))

def load_dir(scope, folder):
    files = sorted((EXPANDED / folder).glob("*.json"))
    ok = 0
    for f in files:
        payload = json.loads(f.read_text(encoding="utf-8"))
        if scope == "category":
            context_id = payload["slug"]
        elif scope == "merchant":
            context_id = payload["merchant_id"]
        elif scope == "customer":
            context_id = payload["customer_id"]
        else:
            context_id = payload["id"]
        status, result = post_context(scope, context_id, payload)
        if status == 200 and result.get("accepted") is True:
            ok += 1
        elif status == 409:
            ok += 1
        else:
            print("FAILED:", scope, context_id, status, result)
    print(f"{scope}: {ok}/{len(files)} accepted")
    return ok

if __name__ == "__main__":
    total = 0
    total += load_dir("category", "categories")
    total += load_dir("merchant", "merchants")
    total += load_dir("customer", "customers")

    req = urllib.request.Request(BASE_URL + "/v1/healthz")
    with urllib.request.urlopen(req, timeout=10) as r:
        health = json.loads(r.read().decode("utf-8"))

    print("\nHEALTH:")
    print(json.dumps(health, indent=2))
