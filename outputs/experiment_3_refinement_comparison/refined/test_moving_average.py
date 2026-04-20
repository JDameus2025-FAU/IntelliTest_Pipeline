import pytest
from src.sample_functions import moving_average


def test_moving_average_basic():
    values = [1, 2, 3, 4]
    window_size = 2
    expected = [1.5, 2.5, 3.5]
    assert moving_average(values, window_size) == expected


@pytest.mark.parametrize(
    ("values", "window_size", "expected"),
    [
        ([1.1, 2.2, 3.3], 2, [1.65, 2.75]),  # standard float example
        ([1.005, 1.005], 2, [1.0]),  # test bankers rounding to 2 decimals
        ([1.005, 1.015], 2, [1.01]),  # average 1.01
        ([1, 2, 3, 4, 5], 1, [1.0, 2.0, 3.0, 4.0, 5.0]),  # window size 1
        ([5, 4, 3, 2, 1], 5, [3.0]),  # window size equals list length
    ],
)
def test_moving_average_various(values, window_size, expected):
    result = moving_average(values, window_size)
    assert isinstance(result, list)
    assert all(isinstance(v, float) for v in result)
    assert result == expected
    # Ensure the returned list is a new object
    assert result is not values
    # Mutating the result should not affect the input list
    result.append(999.99)
    assert len(values) == len(values)  # original list size unchanged


def test_moving_average_empty_input():
    assert moving_average([], 3) == []


def test_moving_average_invalid_window():
    with pytest.raises(ValueError, match="window_size must be positive"):
        moving_average([1, 2, 3], 0)
    with pytest.raises(ValueError, match="window_size cannot exceed the number of values"):
        moving_average([1, 2, 3], 5)


def test_moving_average_large_values_and_window():
    values = list(range(1, 10001))  # 1..10_000
    window_size = 5000
    # The moving average of a consecutive block of 5000 increasing integers
    # has a known exact value: average of first and last in window
    first_expected = round((values[0] + values[window_size - 1]) / 2, 2)
    last_expected = round((values[-window_size] + values[-1]) / 2, 2)
    result = moving_average(values, window_size)
    assert len(result) == len(values) - window_size + 1
    assert result[0] == first_expected
    assert result[-1] == last_expected
    # Check a middle value
    mid_index = len(result) // 2
    mid_start = mid_index
    mid_end = mid_start + window_size - 1
    mid_expected = round((values[mid_start] + values[mid_end]) / 2, 2)
    assert result[mid_index] == mid_expected


def test_moving_average_with_negative_and_zero_values():
    values = [-2, 0, 2, 4]
    window_size = 3
    # (-2 + 0 + 2)/3 = 0.0, (0 + 2 + 4)/3 = 2.0
    expected = [0.0, 2.0]
    assert moving_average(values, window_size) == expected
    # Ensure rounding works for negative sums
    values = [-1.5, -1.5]
    window_size = 2
    assert moving_average(values, window_size) == [-1.5]


def test_moving_average_type_error_on_non_numeric():
    values = ["a", 1, 2]
    with pytest.raises(TypeError):
        moving_average(values, 2)
    values = [None, 2]
    with pytest.raises(TypeError):
        moving_average(values, 2)
