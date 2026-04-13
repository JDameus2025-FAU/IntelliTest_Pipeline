import pytest
from src.sample_functions import add_numbers

def test_add_positive():
    assert add_numbers(2, 3) == 5

def test_add_negative():
    assert add_numbers(-1, -4) == -5

def test_add_zero():
    assert add_numbers(0, 5) == 5

def test_add_large_numbers():
    assert add_numbers(1_000_000, 2_000_000) == 3_000_000
