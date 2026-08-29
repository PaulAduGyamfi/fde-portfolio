# Proof Ledger

## Day 1 - Deterministic application boundary
**Date:** 2026-08-28

- Artifact: 00-learning-labs/day1_fastapi
- Proof: Implemented a FastAPI service with Pydantic validation and pytest coverage
- Test result: 3 passing tests
- Lesson: deterministic validation belongs in code, not in a prompt. LLM's decide and interpret, deterministic code validates and enforces.
- Evidence Link: 
    - FastAPI: https://github.com/PaulAduGyamfi/fde-portfolio/commit/95205b565d8a56a3c2769e496adb62c8c37a2b96
    - Pytest coverage: https://github.com/PaulAduGyamfi/fde-portfolio/commit/8a2ebdff2083d85c99cb4d075b04a3775b5ea62c

Claim: Built a typed Python API that accepts a support ticket and rejects bad input (boundary) for AI workflow

## Day 2 - Structured extraction + first eval
**Date:** 2026-08-29

- Artifact: 00-learning-labs/day2_structured_extraction
- Dataset: 20 golden cases
- Baseline: intent 100%, customer_id 95%, urgency 85%, needs_human_review 85%, missing_info 65% 
- Change made: instructed the model to use field names from schema, and not create its own
- Iteration 1: intent 100%, customer_id 89.5%, urgency 89.5%, needs_human_review 94.7%, missing_info 89.5% ; regressions: customer_id
- Evidence: 
- Lesson: The moment model behavior becomes part of a workflow, you need examples, expected behavior, measurable errors, and a regression path. Structured outputs gaurantees shape, not correctness.
- Evidence Link: https://github.com/PaulAduGyamfi/fde-portfolio/commit/1f1019568b71436ee3f1a339f553e21469031ac0


Claim: Ingested messy support tickets into strongly-typed Pydantic structures using LLM; 20 hand-written golden cases to test the model against; wrote an eval script that prints per-field accuracy and failures; performed one measured iteration.