import pytest
from src.sample_functions import add_numbers

def test_add_positive_numbers():
    assert add_numbers(3, 5) == 8
    assert add_numbers(10, 20) == 30

def test_add_negative_and_positive_numbers():
    assert add_numbers(-4, 7) == 3
    assert add_numbers(5, -10) == -5

def test_add_zero_cases():
    assert add_numbers(0, 0) == 0
    assert add_numbers(0, 5) == 5
    assert add_numbers(5, 0) == 5

def test_add_large_numbers():
    large = 10**12
    assert add_numbers(large, large) == large * 2
    assert add_numbers(-large, large) == 0
