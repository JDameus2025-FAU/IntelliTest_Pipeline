# IntelliTest Pipeline

IntelliTest Pipeline is a small Python research prototype for studying whether iterative LLM refinement improves automatically generated software tests.

The prototype:

- loads a small set of sample Python functions
- generates initial `pytest` tests with an LLM
- refines those tests in a second pass
- evaluates both versions with a transparent heuristic rubric
- writes a CSV comparison report and a short Markdown findings summary

## Project Layout

```text
IntelliTest_Pipeline/
├── outputs/
│   ├── experiment_1_simple_generation/
│   ├── experiment_2_complex_edge_generation/
│   ├── experiment_3_refinement_comparison/
│   └── final_report_summary.md
├── src/
│   ├── evaluate_tests.py
│   ├── generate_tests.py
│   ├── llm_client.py
│   ├── prompts.py
│   ├── refine_tests.py
│   ├── run_experiments.py
│   └── sample_functions.py
├── .env.example
├── README.md
└── requirements.txt
```

## Setup

1. Create and activate a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Create a `.env` file from the example.

```bash
cp .env.example .env
```

4. Add your API key to `.env`.

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-5.2
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
INTELLITEST_USE_MOCK=false
```

Provider examples:

For OpenAI:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-5.2
INTELLITEST_USE_MOCK=false
```

For Groq:

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
INTELLITEST_USE_MOCK=false
```

Note: the older Groq model `llama3-70b-8192` has been deprecated. Use `openai/gpt-oss-20b` or another currently supported Groq model instead.

## Run

Run the full experiment pipeline:

```bash
python src/run_experiments.py
```

If you want to test the pipeline structure without calling a live API, run:

```bash
python src/run_experiments.py --use-mock-llm
```

## Outputs

After a run, the project writes:

- Experiment 1 outputs to `outputs/experiment_1_simple_generation/`
- Experiment 2 outputs to `outputs/experiment_2_complex_edge_generation/`
- Experiment 3 outputs to `outputs/experiment_3_refinement_comparison/`
- a reusable research-style summary to `outputs/final_report_summary.md`

Each experiment folder contains its own `generated/` directory and `reports/` directory.
The refinement comparison experiment also includes a separate `refined/` directory.

## Evaluation Rubric

Each generated test file is scored with a simple heuristic rubric:

- `correctness` (1-5)
- `assertion_strength` (1-5)
- `edge_case_coverage` (1-5)
- `readability` (1-5)
- `notes`

The evaluator is intentionally lightweight and transparent. It uses static heuristics such as:

- whether the file parses as Python
- whether `assert` statements or `pytest.raises` blocks exist
- whether multiple test cases are present
- whether edge-oriented inputs such as `None`, empty values, boundary values, or exception checks appear
- whether the structure looks executable and readable

This makes the scoring easy to explain in a paper, even though it is not a substitute for full semantic correctness evaluation.

## Notes

- The prototype uses environment variables for API configuration.
- The default live client uses the OpenAI Python SDK and the Responses API.
- A mock mode is included so the pipeline can still be demonstrated offline or in restricted environments.
