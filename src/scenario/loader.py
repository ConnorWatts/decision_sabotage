import json
from pathlib import Path
from typing import Dict, List
from .types import ScenarioType, Scenario


class ScenarioLoader:
    """Load scenarios for the sabotage evaluation."""

    def __init__(
        self, scenario_type: ScenarioType, templates_path: str = "data/scenarios"
    ) -> None:
        """Initialize the scenario generator.

        Args:
            scenario (Scenario): The type of scenario to generate.
            templates_path (str): Path to scenario templates directory.
        """
        self.scenario_type = scenario_type
        self.templates_path = Path(templates_path)
        self.scenario = self._load_scenario()

    def _load_scenario(self) -> Scenario:
        """Load the specific scenario template from disk."""
        scenario_file = self.templates_path / f"{self.scenario_type}.json"
        if not scenario_file.exists():
            raise FileNotFoundError(f"Scenario file '{scenario_file}' does not exist.")

        with open(scenario_file, "r") as f:
            json_data = json.load(f)

        return Scenario(**json_data)


class ScenarioGenerator:
    """Generate scenarios for the sabotage evaluation."""

    @staticmethod
    def generate_scenario(
        self, word_count: int = 40000, num_documents: int = 20
    ) -> Dict:
        """Generate a complete business decision scenario.

        Args:
            word_count: Target total word count for all documents
            num_documents: Number of background documents to generate

        Returns:
            Dict containing scenario data
        """

        scenario = {
            "decision": self.scenario["decision"],
            "correct_answer": self.scenario["correct_answer"],
            "context": self.scenario["context"],
            "documents": self._generate_documents(
                self.scenario, word_count, num_documents
            ),
        }

        return scenario

    @staticmethod
    def get_scenario(self) -> Dict:
        """Generate a complete business decision scenario.

        Args:
            word_count: Target total word count for all documents
            num_documents: Number of background documents to generate

        Returns:
            Dict containing scenario data
        """

        scenario = {
            "decision": self.scenario["decision"],
            "correct_answer": self.scenario["correct_answer"],
            "context": self.scenario["context"],
            "documents": self.scenario["documents"],
        }

        return scenario

    def _generate_documents(
        self, template: Dict, total_words: int, num_docs: int
    ) -> List[Dict]:
        """Generate the background documents for a scenario."""
        # Implementation would use an LLM to generate detailed documents
        pass
