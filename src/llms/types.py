from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass


class LLMSource(Enum):
    """Supported model sources."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"  # Future support
    LOCAL = "local"  # Future support


@dataclass
class LLMResponse:
    """Response from a model."""

    response: str
    metadata: Optional[Dict[str, Any]] = None
    generation_time: Optional[float] = None
    token_count: Optional[int] = None
