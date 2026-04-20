import pytest
from src.sample_functions import add_numbers

def test_add_positive_numbers():
    assert add_numbers(3, 7) == 10

def test_add_negative_numbers():
    assert add_numbers(-4, -6) == -10

def test_add_zero():
    assert add_numbers(0, 5) == 5
    assert add_numbers(5, 0) == 5
    assert add_numbers(0, 0) == 0

def test_add_mixed_signs():
    assert add_numbers(-3, 10) == 7
    assert add_numbers(15, -5) == 10
