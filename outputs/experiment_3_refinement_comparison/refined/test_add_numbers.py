import pytest
from src.sample_functions import add_numbers

# --------------------------------------------------------------------------- #
# Basic arithmetic correctness
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 5),
        (10, 15, 25),
        (-1, -1, -2),
        (-5, 3, -2),
        (0, 0, 0),
        (0, 7, 7),
        (7, 0, 7),
    ],
)
def test_add_basic(a: int, b: int, expected: int):
    """Test that add_numbers returns the arithmetic sum for simple cases."""
    result = add_numbers(a, b)
    assert isinstance(result, int), f"Result type is {type(result)}, expected int."
    assert result == expected


# --------------------------------------------------------------------------- #
# Order independence (commutativity)
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "a,b",
    [
        (1, 2),
        (-3, 5),
        (0, 0),
        (123456, -123456),
    ],
)
def test_add_commutative(a: int, b: int):
    """add_numbers(a, b) should equal add_numbers(b, a)."""
    assert add_numbers(a, b) == add_numbers(b, a)


# --------------------------------------------------------------------------- #
# Large number handling
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "a,b,expected",
    [
        (10**12, 10**12, 2 * 10**12),
        (-10**12, 10**12, 0),
        (-10**12, -10**12, -2 * 10**12),
        (10**1000, 10**1000, 2 * 10**1000),
    ],
)
def test_add_large_numbers(a: int, b: int, expected: int):
    """Check that very large integers are summed correctly."""
    assert add_numbers(a, b) == expected


# --------------------------------------------------------------------------- #
# Boolean inputs
# --------------------------------------------------------------------------- #

def test_add_bool_inputs():
    """bool is a subclass of int, so it should be handled naturally."""
    assert add_numbers(True, False) == 1
    assert add_numbers(True, True) == 2
    assert add_numbers(False, False) == 0
    assert isinstance(add_numbers(True, False), int)


# --------------------------------------------------------------------------- #
# Type error handling
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "a,b",
    [
        ("1", 1),
        (1, "2"),
        ("a", "b"),
        (None, 5),
        (5, None),
    ],
)
def test_add_type_errors(a, b):
    """Passing non‑int arguments should raise TypeError."""
    with pytest.raises(TypeError):
        add_numbers(a, b)


# --------------------------------------------------------------------------- #
# Determinism and idempotence
# --------------------------------------------------------------------------- #

def test_add_deterministic():
    """Calling the function with the same arguments repeatedly yields the same result."""
    a, b = 42, -17
    first = add_numbers(a, b)
    for _ in range(10):
        assert add_numbers(a, b) == first


def test_add_no_side_effects():
    """The function should not modify its arguments."""
    a, b = 5, 10
    a_copy, b_copy = a, b
    _ = add_numbers(a, b)
    assert a == a_copy and b == b_copy, "Arguments were unexpectedly modified."
