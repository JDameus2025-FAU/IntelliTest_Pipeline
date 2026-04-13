import re
import pytest

from src.sample_functions import normalize_username


@pytest.mark.parametrize(
    "raw,expected",
    [
        # Basic normalization
        ("  User-Name_123  ", "user_name_123"),
        ("___User--__Name___", "user_name"),
        ("user - name", "user_name"),
        ("user--name", "user_name"),
        ("user__name", "user_name"),
        ("user___name", "user_name"),
        ("user   name", "user_name"),
        ("   user   ", "user"),
        ("user   ", "user"),
        ("   user", "user"),
        ("user", "user"),
        ("  u  ", "u"),
        ("  123  ", "123"),
        ("  1-2-3  ", "1_2_3"),
        ("a-b", "a_b"),
        ("a_b", "a_b"),
        ("a__b", "a_b"),
        ("a___b", "a_b"),
        ("a - b", "a_b"),
        ("a   b", "a_b"),
        ("a_ b", "a_b"),
        ("Ü-ß", "ü_ß"),
        ("Üß", "üß"),
        ("Üß-", "üß"),
        ("Üß   -", "üß"),
        ("Üß-1", "üß_1"),
        ("abc!def", "abcdef"),
        ("abc! def", "abc_def"),
        ("abc! def?", "abc_def"),
        ("abc", "abc"),
        ("ABC", "abc"),
        ("AbC", "abc"),
    ],
)
def test_normalization_valid(raw: str, expected: str) -> None:
    result = normalize_username(raw)
    assert isinstance(result, str)
    assert result == expected
    # only lowercase letters, digits, underscores
    assert re.fullmatch(r"[a-z0-9_]+", result), f"Result contains invalid characters: {result}"
    # no leading or trailing underscores
    assert not result.startswith("_") and not result.endswith("_")
    # no consecutive underscores
    assert "__" not in result


@pytest.mark.parametrize(
    "raw,expected_error",
    [
        ("___", "username must contain at least one alphanumeric character"),
        ("!!!", "username must contain at least one alphanumeric character"),
        ("   !!!   ", "username must contain at least one alphanumeric character"),
        ("_", "username must contain at least one alphanumeric character"),
        ("", "username cannot be empty"),
        ("   ", "username cannot be empty"),
        (None, "username cannot be None"),
    ],
)
def test_normalization_invalid(raw: str | None, expected_error: str) -> None:
    with pytest.raises(ValueError) as exc:
        normalize_username(raw)  # type: ignore[arg-type]
    assert str(exc.value) == expected_error


def test_unicode_case_handling() -> None:
    # Unicode letters should be lowercased correctly
    input_str = "ÜßÄÖü"
    expected = "üßäöü"
    assert normalize_username(input_str) == expected
    # Verify that uppercase letters are lowered
    assert normalize_username("Ü") == "ü"
    assert normalize_username("ß") == "ß"


def test_long_username() -> None:
    long_input = ("A" * 1000) + ("-" * 500) + ("B" * 1000)
    expected = ("a" * 1000) + ("_" * 1) + ("b" * 1000)
    result = normalize_username(long_input)
    assert result == expected
    assert len(result) == 2001  # 1000 + 1 + 1000


def test_no_double_underscore_after_collapsing() -> None:
    raw = "a---b___c---d"
    result = normalize_username(raw)
    assert "__" not in result
    assert result == "a_b_c_d"


def test_ignoring_non_separator_non_alnum() -> None:
    raw = "user@#%name!"
    result = normalize_username(raw)
    assert result == "username"
    # Ensure all punctuation removed
    assert re.fullmatch(r"[a-z0-9_]+", result)


def test_input_with_only_separators_and_whitespace() -> None:
    # Leading/trailing whitespace plus separators should still raise
    with pytest.raises(ValueError):
        normalize_username("   ___   ")
    # Should raise same message as other separator-only cases
    with pytest.raises(ValueError) as exc:
        normalize_username("___")
    assert str(exc.value) == "username must contain at least one alphanumeric character"
    # Mixed whitespace and separators but no alphanum
    with pytest.raises(ValueError):
        normalize_username(" - - - ")
        # same error message
        with pytest.raises(ValueError) as exc:
            normalize_username(" - - - ")
        assert str(exc.value) == "username must contain at least one alphanumeric character"
