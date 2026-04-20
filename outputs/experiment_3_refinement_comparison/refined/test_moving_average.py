import pytest
from src.sample_functions import moving_average


def test_moving_average_basic_and_type():
    values = [1, 2, 3, 4, 5]
    result = moving_average(values, 3)
    assert result == [2.0, 3.0, 4.0]
    assert isinstance(result, list)
    assert all(isinstance(v, float) for v in result)


def test_moving_average_rounding_precision():
    values = [1, 2, 3, 4]
    result = moving_average(values, 2)
    expected = [round(1.5, 2), round(2.5, 2), round(3.5, 2)]
    assert result == expected
    # verify each element is rounded to two decimals
    for r in result:
        assert round(r, 2) == r


def test_moving_average_window_size_one():
    values = [1, 2, 3]
    result = moving_average(values, 1)
    assert result == [1.0, 2.0, 3.0]
    # ensure original list is unmodified
    assert values == [1, 2, 3]


def test_moving_average_window_size_equals_length():
    values = [4, 5, 6]
    result = moving_average(values, 3)
    assert len(result) == 1
    assert result[0] == round(sum(values) / 3, 2)


def test_moving_average_empty_input_returns_empty():
    assert moving_average([], 1) == []


def test_moving_average_window_exceeds_length_raises():
    with pytest.raises(ValueError, match="cannot exceed the number of values"):
        moving_average([1, 2], 3)


def test_moving_average_non_positive_window_raises():
    with pytest.raises(ValueError, match="must be positive"):
        moving_average([1, 2, 3], 0)
    with pytest.raises(ValueError, match="must be positive"):
        moving_average([1, 2, 3], -1)


def test_moving_average_with_floats_and_rounding():
    values = [0.1, 0.2, 0.3, 0.4]
    result = moving_average(values, 2)
    expected = [round((0.1 + 0.2) / 2, 2), round((0.2 + 0.3) / 2, 2), round((0.3 + 0.4) / 2, 2)]
    assert result == expected
    for r in result:
        assert isinstance(r, float)


def test_moving_average_negative_numbers():
    values = [-1, -2, -3, -4]
    result = moving_average(values, 3)
    expected = [round((-1 + -2 + -3) / 3, 2), round((-2 + -3 + -4) / 3, 2)]
    assert result == expected
    assert all(isinstance(v, float) for v in result)


def test_moving_average_non_numeric_values_raises_type_error():
    with pytest.raises(TypeError):
        moving_average([1, "a", 3], 2)
    with pytest.raises(TypeError):
        moving_average([None, 2, 3], 2)
    with pytest.raises(TypeError):
        moving_average([1.0, complex(1, 0), 3.0], 2)


def test_moving_average_returns_new_list():
    values = [1, 2, 3, 4]
    result = moving_average(values, 2)
    # Ensure the returned list is not the same object as the input
    assert result is not values
    # Ensure modifications to result do not affect the original list
    result[0] = 999
    assert values == [1, 2, 3, 4]
    assert result == [999, 3.5, 5.5]


def test_moving_average_throws_on_zero_length_window_and_non_empty_values():
    with pytest.raises(ValueError, match="must be positive"):
        moving_average([1, 2, 3], 0)
    # also test negative window
    with pytest.raises(ValueError, match="must be positive"):
        moving_average([1, 2, 3], -5)
