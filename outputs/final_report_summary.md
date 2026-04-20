# IntelliTest Pipeline Final Summary

## Study Goal

This prototype explores whether iterative LLM-based refinement improves automatically generated Python unit tests under three experimental conditions: simple function generation, complex and edge-case generation, and initial-versus-refined comparison.

## Experimental Setup

- Run timestamp: 2026-04-19 20:33:38
- LLM mode: `groq`
- Model label: `openai/gpt-oss-20b`
- Evaluation method: transparent heuristic scoring rubric covering correctness, assertion strength, edge-case coverage, and readability.
- Scope: small benchmark of sample Python functions intended for local experimentation rather than production-grade test evaluation.

## Condition Summaries

- Experiment 1 (simple generation): average total score 16.00 / 20 across 1 function(s).
- Experiment 2 (complex and edge-case generation): average total score 17.67 / 20 across 3 function(s).
- Experiment 3 (initial vs refinement): average initial score 16.75 / 20 and average refined score 18.25 / 20 across 4 function(s).

## Concise Observations

- In this small benchmark, simple functions were generally easier to cover with acceptable first-pass tests than functions with validation logic or edge-case-heavy behavior.
- The complex and edge-case condition showed more variation in heuristic quality, which is consistent with the broader behavioral surface of those functions.
- In the refinement comparison, 2 of 4 functions improved and 2 remained unchanged under the heuristic rubric.
- The refinement stage appears promising as a way to increase structural completeness, but the current evidence should be treated as preliminary.

## Limitations

- The evaluation rubric is heuristic and does not fully measure semantic correctness or true fault-detection ability.
- The benchmark is small, so the results are better suited to a class project or pilot study than to broad generalization.
- Output quality may vary across providers, models, prompts, and repeated runs.

## Reuse Note

This summary is written to be reusable as a short findings section in a research-style class report. The experiment-specific Markdown files can be cited for condition-level detail, while the CSV files provide the underlying tabular results.

## Report Files

- `Experiment 1: Simple Function Test Generation`: summary `experiment_1_simple_generation.md`, csv `experiment_1_simple_generation.csv`
- `Experiment 2: Complex and Edge-Case Test Generation`: summary `experiment_2_complex_edge_generation.md`, csv `experiment_2_complex_edge_generation.csv`
- `Experiment 3: Initial Output vs Iterative Refinement`: summary `experiment_3_refinement_comparison.md`, csv `experiment_3_refinement_comparison.csv`
