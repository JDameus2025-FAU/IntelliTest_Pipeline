from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Any

from dotenv import load_dotenv

class LLMClientError(RuntimeError):
    """Raised when the configured LLM provider cannot complete a request."""

@dataclass(frozen=True)
class LLMConfig:
    provider_env_var: str = "LLM_PROVIDER"
    model_env_var: str = "LLM_MODEL"
    openai_api_key_env_var: str = "OPENAI_API_KEY"
    openai_model_env_var: str = "OPENAI_MODEL"
    groq_api_key_env_var: str = "GROQ_API_KEY"
    groq_model_env_var: str = "GROQ_MODEL"
    mock_env_var: str = "INTELLITEST_USE_MOCK"
    default_provider: str = "openai"
    default_openai_model: str = "gpt-5.2"
    default_groq_model: str = "openai/gpt-oss-20b"

class LLMClient:
    """Small wrapper that supports interchangeable OpenAI and Groq providers."""

    def __init__(self, use_mock: bool = False, model: str | None = None) -> None:
        load_dotenv()

        self.config = LLMConfig()
        env_mock_value = os.getenv(self.config.mock_env_var, "false").lower() == "true"
        self.use_mock = use_mock or env_mock_value
        self.provider = os.getenv(
            self.config.provider_env_var,
            self.config.default_provider,
        ).strip().lower()

        self.model = model or self._resolve_model()
        self.api_key = self._resolve_api_key()
        self._client: Any | None = None

        if not self.use_mock and self.api_key:
            self._client = self._build_provider_client()

    @property
    def mode_label(self) -> str:
        return "mock" if self.use_mock else self.provider

    def complete(self, instructions: str, prompt: str) -> str:
        if self.use_mock:
            raise LLMClientError("Mock mode is enabled, so no live API request was made.")

        if self.provider not in {"openai", "groq"}:
            raise LLMClientError(
                f"Unsupported LLM_PROVIDER '{self.provider}'. Use 'openai' or 'groq'."
            )

        if not self.api_key:
            raise LLMClientError(
                f"Missing API key for provider '{self.provider}'. "
                f"Set {self._api_key_env_var_for_provider()} or use --use-mock-llm."
            )

        if self._client is None:
            self._client = self._build_provider_client()

        try:
            if self.provider == "openai":
                return self._complete_with_openai(instructions, prompt)
            return self._complete_with_groq(instructions, prompt)
        except Exception as exc:
            raise LLMClientError(f"{self.provider.capitalize()} request failed: {exc}") from exc

    def _resolve_model(self) -> str:
        generic_model = os.getenv(self.config.model_env_var)
        if generic_model:
            return generic_model

        if self.provider == "groq":
            return os.getenv(
                self.config.groq_model_env_var,
                self.config.default_groq_model,
            )

        return os.getenv(
            self.config.openai_model_env_var,
            self.config.default_openai_model,
        )

    def _resolve_api_key(self) -> str | None:
        env_var_name = self._api_key_env_var_for_provider()
        return os.getenv(env_var_name)

    def _api_key_env_var_for_provider(self) -> str:
        if self.provider == "groq":
            return self.config.groq_api_key_env_var
        return self.config.openai_api_key_env_var

    def _build_provider_client(self) -> Any:
        if self.provider == "groq":
            return self._build_groq_client()
        if self.provider == "openai":
            return self._build_openai_client()
        raise LLMClientError(
            f"Unsupported LLM_PROVIDER '{self.provider}'. Use 'openai' or 'groq'."
        )

    def _build_openai_client(self) -> Any:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise LLMClientError(
                "The openai package is not installed. Install requirements or run with --use-mock-llm."
            ) from exc

        return OpenAI(api_key=self.api_key)

    def _build_groq_client(self) -> Any:
        try:
            from groq import Groq
        except ImportError as exc:
            raise LLMClientError(
                "The groq package is not installed. Install requirements or run with --use-mock-llm."
            ) from exc

        return Groq(api_key=self.api_key)

    def _complete_with_openai(self, instructions: str, prompt: str) -> str:
        response = self._client.responses.create(
            model=self.model,
            instructions=instructions,
            input=prompt,
        )

        output_text = getattr(response, "output_text", "")
        if not output_text:
            raise LLMClientError("The OpenAI response did not contain output_text.")
        return output_text.strip()

    def _complete_with_groq(self, instructions: str, prompt: str) -> str:
        completion = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": prompt},
            ],
        )

        if not completion.choices:
            raise LLMClientError("The Groq response did not contain any choices.")

        message = completion.choices[0].message
        content = getattr(message, "content", "")
        if not content:
            raise LLMClientError("The Groq response did not contain message content.")
        return content.strip()
