import json
from pathlib import Path
import urllib.request

BASE_URL = "http://localhost:8000"
ROOT = Path(__file__).resolve().parent
TRIGGERS = ROOT / "expanded" / "triggers"

files = sorted(TRIGGERS.glob("*.json"))
accepted = 0

for f in files:
    trigger = json.loads(f.read_text(encoding="utf-8"))
    body = {
        "scope": "trigger",
        "context_id": trigger["id"],
        "version": 1,
        "payload": trigger,
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
        result = json.loads(r.read().decode("utf-8"))
        if r.status == 200 and (result.get("accepted") is True or result.get("reason") == "stale_version"):
            accepted += 1

print(f"trigger: {accepted}/{len(files)} accepted")

req = urllib.request.Request(BASE_URL + "/v1/healthz")
with urllib.request.urlopen(req, timeout=10) as r:
    print(json.dumps(json.loads(r.read().decode("utf-8")), indent=2))
