from typing import Dict
from .base import BaseSingleExperiment


class SingleSandbaggingExperiment(BaseSingleExperiment):
    def __init__(self, config: Dict):
        super().__init__(config)
        self.num_attempts = config.get("num_attempts", 5)

    def run(self) -> Dict:
        # Implement sandbagging experiment run logic
        pass
