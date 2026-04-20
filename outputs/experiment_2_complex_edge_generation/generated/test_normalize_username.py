import pytest
from src.sample_functions import normalize_username

def test_normalize_with_mixed_separators():
    assert normalize_username("  Alice-__Bob  ") == "alice_bob"

def test_normalize_trims_and_collapses_only_separators():
    with pytest.raises(ValueError, match="username must contain at least one alphanumeric character"):
        normalize_username("__--  ")

def test_normalize_raises_on_none_and_empty():
    with pytest.raises(ValueError, match="username cannot be None"):
        normalize_username(None)

    with pytest.raises(ValueError, match="username cannot be empty"):
        normalize_username("   ")

def test_normalize_leads_and_trailing_underscores_removed():
    assert normalize_username(" _John_ ") == "john"
