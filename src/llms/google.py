from typing import Dict, Optional
import google.generativeai as genai
import os
import time
from .base import BaseLM
from .types import LLMResponse

### NOT WORKING - NEEDS TO BE FIXED ###


class GoogleLM(BaseLM):
    """Google Language Model wrapper for API interactions."""

    def __init__(self, config: Dict) -> None:
        """Initialize Google client with API key and model configuration."""
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")

        genai.configure(api_key=self.api_key)
        self.model_name = config.get("name", "gemini-pro")

        # Set default parameters
        self.default_params = {
            "temperature": config.get("temperature", 0.7),
            "top_p": config.get("top_p", 1.0),
            "top_k": config.get("top_k", 40),
            "max_output_tokens": config.get("max_tokens", 1024),
        }

        # Initialize the model
        self.model = genai.GenerativeModel(self.model_name)

    def generate(self, prompt: str, max_length: Optional[int] = None) -> LLMResponse:
        """Generate text using the Google Gemini API."""
        try:
            start_time = time.time()

            params = self.default_params.copy()
            if max_length is not None:
                params["max_output_tokens"] = max_length

            # Generate content
            response = self.model.generate_content(
                prompt, generation_config=genai.types.GenerationConfig(**params)
            )

            generation_time = time.time() - start_time

            # Extract the response text
            generated_text = response.text

            # Create metadata dictionary
            metadata = {
                "model": self.model_name,
                "finish_reason": response.prompt_feedback.block_reason or "stop",
                "safety_ratings": [
                    {"category": rating.category, "probability": rating.probability}
                    for rating in response.safety_ratings
                ],
            }

            # Create response object
            # Note: Google's API doesn't provide token counts directly
            return LLMResponse(
                response=generated_text,
                metadata=metadata,
                generation_time=generation_time,
                token_count=None,  # Google API doesn't provide token counts
            )

        except Exception as e:
            raise RuntimeError(f"Google API call failed: {str(e)}")

    def _get_model(self) -> str:
        """Get the current model name."""
        return self.model_name

    @staticmethod
    def list_available_models():
        """List all available Google AI models."""
        try:
            return [model.name for model in genai.list_models()]
        except Exception as e:
            raise RuntimeError(f"Failed to list Google AI models: {str(e)}")
