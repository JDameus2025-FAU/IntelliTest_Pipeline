# IntelliTest Pipeline Findings

- Run timestamp: 2026-04-12 23:34:56
- LLM mode: `groq`
- Model label: `openai/gpt-oss-20b`
- Functions evaluated: 4

## Aggregate Results

- Average initial total score: 17.75 / 20
- Average refined total score: 19.50 / 20
- Functions improved after refinement: 3 / 4
- Functions unchanged after refinement: 1 / 4

## Observations

- Largest improvement: `add_numbers` (+4 points)
- Smallest improvement: `classify_score` (+0 points)
- Refinement tends to help most when the initial tests miss edge cases or exception behavior.
- The heuristic evaluator is transparent and experiment-friendly, but it measures structural quality rather than full semantic correctness.

## Per-Function Summary

- `add_numbers`: initial 15 -> refined 19 (+4)
- `classify_score`: initial 19 -> refined 19 (+0)
- `normalize_username`: initial 18 -> refined 20 (+2)
- `moving_average`: initial 19 -> refined 20 (+1)
