import pytest
from src.sample_functions import classify_score


def test_classify_score_buckets():
    assert classify_score(100) == "excellent"
    assert classify_score(90) == "excellent"
    assert classify_score(89) == "good"
    assert classify_score(75) == "good"
    assert classify_score(74) == "pass"
    assert classify_score(60) == "pass"
    assert classify_score(59) == "fail"
    assert classify_score(0) == "fail"


def test_classify_score_invalid_values():
    with pytest.raises(ValueError, match="score must be between 0 and 100"):
        classify_score(-1)
    with pytest.raises(ValueError, match="score must be between 0 and 100"):
        classify_score(101)
        """  """
