import pytest
from src.sample_functions import normalize_username

def test_basic_normalization():
    # Whitespace trimming and case conversion
    assert normalize_username("  Alice- Bob  ") == "alice_bob"
    # Multiple separators collapse into a single underscore
    assert normalize_username("User__Name") == "user_name"

def test_separators_and_special_characters():
    # Special characters are removed
    assert normalize_username("John$%Doe") == "johndoe"
    # Leading and trailing separators are trimmed
    assert normalize_username("__User-Name__") == "user_name"

def test_none_input_raises():
    with pytest.raises(ValueError, match="username cannot be None"):
        normalize_username(None)

def test_invalid_username_raises():
    # Empty string after stripping
    with pytest.raises(ValueError, match="username cannot be empty"):
        normalize_username("   ")
    # Username with only separators
    with pytest.raises(ValueError, match="username must contain at least one alphanumeric character"):
        normalize_username("___")
        normalize_username("--")
        normalize_username(" ")
        normalize_username("")
