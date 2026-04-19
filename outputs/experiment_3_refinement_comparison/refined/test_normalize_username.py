import pytest
from src.sample_functions import normalize_username


def test_normalize_username_normalizes_spacing_case_and_hyphens():
    assert normalize_username("  Alice Smith  ") == "alice_smith"
    assert normalize_username("Team-Lead") == "team_lead"


def test_normalize_username_collapses_repeated_separators():
    assert normalize_username("Data__Team---Lead") == "data_team_lead"


def test_normalize_username_removes_non_alphanumeric_symbols():
    assert normalize_username("User!@# Name") == "user_name"


def test_normalize_username_rejects_empty_and_invalid_values():
    with pytest.raises(ValueError):
        normalize_username("   ")

    with pytest.raises(ValueError):
        normalize_username("!!!")

    with pytest.raises(ValueError):
        normalize_username(None)
