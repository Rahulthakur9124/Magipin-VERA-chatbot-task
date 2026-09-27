import json
from pathlib import Path
import urllib.request
import urllib.error

BASE_URL = "http://localhost:8000"
ROOT = Path(__file__).resolve().parent
TEST_FILE = ROOT / "expanded" / "test_pairs.json"
OUT_FILE = ROOT / "test_results.json"

data = json.loads(TEST_FILE.read_text(encoding="utf-8"))
pairs = data["pairs"]

results = []

for i, case in enumerate(pairs, 1):
    trigger_id = case["trigger_id"]

    body = {
        "now": "2026-04-26T10:00:00Z",
        "available_triggers": [trigger_id],
    }

    req = urllib.request.Request(
        BASE_URL + "/v1/tick",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            output = json.loads(r.read().decode("utf-8"))
        status = "OK"
    except urllib.error.HTTPError as e:
        output = {
            "error": f"HTTP {e.code}",
            "detail": e.read().decode("utf-8", errors="replace"),
        }
        status = "ERROR"
    except Exception as e:
        output = {"error": str(e)}
        status = "ERROR"

    result = {
        "test_id": case["test_id"],
        "trigger_id": trigger_id,
        "status": status,
        "output": output,
    }
    results.append(result)

    actions = output.get("actions", []) if isinstance(output, dict) else []
    if actions:
        body_text = actions[0].get("body", "")
        print(f'{case["test_id"]}: {body_text}')
    else:
        print(f'{case["test_id"]}: NO ACTION')

OUT_FILE.write_text(
    json.dumps(results, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"\nCompleted {len(results)} cases.")
print(f"Saved full results to: {OUT_FILE}")
