import pytest
from src.sample_functions import moving_average


def test_moving_average_basic():
    values = [1, 2, 3, 4]
    window_size = 2
    expected = [1.5, 2.5, 3.5]  # (1+2)/2, (2+3)/2, (3+4)/2
    assert moving_average(values, window_size) == expected


def test_moving_average_rounding():
    values = [1.1, 2.2, 3.3]
    window_size = 2
    # (1.1+2.2)/2 = 1.65, (2.2+3.3)/2 = 2.75
    expected = [1.65, 2.75]
    assert moving_average(values, window_size) == expected


def test_moving_average_empty_input():
    assert moving_average([], 3) == []


def test_moving_average_invalid_window():
    with pytest.raises(ValueError, match="window_size must be positive"):
        moving_average([1, 2, 3], 0)

    with pytest.raises(ValueError, match="window_size cannot exceed the number of values"):
        moving_average([1, 2, 3], 5)
