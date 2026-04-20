import pytest
from src.sample_functions import classify_score

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
def test_classify_score_valid_cases(score, expected):
    assert classify_score(score) == expected

@pytest.mark.parametrize("score", [-1, 101])
def test_classify_score_invalid_scores(score):
    with pytest.raises(ValueError, match="score must be between 0 and 100"):
        classify_score(score)
