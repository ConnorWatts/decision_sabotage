from abc import ABC, abstractmethod
from .types import LLMResponse


class BaseLM(ABC):
    """Abstract base class for language models."""

    @abstractmethod
    async def generate(self, prompt: str) -> LLMResponse:
        pass
