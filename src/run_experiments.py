from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from evaluate_tests import EvaluationResult, evaluate_test_code
from generate_tests import TestArtifact, generate_initial_tests
from llm_client import LLMClient
from refine_tests import refine_generated_tests
from sample_functions import SampleFunction, load_sample_functions


@dataclass(frozen=True)
class ExperimentConfig:
    identifier: str
    title: str
    description: str
    target_condition: str | None
    include_refinement: bool


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
    output_root.mkdir(parents=True, exist_ok=True)

    llm_client = LLMClient(use_mock=args.use_mock_llm, model=args.model)
    sample_functions = load_sample_functions()
    experiment_configs = build_experiment_configs()
    experiment_results: list[dict[str, object]] = []

    for experiment_config in experiment_configs:
        selected_functions = select_functions_for_experiment(
            sample_functions=sample_functions,
            experiment_config=experiment_config,
        )
        experiment_dir = output_root / experiment_config.identifier
        generated_dir = experiment_dir / "generated"
        refined_dir = experiment_dir / "refined"
        reports_dir = experiment_dir / "reports"

        for directory in (generated_dir, reports_dir):
            directory.mkdir(parents=True, exist_ok=True)
        if experiment_config.include_refinement:
            refined_dir.mkdir(parents=True, exist_ok=True)

        if experiment_config.include_refinement:
            comparison_rows = run_refinement_experiment(
                sample_functions=selected_functions,
                generated_dir=generated_dir,
                refined_dir=refined_dir,
                llm_client=llm_client,
                experiment_identifier=experiment_config.identifier,
            )
            csv_path = reports_dir / f"{experiment_config.identifier}.csv"
            write_csv_report(csv_path, comparison_rows)

            markdown_summary = build_refinement_summary(
                experiment_config=experiment_config,
                comparison_rows=comparison_rows,
                llm_mode=llm_client.mode_label,
                model_name=llm_client.model,
            )
        else:
            generation_rows = run_generation_experiment(
                sample_functions=selected_functions,
                generated_dir=generated_dir,
                llm_client=llm_client,
                experiment_identifier=experiment_config.identifier,
            )
            csv_path = reports_dir / f"{experiment_config.identifier}.csv"
            write_csv_report(csv_path, generation_rows)

            markdown_summary = build_generation_summary(
                experiment_config=experiment_config,
                generation_rows=generation_rows,
                llm_mode=llm_client.mode_label,
                model_name=llm_client.model,
            )

        summary_path = reports_dir / f"{experiment_config.identifier}.md"
        summary_path.write_text(markdown_summary, encoding="utf-8")
        experiment_results.append(
            {
                "config": experiment_config,
                "csv_path": csv_path,
                "summary_path": summary_path,
                "rows": comparison_rows if experiment_config.include_refinement else generation_rows,
            }
        )

        print(f"[{experiment_config.identifier}] generated tests: {generated_dir}")
        if experiment_config.include_refinement:
            print(f"[{experiment_config.identifier}] refined tests: {refined_dir}")
        print(f"[{experiment_config.identifier}] csv report: {csv_path}")
        print(f"[{experiment_config.identifier}] markdown summary: {summary_path}")

    write_final_report_summary(
        output_root=output_root,
        experiment_results=experiment_results,
        llm_mode=llm_client.mode_label,
        model_name=llm_client.model,
    )


def build_experiment_configs() -> list[ExperimentConfig]:
    return [
        ExperimentConfig(
            identifier="experiment_1_simple_generation",
            title="Experiment 1: Simple Function Test Generation",
            description="Generate tests for simple functions and evaluate the quality of the first-pass output.",
            target_condition="simple",
            include_refinement=False,
        ),
        ExperimentConfig(
            identifier="experiment_2_complex_edge_generation",
            title="Experiment 2: Complex and Edge-Case Test Generation",
            description="Generate tests for functions with conditionals, validation paths, and edge-case behavior.",
            target_condition="complex_edge",
            include_refinement=False,
        ),
        ExperimentConfig(
            identifier="experiment_3_refinement_comparison",
            title="Experiment 3: Initial Output vs Iterative Refinement",
            description="Compare first-pass generated tests against refined tests across the full benchmark set.",
            target_condition=None,
            include_refinement=True,
        ),
    ]


def select_functions_for_experiment(
    sample_functions: list[SampleFunction],
    experiment_config: ExperimentConfig,
) -> list[SampleFunction]:
    if experiment_config.target_condition is None:
        return sample_functions

    return [
        sample_function
        for sample_function in sample_functions
        if sample_function.condition == experiment_config.target_condition
    ]


