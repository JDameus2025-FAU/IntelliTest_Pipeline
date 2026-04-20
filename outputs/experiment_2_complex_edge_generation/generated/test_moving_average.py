import pytest
from src.sample_functions import moving_average


def test_moving_average_basic():
    values = [1, 2, 3, 4, 5]
    window = 3
    expected = [2.0, 3.0, 4.0]  # (1+2+3)/3, (2+3+4)/3, (3+4+5)/3
    result = moving_average(values, window)
    assert result == expected


def test_moving_average_empty_list():
    values = []
    window = 1
    result = moving_average(values, window)
    assert result == []


def test_moving_average_invalid_window_size():
    values = [1, 2, 3]
    with pytest.raises(ValueError, match="window_size must be positive"):
        moving_average(values, 0)
    with pytest.raises(ValueError, match="window_size cannot exceed the number of values"):
        moving_average(values, 5)


def test_moving_average_window_equals_length():
    values = [4, 6, 8]
    window = 3
    expected = [6.0]  # average of all three values
    result = moving_average(values, window)
    assert result == expected
    # Ensure rounding works with non-integer average
    values = [1, 2]
    window = 2
    expected = [1.5]
    assert moving_average(values, window) == expected
    # Test rounding to two decimals
    values = [1, 2, 3]
    window = 2
    # (1+2)/2 = 1.5, (2+3)/2 = 2.5
    expected = [1.5, 2.5]
    assert moving_average(values, window) == expected
    # Verify rounding: 1.3333 rounds to 1.33
    values = [1, 2, 3]
    window = 3
    expected = [2.0]
    assert moving_average(values, window) == expected
    # Complex rounding case
    values = [1, 2, 2, 4]
    window = 3
    expected = [1.67, 2.67]  # (1+2+2)/3=1.666..., (2+2+4)/3=2.666...
    assert moving_average(values, window) == expected
    # Confirm no rounding errors with floating point precision
    values = [0.1, 0.2, 0.3, 0.4]
    window = 2
    expected = [0.15, 0.25, 0.35]
    assert moving_average(values, window) == expected
