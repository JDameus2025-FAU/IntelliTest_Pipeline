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
    ],
)
def test_classify_score_buckets(score, expected):
    assert classify_score(score) == expected

def test_classify_score_invalid_value():
    with pytest.raises(ValueError):
        classify_score(-1)
    with pytest.raises(ValueError):
        classify_score(101)
