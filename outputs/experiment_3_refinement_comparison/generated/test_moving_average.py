import pytest

from src.sample_functions import moving_average

def test_moving_average_basic():
    values = [1, 2, 3, 4, 5]
    result = moving_average(values, 3)
    assert result == [2.0, 3.0, 4.0]

def test_moving_average_rounding():
    values = [1, 2, 3, 4]
    result = moving_average(values, 2)
    assert result == [1.5, 2.5, 3.5]

def test_moving_average_invalid_window():
    values = [1, 2, 3]
    with pytest.raises(ValueError, match="window_size must be positive"):
        moving_average(values, 0)

def test_moving_average_window_exceeds_length():
    values = [1, 2]
    with pytest.raises(ValueError, match="window_size cannot exceed"):
        moving_average(values, 3)

def test_moving_average_empty_values():
    values = []
    result = moving_average(values, 2)
    assert result == []