def run_generation_experiment(
    sample_functions: list[SampleFunction],
    generated_dir: Path,
    llm_client: LLMClient,
    experiment_identifier: str,
) -> list[dict[str, object]]:
    generation_rows: list[dict[str, object]] = []

    for sample_function in sample_functions:
        initial_artifact = generate_initial_tests(sample_function, llm_client)
        initial_path = generated_dir / f"test_{sample_function.name}.py"
        initial_path.write_text(initial_artifact.code, encoding="utf-8")
        initial_eval = evaluate_test_code(sample_function.name, initial_artifact.code)

        generation_rows.append(
            {
                "experiment_id": experiment_identifier,
                "function_name": sample_function.name,
                "function_condition": sample_function.condition,
                "provider": initial_artifact.provider,
                "generated_path": str(initial_path),
                "correctness": initial_eval.correctness,
                "assertion_strength": initial_eval.assertion_strength,
                "edge_case_coverage": initial_eval.edge_case_coverage,
                "readability": initial_eval.readability,
                "total": initial_eval.total,
                "notes": f"{initial_artifact.notes} {initial_eval.notes}",
            }
        )

    return generation_rows


def run_refinement_experiment(
    sample_functions: list[SampleFunction],
    generated_dir: Path,
    refined_dir: Path,
    llm_client: LLMClient,
    experiment_identifier: str,
) -> list[dict[str, object]]:
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
                experiment_identifier=experiment_identifier,
                sample_function=sample_function,
                initial_artifact=initial_artifact,
                initial_eval=initial_eval,
                refined_artifact=refined_artifact,
                refined_eval=refined_eval,
                initial_path=initial_path,
                refined_path=refined_path,
            )
        )

    return comparison_rows


