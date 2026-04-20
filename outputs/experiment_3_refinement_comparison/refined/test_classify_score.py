import pytest
from src.sample_functions import classify_score

# --------------------------------------------------------------------------- #
# Helper constants
# --------------------------------------------------------------------------- #

VALID_CLASSIFICATIONS = {"excellent", "good", "pass", "fail"}

# --------------------------------------------------------------------------- #
# 1️⃣  Classification tests
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "score,expected",
    [
        (100, "excellent"),
        (90, "excellent"),
        (89, "good"),
        (80, "good"),
        (75, "good"),
        (74, "pass"),
        (60, "pass"),
        (59, "fail"),
        (0, "fail"),
        (30, "fail"),
    ],
)
def test_classification_buckets(score, expected):
    """All valid integer scores should return the correct bucket."""
    result = classify_score(score)
    assert isinstance(result, str), f"Expected string, got {type(result).__name__}"
    assert result == expected, f"Score {score} classified as {result}, expected {expected}"
    assert result in VALID_CLASSIFICATIONS


@pytest.mark.parametrize(
    "score,expected",
    [
        (90.0, "excellent"),
        (89.9, "good"),
        (75.5, "good"),
        (74.9, "pass"),
        (60.0, "pass"),
        (59.99, "fail"),
    ],
)
def test_float_scores(score, expected):
    """
    The function accepts floats but still classifies them into the same buckets.
    """
    result = classify_score(score)
    assert result == expected, f"Float score {score} classified as {result}, expected {expected}"
    assert result in VALID_CLASSIFICATIONS


# --------------------------------------------------------------------------- #
# 2️⃣  Boundary value tests
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "score,expected",
    [
        (0, "fail"),
        (59, "fail"),
        (60, "pass"),
        (74, "pass"),
        (75, "good"),
        (89, "good"),
        (90, "excellent"),
        (100, "excellent"),
    ],
)
def test_boundary_scores(score, expected):
    """Tests the exact boundaries for each bucket."""
    assert classify_score(score) == expected


# --------------------------------------------------------------------------- #
# 3️⃣  Exception tests
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("invalid_score", [-1, 101, 200, -100])
def test_invalid_scores_raise_value_error(invalid_score):
    """Scores outside [0, 100] must raise ValueError."""
    with pytest.raises(ValueError, match=r"score must be between 0 and 100"):
        classify_score(invalid_score)


@pytest.mark.parametrize(
    "bad_input",
    [
        "eighty",
        99.9,  # float is accepted, so not a test
        None,
        [],
        {"score": 90},
        object(),
    ],
)
def test_invalid_input_type_raises_type_error(bad_input):
    """
    Inputs that cannot be compared to an int will raise a TypeError.
    Note that floats are accepted due to Python's comparison semantics.
    """
    if isinstance(bad_input, float):
        pytest.skip("Floats are accepted by the function; skipping TypeError test.")
    with pytest.raises(TypeError):
        classify_score(bad_input)


# --------------------------------------------------------------------------- #
# 4️⃣  Coverage of all valid cases
# --------------------------------------------------------------------------- #

def test_all_valid_scores_have_known_classification():
    """Iterate over the entire valid range and ensure classification is in the set."""
    for score in range(0, 101):
        result = classify_score(score)
        assert result in VALID_CLASSIFICATIONS, f"Unexpected classification {result} for score {score}"
        # Explicit checks for boundaries
        if score == 0:
            assert result == "fail"
        elif 1 <= score <= 59:
            assert result == "fail"
        elif 60 <= score <= 74:
            assert result == "pass"
        elif 75 <= score <= 89:
            assert result == "good"
        elif 90 <= score <= 100:
            assert result == "excellent"
