# Experiment 3: Initial Output vs Iterative Refinement

## Objective

Compare first-pass generated tests against refined tests across the full benchmark set.

## Setup

- Run timestamp: 2026-04-19 20:26:39
- LLM mode: `groq`
- Model label: `openai/gpt-oss-20b`
- Functions evaluated: 4

## Results

- Average initial total score: 17.75 / 20
- Average refined total score: 20.00 / 20
- Functions improved after refinement: 4 / 4
- Functions unchanged after refinement: 0 / 4

## Observations

- Largest improvement: `add_numbers` (+4 points)
- Smallest improvement: `moving_average` (+1 points)
- In this run, the refinement pass generally increased heuristic scores, especially when the first-pass tests missed edge cases or exception behavior.
- These results should be interpreted cautiously because the evaluator measures structural quality and surface coverage patterns rather than full semantic correctness.

## Per-Function Summary

- `add_numbers`: initial 16 -> refined 20 (+4)
- `classify_score`: initial 18 -> refined 20 (+2)
- `normalize_username`: initial 18 -> refined 20 (+2)
- `moving_average`: initial 19 -> refined 20 (+1)
