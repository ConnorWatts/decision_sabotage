from .types import LLMSource
from .base import BaseLM
from ..models.types import ModelConfig


def create_language_model(model_config: ModelConfig) -> BaseLM:
    """
    Create a language model instance based on the provided configuration.

    Args:
        model_config: Configuration dictionary for the model.

    Returns:
        BaseLM: An instance of the specified language model.

    Raises:
        ValueError: If the model source is not supported.
    """
    try:
        source = LLMSource(model_config["source"])
    except ValueError:
        supported = ", ".join([s.value for s in LLMSource])
        raise ValueError(
            f"Unsupported model source: {model_config['source']}. "
            f"Supported sources are: {supported}"
        )

    if source == LLMSource.OPENAI:
        from .openai import OpenAILM

        return OpenAILM(model_config)

    elif source == LLMSource.ANTHROPIC:
        from .anthropic import AnthropicLM

        return AnthropicLM(model_config)

    elif source == LLMSource.GOOGLE:
        from .google import GoogleLM

        return GoogleLM(model_config)

    raise NotImplementedError(f"Support for {source.value} not yet implemented")
