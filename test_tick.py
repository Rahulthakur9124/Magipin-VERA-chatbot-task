import json
from pathlib import Path
import urllib.request

BASE_URL = "http://localhost:8000"
ROOT = Path(__file__).resolve().parent

pairs = json.loads((ROOT / "expanded" / "test_pairs.json").read_text(encoding="utf-8"))["pairs"]
case = pairs[0]

body = {
    "now": "2026-04-26T10:00:00Z",
    "available_triggers": [case["trigger_id"]],
}

data = json.dumps(body).encode("utf-8")
req = urllib.request.Request(
    BASE_URL + "/v1/tick",
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST",
)

with urllib.request.urlopen(req, timeout=10) as r:
    result = json.loads(r.read().decode("utf-8"))

print("TEST CASE:", case["test_id"])
print("TRIGGER:", case["trigger_id"])
print("\nVERA OUTPUT:")
print(json.dumps(result, indent=2, ensure_ascii=False))
