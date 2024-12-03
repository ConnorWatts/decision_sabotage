from typing import Dict, Optional
from openai import OpenAI
import os
import time
from .base import BaseLM
from .types import LLMResponse

# TODO: Add check for model_name and whether it is a valid OpenAI model


class OpenAILM(BaseLM):
    """OpenAI Language Model wrapper for API interactions."""

    def __init__(self, config: Dict) -> None:
        """Initialize OpenAI client with API key and model configuration.

        Args:
            config (Dict): Configuration containing model name and parameters
                Expected format:
                {
                    "name": "gpt-4o",  # or other OpenAI model
                    "temperature": 0.7,
                    "max_tokens": 100,
                    # other OpenAI parameters...
                }
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.client = OpenAI(api_key=self.api_key)
        self.model_name = config.get("name", "gpt-4o")
        self.default_params = {
            "temperature": config.get("temperature", 0.7),
            "max_tokens": config.get("max_tokens", 200),
            "top_p": config.get("top_p", 1.0),
            "frequency_penalty": config.get("frequency_penalty", 0.0),
            "presence_penalty": config.get("presence_penalty", 0.0),
        }

    async def generate(
        self, prompt: str, max_length: Optional[int] = None
    ) -> LLMResponse:
        """Generate text using the OpenAI API.

        Args:
            prompt (str): Input text to generate from
            max_length (Optional[int]): Maximum length of generated text
                                      Overrides default if provided

        Returns:
            ModelResponse: Container with generated text and metadata
        """
        try:
            start_time = time.time()

            params = self.default_params.copy()
            if max_length is not None:
                params["max_tokens"] = max_length

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                **params,
            )

            generation_time = time.time() - start_time
            generated_text = response.choices[0].message.content

            return LLMResponse(
                response=generated_text,
                metadata={
                    "model": self.model_name,
                    "finish_reason": response.choices[0].finish_reason,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens,
                    },
                },
                generation_time=generation_time,
                token_count=response.usage.completion_tokens,
            )

        except Exception as e:
            raise RuntimeError(f"OpenAI API call failed: {str(e)}")

    def _get_model(self) -> str:
        """Get the current model name.

        Returns:
            str: Name of the OpenAI model being used
        """
        return self.model_name
