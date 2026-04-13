import pytest
from src.sample_functions import moving_average


def test_moving_average_returns_expected_windows_for_standard_input():
    assert moving_average([2, 4, 6, 8], 2) == [3.0, 5.0, 7.0]


def test_moving_average_handles_exact_window_length():
    assert moving_average([1, 2, 3], 3) == [2.0]


def test_moving_average_returns_rounded_values():
    assert moving_average([1, 2, 2], 2) == [1.5, 2.0]


def test_moving_average_returns_empty_list_for_empty_input():
    assert moving_average([], 2) == []


def test_moving_average_rejects_invalid_window_sizes():
    with pytest.raises(ValueError):
        moving_average([1, 2, 3], 0)

    with pytest.raises(ValueError):
        moving_average([1, 2, 3], 4)
