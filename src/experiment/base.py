from abc import ABC, abstractmethod
from .types import ExperimentResult
from typing import Dict


class BaseSingleExperiment(ABC):
    """Abstract base class for all experiments."""

    def __init__(self, config: Dict):
        self.config = config

    @abstractmethod
    def run(self) -> ExperimentResult:
        """Run the experiment and return results."""
        pass
