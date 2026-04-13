import pytest
from src.sample_functions import moving_average

def test_moving_average_basic():
    values = [1, 2, 3, 4, 5]
    window_size = 3
    expected = [2.0, 3.0, 4.0]
    assert moving_average(values, window_size) == expected

def test_moving_average_with_decimals_and_rounding():
    values = [1.1, 2.2, 3.3, 4.4]
    window_size = 2
    expected = [1.65, 2.75, 3.85]
    assert moving_average(values, window_size) == expected

def test_moving_average_empty_values():
    assert moving_average([], 3) == []

def test_moving_average_invalid_window():
    with pytest.raises(ValueError):
        moving_average([1, 2, 3], 0)

    with pytest.raises(ValueError):
        moving_average([1, 2, 3], 4)
