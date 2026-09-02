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
- Baseline: intent 95%, customer_id 90%, urgency 90%, needs_human_review 90%, missing_info 65% 
- Change made: instructed the model to use field names from schema, and not create its own
- Iteration 1: intent 95%, customer_id 100%, urgency 85%, needs_human_review 95%, missing_info 95% ; regressions: urgency
- Evidence: 
- Lesson: The moment model behavior becomes part of a workflow, you need examples, expected behavior, measurable errors, and a regression path. Structured outputs gaurantees shape, not correctness.
- Evidence Link: https://github.com/PaulAduGyamfi/fde-portfolio/commit/4e17d65fa63243bf16312e3538062f5bea2c6e01


Claim: Ingested messy support tickets into strongly-typed Pydantic structures using LLM; 20 hand-written golden cases to test the model against; wrote an eval script that prints per-field accuracy and failures; performed one measured iteration.

## Day 3 - Tools/ function calling, Agents, Traces and observability,
**Date:** 2026-08-30

- Artifact: 00-learning-labs/day3_tool_agent
- Test: 11-scenario trace review
- Lesson: the model can never do anything you did not write a tool for and tool descriptions are how the model decides when to call. You judge the agent by its trace (what it actually called), not by how nice its final answer sounds.
- Evidence Link: https://github.com/PaulAduGyamfi/fde-portfolio/commit/418196666711720970df917cbde4f03a6ac5a29d

Claim: Implemented a tool-using agent with two read-only tools. Bound its capabilities in code and judged it by its trace.

## Day 4 - CaseFlow Package Structure/ Extraction contract
**Date:** 2026-08-31

- Artifact: 01-caseflow-agent/
- Dataset: 20 golden cases
- Lesson: I design the contract before the prompt. Structured outputs gaurantees shape.
- Evidence Link: https://github.com/PaulAduGyamfi/fde-portfolio/commit/37cd22ffed85883f63a8146f0825e7f39309a652

Claim: EmailIn/Extraction contract (schemas.py) written and committed before extract.py's instructions existed. 20 golden-case emails (evals/cases.jsonl) written with full expected blocks before extractor instructions were written or the model was called.

## Day 5 - CaseFlow /extract endpoint and its eval + baseline v1
**Date:** 2026-09-01

- Artifact: 01-caseflow-agent/ (caseflow/extract.py, caseflow/api.py, caseflow/llm.py, evals/run_extraction_eval.py)
- Dataset: 20 golden cases (5 normal / 11 edge / 4 adversarial)
- Baseline v1: intent 95%, urgency 75%, account_id 90%, needs_human_review 75% — 12 of 20 cases failed at least one field
- Failure clusters: account_id not normalized to ACC- form ("77385", "AC8831"); billing_question vs refund_status boundary; urgency low vs normal boundary; needs_human_review under-triggers on frustrated/blocked customers
- Change made: none yet — this day is the honest unturned baseline
- Lesson: Self-reported confidence is not a quality signal. Ten of the twelve failing cases came back at 0.98-0.99 confidence, so confidence cannot be used as a routing or auto-approve gate; only the eval can. A golden set is fallible too. An eval failure is a claim that model and label disagree — you triage which one is wrong before you touch the prompt.
- Evidence Link: https://github.com/PaulAduGyamfi/fde-portfolio/commit/9ce3d6753aea62fad7d3619a2d9e3ce3f0dbf3a5