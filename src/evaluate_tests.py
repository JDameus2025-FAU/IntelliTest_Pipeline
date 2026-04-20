from __future__ import annotations

from dataclasses import dataclass
import ast
import re

@dataclass(frozen=True)
class EvaluationResult:
    correctness: int
    assertion_strength: int
    edge_case_coverage: int
    readability: int
    notes: str

    @property
    def total(self) -> int:
        return (
            self.correctness
            + self.assertion_strength
            + self.edge_case_coverage
            + self.readability
        )

EDGE_PATTERNS = {
    "none": r"\bNone\b",
    "empty_string": r'""|\'\'',
    "zero": r"[\(\[, ]0[\)\], ]",
    "negative": r"-1|-5|-10",
    "empty_list": r"\[\]",
    "exception": r"pytest\.raises",
    "boundary": r"\b100\b|\b90\b|\b75\b|\b60\b",
    "whitespace": r'"  |  "',
}

def evaluate_test_code(function_name: str, test_code: str) -> EvaluationResult:
    notes: list[str] = []

    try:
        tree = ast.parse(test_code)
        notes.append("Python syntax parsed successfully.")
    except SyntaxError as exc:
        return EvaluationResult(
            correctness=1,
            assertion_strength=1,
            edge_case_coverage=1,
            readability=1,
            notes=f"Syntax error detected: {exc}",
        )

    test_names = re.findall(r"^def (test_[A-Za-z0-9_]+)\(", test_code, flags=re.MULTILINE)
    assert_count = len(re.findall(r"\bassert\b", test_code))
    raises_count = len(re.findall(r"pytest\.raises", test_code))
    import_ok = (
        f"from src.sample_functions import {function_name}" in test_code
        or f"from sample_functions import {function_name}" in test_code
    )
    function_referenced = function_name in test_code
    edge_hits = [label for label, pattern in EDGE_PATTERNS.items() if re.search(pattern, test_code)]

    correctness = _score_correctness(
        tree=tree,
        import_ok=import_ok,
        function_referenced=function_referenced,
        test_names=test_names,
        assert_count=assert_count,
        raises_count=raises_count,
    )
    assertion_strength = _score_assertion_strength(
        test_code=test_code,
        assert_count=assert_count,
        raises_count=raises_count,
    )
    edge_case_coverage = _score_edge_case_coverage(edge_hits=edge_hits, raises_count=raises_count)
    readability = _score_readability(test_code=test_code, test_names=test_names)

    if import_ok:
        notes.append("Imports the target function.")
    else:
        notes.append("Missing an explicit import for the target function.")

    if test_names:
        notes.append(f"Found {len(test_names)} test case(s).")
    else:
        notes.append("No pytest-style test functions were detected.")

    if assert_count or raises_count:
        notes.append(
            f"Detected {assert_count} assert statement(s) and {raises_count} exception assertion(s)."
        )
    else:
        notes.append("No assertions or exception checks were detected.")

    if edge_hits:
        notes.append(f"Edge-oriented patterns detected: {', '.join(edge_hits)}.")
    else:
        notes.append("No obvious edge-oriented inputs were detected.")

    return EvaluationResult(
        correctness=correctness,
        assertion_strength=assertion_strength,
        edge_case_coverage=edge_case_coverage,
        readability=readability,
        notes=" ".join(notes),
    )


def _score_correctness(
    tree: ast.AST,
    import_ok: bool,
    function_referenced: bool,
    test_names: list[str],
    assert_count: int,
    raises_count: int,
) -> int:
    score = 2

    if import_ok and function_referenced:
        score += 1
    if test_names:
        score += 1
    if assert_count > 0 or raises_count > 0:
        score += 1
    if not any(isinstance(node, ast.FunctionDef) for node in ast.walk(tree)):
        score -= 1

    return max(1, min(5, score))

def _score_assertion_strength(test_code: str, assert_count: int, raises_count: int) -> int:
    if assert_count == 0 and raises_count == 0:
        return 1
    if assert_count == 1 and raises_count == 0:
        return 2

    rich_assertions = sum(
        1
        for marker in ["==", "!=", " in ", "len(", "pytest.raises"]
        if marker in test_code
    )

    score = 2
    if assert_count >= 2:
        score += 1
    if raises_count >= 1:
        score += 1
    if rich_assertions >= 3:
        score += 1

    return max(1, min(5, score))

def _score_edge_case_coverage(edge_hits: list[str], raises_count: int) -> int:
    score = 1

    if edge_hits:
        score += 1
    if len(edge_hits) >= 2:
        score += 1
    if len(edge_hits) >= 4:
        score += 1
    if raises_count >= 1:
        score += 1

    return max(1, min(5, score))

def _score_readability(test_code: str, test_names: list[str]) -> int:
    lines = [line for line in test_code.splitlines() if line.strip()]
    long_lines = [line for line in lines if len(line) > 100]
    descriptive_names = [name for name in test_names if len(name.split("_")) >= 4]

    score = 2
    if len(test_names) >= 2:
        score += 1
    if len(descriptive_names) >= max(1, len(test_names) // 2):
        score += 1
    if not long_lines:
        score += 1

    return max(1, min(5, score))
