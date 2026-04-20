import pytest
from src.sample_functions import normalize_username

def test_basic_normalization():
    assert normalize_username("  John_Doe  ") == "john_doe"

def test_collapse_and_trim_separators():
    assert normalize_username("__John--Doe__") == "john_doe"
    assert normalize_username("-John-") == "john"
    assert normalize_username("a__b") == "a_b"

def test_remove_non_alphanumeric_and_case():
    assert normalize_username("John!Doe") == "johndoe"
    assert normalize_username("JOHN_DOE") == "john_doe"

def test_invalid_inputs():
    with pytest.raises(ValueError, match="None"):
        normalize_username(None)
    with pytest.raises(ValueError, match="empty"):
        normalize_username("   ")
    with pytest.raises(ValueError, match="at least one alphanumeric"):
        normalize_username("__")
