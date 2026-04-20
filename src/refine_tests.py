from __future__ import annotations

from llm_client import LLMClient, LLMClientError
from prompts import REFINEMENT_SYSTEM_PROMPT, build_refinement_prompt
from generate_tests import TestArtifact, _looks_like_test_file, _sanitize_test_code
from sample_functions import SampleFunction

def refine_generated_tests(
    sample_function: SampleFunction,
    initial_tests: TestArtifact,
    evaluation_notes: str,
    llm_client: LLMClient,
) -> TestArtifact:
    """Run the second-pass refinement step for a single sample function."""
    if llm_client.use_mock:
        return TestArtifact(
            function_name=sample_function.name,
            code=_mock_refined_tests(sample_function.name),
            provider="mock",
            notes="Refined tests generated in mock mode.",
        )

    prompt = build_refinement_prompt(
        function_name=sample_function.name,
        function_source=sample_function.source_code,
        existing_test_code=initial_tests.code,
        evaluation_notes=evaluation_notes,
    )

    try:
        response_text = llm_client.complete(
            instructions=REFINEMENT_SYSTEM_PROMPT,
            prompt=prompt,
        )
        cleaned_code = _sanitize_test_code(response_text, sample_function.name)
        if not _looks_like_test_file(cleaned_code):
            raise LLMClientError("Refined content did not look like a pytest file.")
        return TestArtifact(
            function_name=sample_function.name,
            code=cleaned_code,
            provider=f"openai:{llm_client.model}",
            notes="Refined tests generated with the live API.",
        )
    except LLMClientError as exc:
        return TestArtifact(
            function_name=sample_function.name,
            code=_mock_refined_tests(sample_function.name),
            provider="mock-fallback",
            notes=f"Refinement fell back to mock output: {exc}",
        )

def _mock_refined_tests(function_name: str) -> str:
    fixtures = {
        "add_numbers": """import pytest
from src.sample_functions import add_numbers

def test_add_numbers_with_positive_values():
    assert add_numbers(2, 3) == 5

def test_add_numbers_with_negative_values():
    assert add_numbers(-4, -6) == -10

def test_add_numbers_with_zero():
    assert add_numbers(0, 9) == 9

def test_add_numbers_with_mixed_sign_values():
    assert add_numbers(-7, 10) == 3
""",
        "classify_score": """import pytest
from src.sample_functions import classify_score

def test_classify_score_returns_excellent_for_boundary_and_high_scores():
    assert classify_score(90) == "excellent"
    assert classify_score(100) == "excellent"

def test_classify_score_returns_good_for_midrange_scores():
    assert classify_score(75) == "good"
    assert classify_score(89) == "good"

def test_classify_score_returns_pass_and_fail_for_lower_ranges():
    assert classify_score(60) == "pass"
    assert classify_score(59) == "fail"

def test_classify_score_rejects_values_outside_valid_range():
    with pytest.raises(ValueError):
        classify_score(-1)

    with pytest.raises(ValueError):
        classify_score(101)
""",
        "normalize_username": """import pytest
from src.sample_functions import normalize_username

def test_normalize_username_normalizes_spacing_case_and_hyphens():
    assert normalize_username("  Alice Smith  ") == "alice_smith"
    assert normalize_username("Team-Lead") == "team_lead"

def test_normalize_username_collapses_repeated_separators():
    assert normalize_username("Data__Team---Lead") == "data_team_lead"

def test_normalize_username_removes_non_alphanumeric_symbols():
    assert normalize_username("User!@# Name") == "user_name"

def test_normalize_username_rejects_empty_and_invalid_values():
    with pytest.raises(ValueError):
        normalize_username("   ")

    with pytest.raises(ValueError):
        normalize_username("!!!")

    with pytest.raises(ValueError):
        normalize_username(None)
""",
        "moving_average": """import pytest
from src.sample_functions import moving_average

def test_moving_average_returns_expected_windows_for_standard_input():
    assert moving_average([2, 4, 6, 8], 2) == [3.0, 5.0, 7.0]

def test_moving_average_handles_exact_window_length():
    assert moving_average([1, 2, 3], 3) == [2.0]

def test_moving_average_returns_rounded_values():
    assert moving_average([1, 2, 2], 2) == [1.5, 2.0]

def test_moving_average_returns_empty_list_for_empty_input():
    assert moving_average([], 2) == []

def test_moving_average_rejects_invalid_window_sizes():
    with pytest.raises(ValueError):
        moving_average([1, 2, 3], 0)

    with pytest.raises(ValueError):
        moving_average([1, 2, 3], 4)
""",
    }
    return fixtures[function_name]
