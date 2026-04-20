from __future__ import annotations

from dataclasses import dataclass
import inspect

def add_numbers(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b

def classify_score(score: int) -> str:
    """Classify a numeric score into a letter-style performance bucket."""
    if score < 0 or score > 100:
        raise ValueError("score must be between 0 and 100")

    if score >= 90:
        return "excellent"
    if score >= 75:
        return "good"
    if score >= 60:
        return "pass"
    return "fail"


def normalize_username(raw_username: str) -> str:
    """Normalize a username by trimming whitespace and collapsing separators."""
    if raw_username is None:
        raise ValueError("username cannot be None")

    candidate = raw_username.strip().lower()
    if not candidate:
        raise ValueError("username cannot be empty")

    normalized_chars: list[str] = []
    for char in candidate:
        if char.isalnum():
            normalized_chars.append(char)
        elif char in {" ", "-", "_"}:
            normalized_chars.append("_")

    normalized = "".join(normalized_chars)
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    normalized = normalized.strip("_")

    if not normalized:
        raise ValueError("username must contain at least one alphanumeric character")

    return normalized

def moving_average(values: list[float], window_size: int) -> list[float]:
    """Compute a rounded moving average using a fixed-size sliding window."""
    if window_size <= 0:
        raise ValueError("window_size must be positive")
    if not values:
        return []
    if window_size > len(values):
        raise ValueError("window_size cannot exceed the number of values")

    averages: list[float] = []
    for start_index in range(len(values) - window_size + 1):
        window = values[start_index : start_index + window_size]
        averages.append(round(sum(window) / window_size, 2))
    return averages


@dataclass(frozen=True)
class SampleFunction:
    name: str
    source_code: str
    description: str
    condition: str

def load_sample_functions() -> list[SampleFunction]:
    """Return the small benchmark set used in the experiment."""
    functions = [
        (add_numbers, "simple"),
        (classify_score, "complex_edge"),
        (normalize_username, "complex_edge"),
        (moving_average, "complex_edge"),
    ]

    return [
        SampleFunction(
            name=function.__name__,
            source_code=inspect.getsource(function),
            description=inspect.getdoc(function) or "",
            condition=condition,
        )
        for function, condition in functions
    ]
