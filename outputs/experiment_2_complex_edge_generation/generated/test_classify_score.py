import pytest
from src.sample_functions import classify_score


def test_classify_score_returns_excellent_for_high_scores():
    assert classify_score(95) == "excellent"


def test_classify_score_returns_pass_for_midrange_score():
    assert classify_score(65) == "pass"
