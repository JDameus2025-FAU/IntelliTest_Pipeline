# IntelliTest Pipeline Findings

- Run timestamp: 2026-04-12 23:00:28
- LLM mode: `mock`
- Model label: `gpt-5.2`
- Functions evaluated: 4

## Aggregate Results

- Average initial total score: 14.75 / 20
- Average refined total score: 17.50 / 20
- Functions improved after refinement: 4 / 4
- Functions unchanged after refinement: 0 / 4

## Observations

- Largest improvement: `classify_score` (+4 points)
- Smallest improvement: `add_numbers` (+1 points)
- Refinement tends to help most when the initial tests miss edge cases or exception behavior.
- The heuristic evaluator is transparent and experiment-friendly, but it measures structural quality rather than full semantic correctness.

## Per-Function Summary

- `add_numbers`: initial 15 -> refined 16 (+1)
- `classify_score`: initial 14 -> refined 18 (+4)
- `normalize_username`: initial 15 -> refined 18 (+3)
- `moving_average`: initial 15 -> refined 18 (+3)
