from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path

from evaluate_tests import EvaluationResult, evaluate_test_code
from generate_tests import TestArtifact, generate_initial_tests
from llm_client import LLMClient
from refine_tests import refine_generated_tests
from sample_functions import load_sample_functions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the IntelliTest Pipeline experiment.")
    parser.add_argument(
        "--use-mock-llm",
        action="store_true",
        help="Use deterministic mock outputs instead of a live API call.",
    )
    parser.add_argument(
        "--output-root",
        default="outputs",
        help="Directory where generated tests and reports should be written.",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Override the model name used by the live client.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_root = Path(args.output_root)
    generated_dir = output_root / "generated"
    refined_dir = output_root / "refined"
    reports_dir = output_root / "reports"

    for directory in (generated_dir, refined_dir, reports_dir):
        directory.mkdir(parents=True, exist_ok=True)

    llm_client = LLMClient(use_mock=args.use_mock_llm, model=args.model)
    sample_functions = load_sample_functions()

    comparison_rows: list[dict[str, object]] = []

    for sample_function in sample_functions:
        initial_artifact = generate_initial_tests(sample_function, llm_client)
        initial_path = generated_dir / f"test_{sample_function.name}.py"
        initial_path.write_text(initial_artifact.code, encoding="utf-8")
        initial_eval = evaluate_test_code(sample_function.name, initial_artifact.code)

        refined_artifact = refine_generated_tests(
            sample_function=sample_function,
            initial_tests=initial_artifact,
            evaluation_notes=initial_eval.notes,
            llm_client=llm_client,
        )
        refined_path = refined_dir / f"test_{sample_function.name}.py"
        refined_path.write_text(refined_artifact.code, encoding="utf-8")
        refined_eval = evaluate_test_code(sample_function.name, refined_artifact.code)

        comparison_rows.append(
            _build_comparison_row(
                function_name=sample_function.name,
                initial_artifact=initial_artifact,
                initial_eval=initial_eval,
                refined_artifact=refined_artifact,
                refined_eval=refined_eval,
                initial_path=initial_path,
                refined_path=refined_path,
            )
        )

    csv_path = reports_dir / "evaluation_summary.csv"
    write_csv_report(csv_path, comparison_rows)

    markdown_summary = build_markdown_summary(
        comparison_rows=comparison_rows,
        llm_mode=llm_client.mode_label,
        model_name=llm_client.model,
    )
    summary_path = reports_dir / "findings.md"
    summary_path.write_text(markdown_summary, encoding="utf-8")

    print(f"Generated initial tests in: {generated_dir}")
    print(f"Generated refined tests in: {refined_dir}")
    print(f"Wrote CSV report to: {csv_path}")
    print(f"Wrote Markdown summary to: {summary_path}")


def _build_comparison_row(
    function_name: str,
    initial_artifact: TestArtifact,
    initial_eval: EvaluationResult,
    refined_artifact: TestArtifact,
    refined_eval: EvaluationResult,
    initial_path: Path,
    refined_path: Path,
) -> dict[str, object]:
    return {
        "function_name": function_name,
        "initial_provider": initial_artifact.provider,
        "refined_provider": refined_artifact.provider,
        "initial_path": str(initial_path),
        "refined_path": str(refined_path),
        "initial_correctness": initial_eval.correctness,
        "refined_correctness": refined_eval.correctness,
        "initial_assertion_strength": initial_eval.assertion_strength,
        "refined_assertion_strength": refined_eval.assertion_strength,
        "initial_edge_case_coverage": initial_eval.edge_case_coverage,
        "refined_edge_case_coverage": refined_eval.edge_case_coverage,
        "initial_readability": initial_eval.readability,
        "refined_readability": refined_eval.readability,
        "initial_total": initial_eval.total,
        "refined_total": refined_eval.total,
        "total_improvement": refined_eval.total - initial_eval.total,
        "initial_notes": f"{initial_artifact.notes} {initial_eval.notes}",
        "refined_notes": f"{refined_artifact.notes} {refined_eval.notes}",
    }


def write_csv_report(csv_path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_markdown_summary(
    comparison_rows: list[dict[str, object]],
    llm_mode: str,
    model_name: str,
) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    function_count = len(comparison_rows)
    initial_average = _average_for_key(comparison_rows, "initial_total")
    refined_average = _average_for_key(comparison_rows, "refined_total")
    improved_count = sum(1 for row in comparison_rows if row["total_improvement"] > 0)
    unchanged_count = sum(1 for row in comparison_rows if row["total_improvement"] == 0)

    strongest_gain_row = max(comparison_rows, key=lambda row: row["total_improvement"])
    weakest_gain_row = min(comparison_rows, key=lambda row: row["total_improvement"])

    lines = [
        "# IntelliTest Pipeline Findings",
        "",
        f"- Run timestamp: {timestamp}",
        f"- LLM mode: `{llm_mode}`",
        f"- Model label: `{model_name}`",
        f"- Functions evaluated: {function_count}",
        "",
        "## Aggregate Results",
        "",
        f"- Average initial total score: {initial_average:.2f} / 20",
        f"- Average refined total score: {refined_average:.2f} / 20",
        f"- Functions improved after refinement: {improved_count} / {function_count}",
        f"- Functions unchanged after refinement: {unchanged_count} / {function_count}",
        "",
        "## Observations",
        "",
        f"- Largest improvement: `{strongest_gain_row['function_name']}` "
        f"({strongest_gain_row['total_improvement']:+d} points)",
        f"- Smallest improvement: `{weakest_gain_row['function_name']}` "
        f"({weakest_gain_row['total_improvement']:+d} points)",
        "- Refinement tends to help most when the initial tests miss edge cases or exception behavior.",
        "- The heuristic evaluator is transparent and experiment-friendly, but it measures structural quality rather than full semantic correctness.",
        "",
        "## Per-Function Summary",
        "",
    ]

    for row in comparison_rows:
        lines.append(
            f"- `{row['function_name']}`: initial {row['initial_total']} -> "
            f"refined {row['refined_total']} ({row['total_improvement']:+d})"
        )

    lines.append("")
    return "\n".join(lines)


def _average_for_key(rows: list[dict[str, object]], key: str) -> float:
    if not rows:
        return 0.0
    return sum(float(row[key]) for row in rows) / len(rows)


if __name__ == "__main__":
    main()
