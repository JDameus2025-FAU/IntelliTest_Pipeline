import pytest
from src.sample_functions import add_numbers

# --------------------------------------------------------------------
# Parameterized tests for typical arithmetic combinations
# --------------------------------------------------------------------
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5),           # small positives
        (-1, -4, -5),        # small negatives
        (0, 5, 5),           # one zero
        (5, 0, 5),           # zero second
        (1_000_000, 2_000_000, 3_000_000),  # large positives
        (-1_000_000, -2_000_000, -3_000_000),  # large negatives
        (-10, 10, 0),        # opposite signs cancel
    ],
)
def test_add_numbers_basic(a, b, expected):
    """Basic addition cases: positives, negatives, zeros, large integers."""
    result = add_numbers(a, b)
    assert isinstance(result, int), f"Result should be int, got {type(result)}"
    assert result == expected, f"add_numbers({a}, {b}) returned {result}, expected {expected}"


# --------------------------------------------------------------------
# Tests for type handling – the function should raise TypeError on non‑int
# --------------------------------------------------------------------
@pytest.mark.parametrize(
    "a, b",
    [
        ("1", 2),          # string first
        (3, "4"),          # string second
        (1.5, 2),          # float first
        (3, 2.5),          # float second
        (None, 5),         # None first
        (5, None),         # None second
    ],
)
def test_add_numbers_invalid_types(a, b):
    """add_numbers should raise TypeError when arguments are not integers."""
    with pytest.raises(TypeError):
        add_numbers(a, b)


# --------------------------------------------------------------------
# Idempotence and repeatability
# --------------------------------------------------------------------
def test_add_numbers_idempotent():
    """Calling add_numbers with the same arguments should yield the same result."""
    a, b = 7, -3
    first_call = add_numbers(a, b)
    second_call = add_numbers(a, b)
    assert first_call == second_call == 4


# --------------------------------------------------------------------
# Boundary behaviour: test with very large integers (Python's unlimited int)
# --------------------------------------------------------------------
def test_add_numbers_large_integers():
    """Ensure function can handle extremely large integers."""
    large = 10**1000  # 1 followed by 1000 zeros
    result = add_numbers(large, large)
    assert result == large * 2
    assert isinstance(result, int)


# --------------------------------------------------------------------
# Ensure that the function does not alter input values (pure function)
# --------------------------------------------------------------------
def test_add_numbers_pure():
    """add_numbers should not mutate its arguments."""
    a, b = 4, 5
    a_copy, b_copy = a, b
    _ = add_numbers(a, b)
    assert a == a_copy and b == b_copy, "Function mutated its inputs"


# --------------------------------------------------------------------
# Additional edge case: adding two zeros
# --------------------------------------------------------------------
def test_add_numbers_two_zeros():
    """Adding zero and zero should return zero."""
    assert add_numbers(0, 0) == 0, "add_numbers(0, 0) did not return 0"


# --------------------------------------------------------------------
# Negative test: ensure function does not accept non-integer types silently
# --------------------------------------------------------------------
def test_add_numbers_no_implicit_conversion():
    """The function should not perform implicit conversion from string to int."""
    with pytest.raises(TypeError):
        add_numbers("5", "10")
