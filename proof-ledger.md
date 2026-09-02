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

## Day 6 (Part 1 of 2) — 2026-09-02 — Failure analysis, calibration check, needs_human_review fix
- Artifact: 01-caseflow-agent/caseflow (extract.py instructions)
- Calibration finding: inconclusive — intent had no variance to test against (100% baseline), and
  the confidence distribution was heavily skewed (19/20 cases >=0.85). Separately confirmed the
  model reports 0.98-0.99 confidence on cases where OTHER fields (urgency, needs_human_review,
  account_id) are wrong, including adversarial cases — confidence should not be trusted as a proxy
  for overall extraction correctness.
- Change made: added an explicit "unsupported action" trigger to needs_human_review, with 4 concrete
  examples (update, reset, cancel, send-a-document), based on 4/5 failing cases sharing that exact
  pattern (case_018, phishing, correctly excluded as a different category).
- Result: 4 of 5 originally-diagnosed cases (001, 003, 005, 009) fixed. needs_human_review_accuracy
  held flat at 75% because 3 new false positives (002, 004, 012) and 1 new miss (017) appeared —
  NOT YET DIAGNOSED, carried forward as an open item.
- Also observed: case_015 (intent) and case_009 (urgency) each flipped correct/incorrect across runs
  with no relevant instruction change touching those fields — evidence the model's outputs are
  genuinely non-deterministic at this sample size, not purely a function of prompt changes.
- Separate change (isolated to its own run): added an account_id formatting/normalization
  instruction — account_id_accuracy 90% -> 100%, cleanly isolated by running it as its own iteration.
- Regressions: intent_accuracy 95% -> 90% (net), partially explained by non-determinism (see above),
  not fully attributable to either instruction change yet.
- FDE lesson: a flat top-line percentage can hide a completely different set of underlying failures;
  and at small sample sizes, LLM run-to-run variance can look identical to a prompt-caused regression
  unless you check for it explicitly.
- Evidence: https://github.com/PaulAduGyamfi/fde-portfolio/commit/fb28254fa7e67d130b0edbf85e2b3a90493272c6
- Open for Day 6 Part 2 / later: diagnose 002/004/012 false positives; consider whether temperature
  can be pinned lower to reduce noise before trusting future before/after comparisons.