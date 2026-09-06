# CaseFlow — AI-assisted support triage with a deterministic spine

## What CaseFlow does
Accepts support tickets (email or GitHub issues), validates deterministically, uses a model to
interpret free-text into a typed extraction (intent, urgency, account ID, missing information), and
lets an investigator agent look up account/case data and draft replies through three tools. No message
is ever sent automatically — every draft requires human review.

## Why Day 1 contains no AI
Validation, required fields, and request shape are rules that must be predictable and testable — a
model is probabilistic and can't guarantee that. The FastAPI + Pydantic boundary has zero model calls;
inference is introduced only where interpretation of language is genuinely required.

## Where model inference is used
Two agents: (1) the extractor, reading a raw ticket into structured fields; (2) the investigator,
deciding whether to call get_account / list_open_cases before drafting a reply.

## Structured-output contract
`Extraction` (Pydantic): intent, urgency, account_id (nullable), requested_action, needs_human_review,
missing_information, confidence. Shape is guaranteed by the schema; correctness is measured separately.

## Golden dataset and current eval results
20 hand-written cases (5/4/4/4/3 intent split, 7 edge, 3 adversarial). Current numbers:
[intent 80% / urgency 75% / account_id 100% / needs_human_review 75%]

## Tools and permission boundary
Three tools: get_account (read), list_open_cases (read), create_draft_reply (creates a draft only —
never sends). The investigator is instructed to call read tools before drafting and never claim a
send/refund/account-change occurred.

## External integration
/import/github fetches real GitHub issues via fetch_json, with classified retries (transient failures
like 503/timeout retry with backoff; permanent failures like 404 raise immediately, no wasted attempts).

## Auth and observability
/extract, /handle, and /import/github require an Api-Key header (require_api_key); /health is
intentionally left open for uptime checks. Every request gets a run_id via middleware.

## How to run tests
cd 01-caseflow-agent && pytest -q

## How to run the eval
cd 01-caseflow-agent/evals && python run_extraction_eval.py
