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