# Experiment 2: Complex and Edge-Case Test Generation

## Objective

Generate tests for functions with conditionals, validation paths, and edge-case behavior.

## Setup

- Run timestamp: 2026-04-19 02:24:50
- LLM mode: `mock`
- Model label: `openai/gpt-oss-20b`
- Functions evaluated: 3

## Results

- Average total score: 14.67 / 20
- Highest-scoring function: `normalize_username` (15/20)
- Lowest-scoring function: `classify_score` (14/20)

## Observations

- In this small benchmark, the generated tests for this condition were structurally usable but varied in completeness.
- Differences in score should be read as heuristic quality signals rather than definitive measures of semantic correctness.

## Per-Function Summary

- `classify_score` (complex_edge): total 14 / 20
- `normalize_username` (complex_edge): total 15 / 20
- `moving_average` (complex_edge): total 15 / 20
