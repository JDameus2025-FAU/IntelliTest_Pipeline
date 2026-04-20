import pytest
from src.sample_functions import moving_average

def test_basic_moving_average():
    values = [1, 2, 3, 4, 5]
    result = moving_average(values, 3)
    assert result == [2.0, 3.0, 4.0]

def test_window_equals_length():
    values = [1, 2, 3]
    result = moving_average(values, 3)
    assert result == [2.0]

def test_invalid_window_size_zero():
    with pytest.raises(ValueError, match="window_size must be positive"):
        moving_average([1, 2, 3], 0)

def test_window_size_exceeds_values():
    with pytest.raises(ValueError, match="window_size cannot exceed the number of values"):
        moving_average([1, 2], 3)

def test_empty_values_returns_empty():
    assert moving_average([], 3) == []
