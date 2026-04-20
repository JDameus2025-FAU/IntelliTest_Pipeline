import pytest
from src.sample_functions import add_numbers


def test_add_numbers_with_positive_values():
    assert add_numbers(2, 3) == 5


def test_add_numbers_with_negative_values():
    assert add_numbers(-4, -6) == -10


def test_add_numbers_with_zero():
    assert add_numbers(0, 9) == 9


def test_add_numbers_with_mixed_sign_values():
    assert add_numbers(-7, 10) == 3
