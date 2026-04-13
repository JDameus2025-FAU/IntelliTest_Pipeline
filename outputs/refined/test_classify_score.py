import pytest
from src.sample_functions import classify_score


@pytest.mark.parametrize(
    "score,expected",
    [
        (100, "excellent"),
        (90, "excellent"),
        (89, "good"),
        (75, "good"),
        (74, "pass"),
        (60, "pass"),
        (59, "fail"),
        (0, "fail"),
        (99, "excellent"),
        (76, "good"),
        (61, "pass"),
        (1, "fail"),
    ],
)
def test_classify_score_buckets(score: int, expected: str) -> None:
    """Verify that classify_score returns the correct bucket for a wide range of scores."""
    assert classify_score(score) == expected, f"{score} should be classified as {expected}"


@pytest.mark.parametrize(
    "score",
    [-1, 101, -100, 200],
)
def test_classify_score_out_of_range_raises(score: int) -> None:
    """Ensure ValueError is raised for scores outside the 0–100 inclusive range."""
    with pytest.raises(ValueError) as exc_info:
        classify_score(score)
    assert str(exc_info.value) == "score must be between 0 and 100"


def test_classify_score_error_message() -> None:
    """Test the exact error message for out-of-range inputs."""
    with pytest.raises(ValueError) as exc_info:
        classify_score(-5)
    assert str(exc_info.value) == "score must be between 0 and 100"


@pytest.mark.parametrize(
    "invalid_input",
    ["85", None, [90], {"score": 90}],
)
def test_classify_score_invalid_type_raises(invalid_input) -> None:
    """Passing a non-numeric type should raise TypeError during comparison."""
    with pytest.raises(TypeError):
        classify_score(invalid_input)


def test_classify_score_accepts_float_and_returns_correct_bucket() -> None:
    """Floating point numbers are accepted and correctly classified."""
    # float values fall within the numeric comparison logic
    assert classify_score(85.0) == "good"
    assert classify_score(75.5) == "good"
    assert classify_score(60.1) == "pass"
    assert classify_score(59.9) == "fail"
    assert classify_score(0.0) == "fail"
    assert classify_score(100.0) == "excellent"


def test_classify_score_is_pure_function() -> None:
    """Confirm that repeated calls with the same input yield the same result."""
    assert classify_score(77) == classify_score(77) == "good"
    assert classify_score(58) == classify_score(58) == "fail"
    assert classify_score(93) == classify_score(93) == "excellent"
    assert classify_score(63) == classify_score(63) == "pass"
