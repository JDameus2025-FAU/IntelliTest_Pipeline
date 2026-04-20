import re
import pytest
from src.sample_functions import normalize_username


def _is_valid_normalized(name: str) -> bool:
    """Helper to assert that a normalized username matches expected rules."""
    # Must be non‑empty, only lowercase alphanumerics or underscore
    return bool(name) and re.fullmatch(r"[a-z0-9_]+", name) is not None


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("  John_Doe  ", "john_doe"),
        ("__John--Doe__", "john_doe"),
        ("-John-", "john"),
        ("a__b", "a_b"),
        ("John!Doe", "johndoe"),
        ("JOHN_DOE", "john_doe"),
        ("User123", "user123"),
        ("A!B@C", "abc"),
        ("John   Doe", "john_doe"),
        ("John-__Doe", "john_doe"),
        ("  a__b  ", "a_b"),
        ("___a", "a"),
        ("a___b", "a_b"),
        ("___", None),  # expect error
        ("!!!", None),  # expect error
        ("éclair", "éclair"),  # unicode preserved
        ("ÉCLAIR", "éclair"),
        ("123", "123"),
        ("  ", None),  # expect error
        ("", None),   # expect error
    ],
)
def test_normalize_various_cases(raw, expected):
    if expected is None:
        with pytest.raises(ValueError):
            normalize_username(raw)
    else:
        result = normalize_username(raw)
        assert result == expected
        assert _is_valid_normalized(result)


def test_collapse_multiple_separators_and_strip():
    input_str = "a---b__c---__--d"
    expected = "a_b_c_d"
    result = normalize_username(input_str)
    assert result == expected
    # Verify no double underscores
    assert "__" not in result
    # Verify no leading/trailing underscore
    assert not result.startswith("_")
    assert not result.endswith("_")
    assert _is_valid_normalized(result)


def test_all_separators_raise_error():
    separators = ["_", "-", " ", "__", "---", "  ", "___---___"]
    for sep in separators:
        with pytest.raises(ValueError, match="alphanumeric"):
            normalize_username(sep)


def test_none_input_raises_value_error():
    with pytest.raises(ValueError, match="None"):
        normalize_username(None)


def test_empty_or_whitespace_input_raises_value_error():
    for raw in ["   ", "\t\n", ""]:
        with pytest.raises(ValueError, match="empty"):
            normalize_username(raw)


def test_output_contains_only_allowed_characters():
    for raw in [
        "Alpha_Beta-123",
        "   Mix-____Case   ",
        "N0n-Alphanum!@#",
        "  001-___002__",
    ]:
        result = normalize_username(raw)
        assert _is_valid_normalized(result), f"Invalid characters in {result!r}"


def test_unicode_and_case_handling():
    raw = "ÜBER---Test___ÄÜÖ"
    expected = "über_test_äüö"
    assert normalize_username(raw) == expected


def test_long_input_performance_and_consistency():
    raw = ("a" * 1000) + "____" + ("b" * 1000) + "__" + ("c" * 1000)
    expected = f"{'a'*1000}_b{'c'*1000}"
    result = normalize_username(raw)
    assert result == expected
    # Ensure the function did not raise and result is valid
    assert _is_valid_normalized(result) and len(result) == len(expected)
