import pytest
from src.sample_functions import normalize_username


def test_normalize_username_lowercases_and_strips_spaces():
    assert normalize_username("  Alice Smith  ") == "alice_smith"


def test_normalize_username_handles_hyphens():
    assert normalize_username("Team-Lead") == "team_lead"
