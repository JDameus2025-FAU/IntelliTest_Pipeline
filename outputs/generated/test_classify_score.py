import pytest
from src.sample_functions import classify_score


def test_classification_buckets():
    # Excellent range
    assert classify_score(100) == "excellent"
    assert classify_score(90) == "excellent"

    # Good range
    assert classify_score(89) == "good"
    assert classify_score(75) == "good"

    # Pass range
    assert classify_score(74) == "pass"
    assert classify_score(60) == "pass"

    # Fail range
    assert classify_score(59) == "fail"
    assert classify_score(0) == "fail"


def test_boundary_values():
    # Exactly at boundaries
    assert classify_score(90) == "excellent"
    assert classify_score(89) == "good"
    assert classify_score(75) == "good"
    assert classify_score(74) == "pass"
    assert classify_score(60) == "pass"
    assert classify_score(59) == "fail"
    assert classify_score(0) == "fail"


def test_out_of_range_raises_value_error():
    with pytest.raises(ValueError):
        classify_score(-1)
    with pytest.raises(ValueError):
        classify_score(101)
