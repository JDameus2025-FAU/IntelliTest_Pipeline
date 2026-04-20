import pytest
from src.sample_functions import normalize_username

def test_basic_normalization():
    raw = "  John-Doe_123   "
    expected = "john_doe123"
    assert normalize_username(raw) == expected

def test_collapse_multiple_separators():
    raw = "___a--b__c__"
    expected = "a_b_c"
    assert normalize_username(raw) == expected

def test_error_on_none_username():
    with pytest.raises(ValueError, match="cannot be None"):
        normalize_username(None)

def test_error_on_empty_or_only_separators():
    with pytest.raises(ValueError, match="cannot be empty"):
        normalize_username("   ")
    with pytest.raises(ValueError, match="must contain at least one alphanumeric"):
        normalize_username("___---___")
