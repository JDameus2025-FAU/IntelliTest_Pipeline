from __future__ import annotations

from dataclasses import dataclass
import ast
import re

from llm_client import LLMClient, LLMClientError
from prompts import GENERATION_SYSTEM_PROMPT, build_generation_prompt
from sample_functions import SampleFunction


@dataclass(frozen=True)
class TestArtifact:
    function_name: str
    code: str
    provider: str
    notes: str


def generate_initial_tests(sample_function: SampleFunction, llm_client: LLMClient) -> TestArtifact:
    """Generate the initial pytest file for a sample function."""
    if llm_client.use_mock:
        return TestArtifact(
            function_name=sample_function.name,
            code=_mock_generated_tests(sample_function.name),
            provider="mock",
            notes="Initial tests generated in mock mode.",
        )

    prompt = build_generation_prompt(
        function_name=sample_function.name,
        function_source=sample_function.source_code,
        description=sample_function.description,
    )

    try:
        response_text = llm_client.complete(
            instructions=GENERATION_SYSTEM_PROMPT,
            prompt=prompt,
        )
        cleaned_code = _sanitize_test_code(response_text, sample_function.name)
        if not _looks_like_test_file(cleaned_code):
            raise LLMClientError("Generated content did not look like a pytest file.")
        return TestArtifact(
            function_name=sample_function.name,
            code=cleaned_code,
            provider=f"openai:{llm_client.model}",
            notes="Initial tests generated with the live API.",
        )
    except LLMClientError as exc:
        return TestArtifact(
            function_name=sample_function.name,
            code=_mock_generated_tests(sample_function.name),
            provider="mock-fallback",
            notes=f"Initial generation fell back to mock output: {exc}",
        )


def _sanitize_test_code(raw_text: str, function_name: str) -> str:
    code = raw_text.strip()

    if code.startswith("```"):
        code = re.sub(r"^```[a-zA-Z0-9_+-]*\n", "", code)
        code = re.sub(r"\n```$", "", code)

    if "from src.sample_functions import" not in code and "from sample_functions import" not in code:
        code = f"import pytest\nfrom src.sample_functions import {function_name}\n\n{code}"

    return code.strip() + "\n"


def _looks_like_test_file(code: str) -> bool:
    if "def test_" not in code:
        return False

    try:
        ast.parse(code)
    except SyntaxError:
        return False

    return True


def _mock_generated_tests(function_name: str) -> str:
    fixtures = {
        "add_numbers": """import pytest
from src.sample_functions import add_numbers


def test_add_numbers_with_positive_values():
    assert add_numbers(2, 3) == 5


def test_add_numbers_with_negative_value():
    assert add_numbers(-1, 4) == 3
""",
        "classify_score": """import pytest
from src.sample_functions import classify_score


def test_classify_score_returns_excellent_for_high_scores():
    assert classify_score(95) == "excellent"


def test_classify_score_returns_pass_for_midrange_score():
    assert classify_score(65) == "pass"
""",
        "normalize_username": """import pytest
from src.sample_functions import normalize_username


def test_normalize_username_lowercases_and_strips_spaces():
    assert normalize_username("  Alice Smith  ") == "alice_smith"


def test_normalize_username_handles_hyphens():
    assert normalize_username("Team-Lead") == "team_lead"
""",
        "moving_average": """import pytest
from src.sample_functions import moving_average


def test_moving_average_returns_expected_windows():
    assert moving_average([2, 4, 6, 8], 2) == [3.0, 5.0, 7.0]


def test_moving_average_returns_empty_list_for_empty_input():
    assert moving_average([], 2) == []
""",
    }
    return fixtures[function_name]
