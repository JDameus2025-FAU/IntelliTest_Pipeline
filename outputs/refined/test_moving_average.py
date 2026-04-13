import pytest
from src.sample_functions import moving_average

@pytest.mark.parametrize(
    "values, window_size, expected",
    [
        ([1, 2, 3, 4, 5], 3, [2.0, 3.0, 4.0]),
        ([1.1, 2.2, 3.3, 4.4], 2, [1.65, 2.75, 3.85]),
        ([0.005], 1, [0.01]),  # rounding of single value
        ([-5, -4, -3, -2, -1], 2, [-4.5, -3.5, -2.5, -1.5]),
        ([1000000, 2000000], 2, [1500000.0]),
        ([1, 2, 3], 1, [1.0, 2.0, 3.0]),  # window size 1
    ],
)
def test_moving_average_basic(values, window_size, expected):
    """Test normal functionality across a range of input sizes and types."""
    result = moving_average(values, window_size)
    assert isinstance(result, list)
    assert all(isinstance(v, float) for v in result)
    assert result == expected


def test_moving_average_rounding_edge():
    """Verify rounding behaves correctly for values that should round up."""
    # 0.005 should round to 0.01 with round(,2)
    assert moving_average([0.005], 1) == [0.01]
    # 1.2345 should round to 1.23 (round half to even)
    assert moving_average([1.2345], 1) == [1.23]


def test_moving_average_window_equals_length():
    """When the window size equals the number of values, a single average should be returned."""
    values = [10, 20, 30]
    assert moving_average(values, 3) == [20.0]


def test_moving_average_empty_input():
    """Empty input list should return an empty list without raising."""
    assert moving_average([], 1) == []


def test_moving_average_invalid_window_size():
    """Negative, zero, or too large window sizes must raise ValueError with clear message."""
    with pytest.raises(ValueError, match="window_size must be positive"):
        moving_average([1, 2, 3], 0)

    with pytest.raises(ValueError, match="window_size must be positive"):
        moving_average([1, 2, 3], -5)

    with pytest.raises(ValueError, match="window_size cannot exceed the number of values"):
        moving_average([1, 2, 3], 4)


def test_input_immutability():
    """The function should not modify the original list."""
    original = [1, 2, 3, 4, 5]
    copy = original.copy()
    moving_average(original, 3)
    assert original == copy, "Input list should remain unchanged"


def test_moving_average_mixed_integer_float():
    """Input containing both integers and floats should be handled correctly."""
    values = [1, 2.5, 3, 4.5, 5]
    result = moving_average(values, 2)
    assert result == [1.75, 2.75, 3.75, 4.75]


def test_moving_average_large_numbers():
    """Test handling of large numeric values to ensure no overflow occurs."""
    values = [1e12, 2e12, 3e12]
    result = moving_average(values, 2)
    assert result == [1.5e12, 2.5e12]


def test_moving_average_result_type():
    """Ensure the function returns a list of floats, not strings or integers."""
    values = [1, 2, 3]
    result = moving_average(values, 2)
    assert isinstance(result, list)
    assert all(isinstance(v, float) for v in result)


def test_moving_average_consistency_with_manual_calculation():
    """Cross‑check against a manual sliding window calculation."""
    values = [5, 1, 4, 2, 3]
    window_size = 3
    manual = [round(sum(values[i:i + window_size]) / window_size, 2)
              for i in range(len(values) - window_size + 1)]
    assert moving_average(values, window_size) == manual

# End of test file
