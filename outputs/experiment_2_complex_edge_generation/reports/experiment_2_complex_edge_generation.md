# Experiment 2: Complex and Edge-Case Test Generation

## Objective

Generate tests for functions with conditionals, validation paths, and edge-case behavior.

## Setup

- Run timestamp: 2026-04-19 20:33:28
- LLM mode: `groq`
- Model label: `openai/gpt-oss-20b`
- Functions evaluated: 3

## Results

- Average total score: 17.67 / 20
- Highest-scoring function: `classify_score` (18/20)
- Lowest-scoring function: `normalize_username` (17/20)

## Observations

- In this small benchmark, the generated tests for this condition were structurally usable but varied in completeness.
- Differences in score should be read as heuristic quality signals rather than definitive measures of semantic correctness.

## Per-Function Summary

- `classify_score` (complex_edge): total 18 / 20
- `normalize_username` (complex_edge): total 17 / 20
- `moving_average` (complex_edge): total 18 / 20