def _build_comparison_row(
    experiment_identifier: str,
    sample_function: SampleFunction,
    initial_artifact: TestArtifact,
    initial_eval: EvaluationResult,
    refined_artifact: TestArtifact,
    refined_eval: EvaluationResult,
    initial_path: Path,
    refined_path: Path,
) -> dict[str, object]:
    return {
        "experiment_id": experiment_identifier,
        "function_name": sample_function.name,
        "function_condition": sample_function.condition,
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


def build_generation_summary(
    experiment_config: ExperimentConfig,
    generation_rows: list[dict[str, object]],
    llm_mode: str,
    model_name: str,
) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    function_count = len(generation_rows)
    average_total = _average_for_key(generation_rows, "total")
    strongest_row = max(generation_rows, key=lambda row: row["total"])
    weakest_row = min(generation_rows, key=lambda row: row["total"])

    lines = [
        f"# {experiment_config.title}",
        "",
        "## Objective",
        "",
        experiment_config.description,
        "",
        "## Setup",
        "",
        f"- Run timestamp: {timestamp}",
        f"- LLM mode: `{llm_mode}`",
        f"- Model label: `{model_name}`",
        f"- Functions evaluated: {function_count}",
        "",
        "## Results",
        "",
        f"- Average total score: {average_total:.2f} / 20",
        f"- Highest-scoring function: `{strongest_row['function_name']}` ({strongest_row['total']}/20)",
        f"- Lowest-scoring function: `{weakest_row['function_name']}` ({weakest_row['total']}/20)",
        "",
        "## Observations",
        "",
        "- In this small benchmark, the generated tests for this condition were structurally usable but varied in completeness.",
        "- Differences in score should be read as heuristic quality signals rather than definitive measures of semantic correctness.",
        "",
        "## Per-Function Summary",
        "",
    ]

    for row in generation_rows:
        lines.append(
            f"- `{row['function_name']}` ({row['function_condition']}): "
            f"total {row['total']} / 20"
        )

    lines.append("")
    return "\n".join(lines)


def build_refinement_summary(
    experiment_config: ExperimentConfig,
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
        f"# {experiment_config.title}",
        "",
        "## Objective",
        "",
        experiment_config.description,
        "",
        "## Setup",
        "",
        f"- Run timestamp: {timestamp}",
        f"- LLM mode: `{llm_mode}`",
        f"- Model label: `{model_name}`",
        f"- Functions evaluated: {function_count}",
        "",
        "## Results",
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
        "- In this run, the refinement pass generally increased heuristic scores, especially when the first-pass tests missed edge cases or exception behavior.",
        "- These results should be interpreted cautiously because the evaluator measures structural quality and surface coverage patterns rather than full semantic correctness.",
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


def write_final_report_summary(
    output_root: Path,
    experiment_results: list[dict[str, object]],
    llm_mode: str,
    model_name: str,
) -> None:
    summary_path = output_root / "final_report_summary.md"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    simple_result = _get_experiment_result(
        experiment_results, "experiment_1_simple_generation"
    )
    complex_result = _get_experiment_result(
        experiment_results, "experiment_2_complex_edge_generation"
    )
    refinement_result = _get_experiment_result(
        experiment_results, "experiment_3_refinement_comparison"
    )
    simple_rows = simple_result["rows"]
    complex_rows = complex_result["rows"]
    refinement_rows = refinement_result["rows"]

    simple_average = _average_for_key(simple_rows, "total")
    complex_average = _average_for_key(complex_rows, "total")
    initial_average = _average_for_key(refinement_rows, "initial_total")
    refined_average = _average_for_key(refinement_rows, "refined_total")
    improved_count = sum(1 for row in refinement_rows if row["total_improvement"] > 0)
    unchanged_count = sum(1 for row in refinement_rows if row["total_improvement"] == 0)

    lines = [
        "# IntelliTest Pipeline Final Summary",
        "",
        "## Study Goal",
        "",
        "This prototype explores whether iterative LLM-based refinement improves automatically generated Python unit tests under three experimental conditions: simple function generation, complex and edge-case generation, and initial-versus-refined comparison.",
        "",
        "## Experimental Setup",
        "",
        f"- Run timestamp: {timestamp}",
        f"- LLM mode: `{llm_mode}`",
        f"- Model label: `{model_name}`",
        "- Evaluation method: transparent heuristic scoring rubric covering correctness, assertion strength, edge-case coverage, and readability.",
        "- Scope: small benchmark of sample Python functions intended for local experimentation rather than production-grade test evaluation.",
        "",
        "## Condition Summaries",
        "",
        f"- Experiment 1 (simple generation): average total score {simple_average:.2f} / 20 across {len(simple_rows)} function(s).",
        f"- Experiment 2 (complex and edge-case generation): average total score {complex_average:.2f} / 20 across {len(complex_rows)} function(s).",
        f"- Experiment 3 (initial vs refinement): average initial score {initial_average:.2f} / 20 and average refined score {refined_average:.2f} / 20 across {len(refinement_rows)} function(s).",
        "",
        "## Concise Observations",
        "",
        "- In this small benchmark, simple functions were generally easier to cover with acceptable first-pass tests than functions with validation logic or edge-case-heavy behavior.",
        "- The complex and edge-case condition showed more variation in heuristic quality, which is consistent with the broader behavioral surface of those functions.",
        f"- In the refinement comparison, {improved_count} of {len(refinement_rows)} functions improved and {unchanged_count} remained unchanged under the heuristic rubric.",
        "- The refinement stage appears promising as a way to increase structural completeness, but the current evidence should be treated as preliminary.",
        "",
        "## Limitations",
        "",
        "- The evaluation rubric is heuristic and does not fully measure semantic correctness or true fault-detection ability.",
        "- The benchmark is small, so the results are better suited to a class project or pilot study than to broad generalization.",
        "- Output quality may vary across providers, models, prompts, and repeated runs.",
        "",
        "## Reuse Note",
        "",
        "This summary is written to be reusable as a short findings section in a research-style class report. The experiment-specific Markdown files can be cited for condition-level detail, while the CSV files provide the underlying tabular results.",
        "",
        "## Report Files",
        "",
    ]

    for experiment_result in experiment_results:
        config = experiment_result["config"]
        lines.append(
            f"- `{config.title}`: summary `{Path(str(experiment_result['summary_path'])).name}`, csv `{Path(str(experiment_result['csv_path'])).name}`"
        )

    lines.append("")
    summary_path.write_text("\n".join(lines), encoding="utf-8")


def _get_experiment_result(
    experiment_results: list[dict[str, object]], identifier: str
) -> dict[str, object]:
    for experiment_result in experiment_results:
        config = experiment_result["config"]
        if isinstance(config, ExperimentConfig) and config.identifier == identifier:
            return experiment_result
    raise ValueError(f"Experiment result not found for identifier: {identifier}")


def _average_for_key(rows: list[dict[str, object]], key: str) -> float:
    if not rows:
        return 0.0
    return sum(float(row[key]) for row in rows) / len(rows)


if __name__ == "__main__":
    main()
