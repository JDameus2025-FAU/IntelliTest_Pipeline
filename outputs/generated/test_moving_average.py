import pytest
from src.sample_functions import moving_average


def test_moving_average_returns_expected_windows():
    assert moving_average([2, 4, 6, 8], 2) == [3.0, 5.0, 7.0]


def test_moving_average_returns_empty_list_for_empty_input():
    assert moving_average([], 2) == []
