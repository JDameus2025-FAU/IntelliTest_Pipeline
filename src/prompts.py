from __future__ import annotations


GENERATION_SYSTEM_PROMPT = """You are generating pytest unit tests for a Python research prototype.
Return only executable Python code.
Do not include Markdown fences or explanations.
Requirements:
- Use pytest style tests.
- Import the target function from src.sample_functions.
- Write readable, focused unit tests.
- Include direct assertions.
- Prefer 2 to 4 tests in the initial pass.
"""


REFINEMENT_SYSTEM_PROMPT = """You are refining pytest unit tests for a Python research prototype.
Return only executable Python code.
Do not include Markdown fences or explanations.
Improve the original tests by:
- adding missing edge cases
- strengthening weak assertions
- improving completeness and readability
- preserving valid existing coverage where useful
"""


def build_generation_prompt(function_name: str, function_source: str, description: str) -> str:
    return f"""Generate initial pytest tests for the following Python function.

Function name:
{function_name}

Function description:
{description}

Function source:
```python
{function_source}
```

Return a complete pytest file that imports only what it needs from src.sample_functions.
"""


def build_refinement_prompt(
    function_name: str,
    function_source: str,
    existing_test_code: str,
    evaluation_notes: str,
) -> str:
    return f"""Refine the following pytest tests for the target function.

Target function:
{function_name}

Function source:
```python
{function_source}
```

Current test file:
```python
{existing_test_code}
```

Evaluator feedback:
{evaluation_notes}

Return a full improved pytest file for src.sample_functions.{function_name}.
"""
