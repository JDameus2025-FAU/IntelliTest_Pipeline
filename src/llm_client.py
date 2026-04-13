from __future__ import annotations

from dataclasses import dataclass
import os

from dotenv import load_dotenv


class LLMClientError(RuntimeError):
    """Raised when the live LLM client cannot complete a request."""


@dataclass(frozen=True)
class LLMConfig:
    api_key_env_var: str = "OPENAI_API_KEY"
    model_env_var: str = "OPENAI_MODEL"
    mock_env_var: str = "INTELLITEST_USE_MOCK"
    default_model: str = "gpt-5.2"


class LLMClient:
    """Small wrapper around the OpenAI Responses API for experiment use."""

    def __init__(self, use_mock: bool = False, model: str | None = None) -> None:
        load_dotenv()

        self.config = LLMConfig()
        env_mock_value = os.getenv(self.config.mock_env_var, "false").lower() == "true"
        self.use_mock = use_mock or env_mock_value
        self.model = model or os.getenv(self.config.model_env_var, self.config.default_model)
        self.api_key = os.getenv(self.config.api_key_env_var)
        self._client = None

        if not self.use_mock and self.api_key:
            self._client = self._build_openai_client()

    def _build_openai_client(self):
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise LLMClientError(
                "The openai package is not installed. Install requirements or run with --use-mock-llm."
            ) from exc

        return OpenAI(api_key=self.api_key)

    @property
    def mode_label(self) -> str:
        return "mock" if self.use_mock else "openai"

    def complete(self, instructions: str, prompt: str) -> str:
        if self.use_mock:
            raise LLMClientError("Mock mode is enabled, so no live API request was made.")

        if not self.api_key:
            raise LLMClientError(
                "OPENAI_API_KEY is not set. Add it to your environment or use --use-mock-llm."
            )

        if self._client is None:
            self._client = self._build_openai_client()

        try:
            response = self._client.responses.create(
                model=self.model,
                instructions=instructions,
                input=prompt,
            )
        except Exception as exc:
            raise LLMClientError(f"OpenAI request failed: {exc}") from exc

        output_text = getattr(response, "output_text", "")
        if not output_text:
            raise LLMClientError("The API response did not contain output_text.")
        return output_text.strip()
