from enum import Enum
from dataclasses import dataclass
from typing import Literal


class ModelType(Enum):
    """Types of models available in the system."""

    HELPER = "helper"
    PARTICIPANT = "participant"
    DEBATE = "debate"
    JUDGE = "judge"


class ModelBehaviourType(str, Enum):
    """Types of model behavior for the experiment."""

    CONTROL = "control"
    AGGRESSIVE = "aggressive"
    MODERATE = "moderate"
    SUBTLE = "subtle"
    SANDBAGGING = "sandbagging"


@dataclass
class ModelConfig:
    """Configuration for a (LLM) model."""

    # TODO: Name better (for llm specific config)
    source: Literal["openai", "anthropic"]
    name: str
    temperature: float
    behavior: ModelBehaviourType
