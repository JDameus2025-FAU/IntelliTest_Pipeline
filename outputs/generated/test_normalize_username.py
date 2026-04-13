import pytest

from src.sample_functions import normalize_username


def test_normalization_basic():
    raw = "  User-Name_123  "
    expected = "user_name_123"
    assert normalize_username(raw) == expected


def test_separator_collapsing_and_trimming():
    # Multiple separators, leading/trailing underscores
    raw = "___User--__Name___"
    expected = "user_name"
    assert normalize_username(raw) == expected

    # Spaces and hyphens collapsed to underscores
    raw2 = "user - name"
    expected2 = "user_name"
    assert normalize_username(raw2) == expected2

    # Only separators should raise ValueError
    with pytest.raises(ValueError) as exc:
        normalize_username("___")
    assert str(exc.value) == "username must contain at least one alphanumeric character"


def test_invalid_inputs():
    # Empty string after stripping
    with pytest.raises(ValueError) as exc:
        normalize_username("   ")
    assert str(exc.value) == "username cannot be empty"

    # None input
    with pytest.raises(ValueError) as exc:
        normalize_username(None)
    assert str(exc.value) == "username cannot be None"
