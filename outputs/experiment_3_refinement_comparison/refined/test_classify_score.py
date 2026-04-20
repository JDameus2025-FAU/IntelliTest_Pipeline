import pytest
from src.sample_functions import classify_score

@pytest.mark.parametrize(
    "score,expected",
    [
        # Excellent boundary
        (100, "excellent"),
        (99, "excellent"),
        (90, "excellent"),
        # Good boundary
        (89, "good"),
        (88, "good"),
        (75, "good"),
        # Pass boundary
        (74, "pass"),
        (70, "pass"),
        (60, "pass"),
        # Fail boundary
        (59, "fail"),
        (50, "fail"),
        (0, "fail"),
        # Float values
        (100.0, "excellent"),
        (90.0, "excellent"),
        (89.9, "good"),
        (75.0, "good"),
        (74.5, "pass"),
        (60.0, "pass"),
        (59.9, "fail"),
        (0.0, "fail"),
    ],
)
def test_classify_score_buckets(score, expected):
    """
    Test that classify_score correctly maps numeric scores to their
    performance buckets, including integer and float inputs at the
    boundaries of each category.
    """
    result = classify_score(score)
    assert isinstance(result, str), "Result should be a string"
    assert result == expected, f"Score {score} should map to {expected}"


@pytest.mark.parametrize(
    "invalid_score",
    [
        -1,
        -10,
        101,
        200,
        -100,
        150.1,
    ],
)
def test_classify_score_invalid_value(invalid_score):
    """
    Test that classify_score raises a ValueError with the correct
    message when the score is outside the 0-100 inclusive range.
    """
    with pytest.raises(ValueError, match=r"score must be between 0 and 100"):
        classify_score(invalid_score)


def test_classify_score_type_error():
    """
    Test that passing a non-numeric type results in a TypeError
    because the comparison operators are not defined for strings.
    """
    with pytest.raises(TypeError):
        classify_score("ninety")

    with pytest.raises(TypeError):
        classify_score([90])

    with pytest.raises(TypeError):
        classify_score(None)


def test_classify_score_exact_midpoints():
    """
    Test that exact midpoints of each category return the correct bucket.
    """
    assert classify_score(90) == "excellent"
    assert classify_score(75) == "good"
    assert classify_score(60) == "pass"
    assert classify_score(0) == "fail"


def test_classify_score_range_of_values():
    """
    Test a random sample of values across the entire valid range to
    ensure consistent behavior.
    """
    for score in range(0, 101, 5):
        if score >= 90:
            expected = "excellent"
        elif score >= 75:
            expected = "good"
        elif score >= 60:
            expected = "pass"
        else:
            expected = "fail"
        assert classify_score(score) == expected, f"Failed at score {score}"
