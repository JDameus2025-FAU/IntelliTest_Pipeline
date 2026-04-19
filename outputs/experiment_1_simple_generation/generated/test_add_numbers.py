import pytest
from src.sample_functions import add_numbers


def test_add_numbers_with_positive_values():
    assert add_numbers(2, 3) == 5


def test_add_numbers_with_negative_value():
    assert add_numbers(-1, 4) == 3
