# Vera AI Challenge Bot — v0.2

A grounded, deterministic implementation of the magicpin Vera challenge contract.

## Design
- Versioned in-memory context store for category/merchant/customer/trigger pushes.
- Trigger-aware routing rather than one generic prompt.
- Customer-facing flows use customer name, consent, language preference, relationship state and real trigger details.
- Merchant-facing flows prioritize one concrete next step and cite supplied source data where relevant.
- No unsupported prices, dates, competitor facts, research statistics or medical claims are invented.
- `/v1/reply` detects opt-out, repeated auto-replies, affirmative intent and requests to wait.

## Run
```bash
pip install -r requirements.txt
uvicorn bot:app --host 0.0.0.0 --port 8080
```

## Generate canonical submission
```bash
python generate_submission.py
```

## Required endpoints
- `GET /v1/healthz`
- `GET /v1/metadata`
- `POST /v1/context`
- `POST /v1/tick`
- `POST /v1/reply`

## Optional LLM copy editor
Set `OPENAI_API_KEY` (or `LLM_API_KEY`) to enable a guarded OpenAI-compatible copy-edit pass. Optional settings:
- `LLM_MODEL` (default `gpt-4o-mini`)
- `OPENAI_BASE_URL` (default `https://api.openai.com/v1`)
- `LLM_TIMEOUT` (default `8` seconds)

The LLM receives only whitelisted context/facts and its output is rejected if it introduces new numeric facts or drops important grounded proper nouns. If the LLM is unavailable, the deterministic composer remains fully functional.

## Validation
The supplied dataset generates 30 canonical submission rows. The API was also smoke-tested locally for health, metadata, intent transition, auto-reply backoff/termination, and opt-out handling.

The official `judge_simulator.py` uses an external LLM scorer and therefore needs a judge API key to produce the official /50 score.
