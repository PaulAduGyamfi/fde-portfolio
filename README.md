# FDE Build

Support tickets arrive as messy free text and need triage; the goal is a measured reduction in
first-response handling time. Current extraction accuracy: intent 95% /
urgency 85% on 20 cases.

## What ServiceOps v0 does
Accepts a support ticket, validates it deterministically, uses a model to interpret free-text tickets
into a typed extraction (intent, urgency, customer ID, missing information), and lets an investigator
agent look up account and case data through two read-only tools. No write actions exist yet.

## Why Day 1 contains no AI
Validation, required fields, and request shape are rules that must be predictable and testable — a model
is probabilistic and can't guarantee that. Day 1 built the FastAPI + Pydantic boundary with zero model
calls, so the application has a deterministic foundation before any inference is introduced.

## Where model inference is used
(1) extracting structured fields (intent, urgency, customer ID) from a raw
ticket's free text, where interpretation of language is genuinely required; (2) the investigator agent,
which decides whether it needs to call `get_account` or `list_open_cases` to answer a question, and
synthesizes their results into an answer.

## Structured-output contract
`TicketExtraction` (Pydantic model): `intent`, `customer_id` (nullable), `urgency`, `needs_human_review`,
`missing_information`, `short_summary`. The model's output is validated against this schema — shape is
guaranteed; correctness is measured separately by the eval, not assumed from the schema passing.

## Golden dataset and current eval results
20 hand-written cases. Fields graded: intent, customer_id, urgency, needs_human_review, plus a separate
subset-based check on missing_information. Baseline vs. current numbers: 

Baseline:
cases=20
intent_accuracy=95.0%
customer_id_accuracy=90.0%
urgency_accuracy=90.0%
needs_human_review_accuracy=95.0%
missing_information_pass=65.0%

Current:
cases=20
intent_accuracy=95.0%
customer_id_accuracy=100.0%
urgency_accuracy=85.0%
needs_human_review_accuracy=90.0%
missing_information_pass=95.0%

## Tools and permission boundary
Two tools, both read-only: `get_account(customer_id)`, `list_open_cases(customer_id)`. No tool exists
to create, modify, or send anything — the agent is structurally incapable of taking a write action,
regardless of what any message asks it to do.



## How to run tests
```bash
cd 00-learning-labs/day1_fastapi && pytest -q
```

## How to run the eval
```bash
cd 00-learning-labs/day2_structured_extraction && python eval_extractor.py
```