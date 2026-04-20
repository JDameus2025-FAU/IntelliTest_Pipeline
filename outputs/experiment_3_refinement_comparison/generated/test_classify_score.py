import pytest
from src.sample_functions import classify_score

def test_excellent_classification():
    assert classify_score(100) == "excellent"
    assert classify_score(90) == "excellent"

def test_good_classification():
    assert classify_score(75) == "good"
    assert classify_score(80) == "good"

def test_pass_classification():
    assert classify_score(60) == "pass"
    assert classify_score(59) == "fail"  # just below pass threshold

def test_fail_classification():
    assert classify_score(0) == "fail"
    assert classify_score(30) == "fail"
