from typing import Dict, Optional
from anthropic import Anthropic
import os
import time
from .base import BaseLM
from .types import LLMResponse


class AnthropicLM(BaseLM):
    """Anthropic Language Model wrapper for API interactions."""

    def __init__(self, config: Dict) -> None:
        """Initialize Anthropic client with API key and model configuration."""
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.client = Anthropic(api_key=self.api_key)
        self.model_name = config.get("name", "claude-3-opus-20240229")
        self.default_params = {
            "temperature": config.get("temperature", 0.7),
            "max_tokens": config.get("max_tokens", 1000),
            "top_p": config.get("top_p", 1.0),
        }

    def generate(self, prompt: str, max_length: Optional[int] = None) -> LLMResponse:
        """Generate text using the Anthropic API."""
        try:
            start_time = time.time()

            params = self.default_params.copy()
            if max_length is not None:
                params["max_tokens"] = max_length

            response = self.client.messages.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                **params,
            )

            generation_time = time.time() - start_time
            generated_text = response.content[0].text

            return LLMResponse(
                response=generated_text,
                metadata={
                    "model": self.model_name,
                    "stop_reason": response.stop_reason,
                    "usage": {
                        "input_tokens": response.usage.input_tokens,
                        "output_tokens": response.usage.output_tokens,
                    },
                },
                generation_time=generation_time,
                token_count=response.usage.output_tokens,
            )

        except Exception as e:
            raise RuntimeError(f"Anthropic API call failed: {str(e)}")

    def _get_model(self) -> str:
        """Get the current model name."""
        return self.model_name
