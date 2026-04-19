import pytest
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
