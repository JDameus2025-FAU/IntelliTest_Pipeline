import pytest
from src.sample_functions import add_numbers

def test_add_positive_numbers():
    assert add_numbers(2, 3) == 5
    assert add_numbers(10, 15) == 25

def test_add_negative_numbers():
    assert add_numbers(-1, -1) == -2
    assert add_numbers(-5, 3) == -2

def test_add_with_zero():
    assert add_numbers(0, 0) == 0
    assert add_numbers(0, 7) == 7
    assert add_numbers(7, 0) == 7

def test_add_large_numbers():
    large = 10**12
    assert add_numbers(large, large) == 2 * large
    assert add_numbers(-large, large) == 0
    assert add_numbers(-large, -large) == -2 * large
