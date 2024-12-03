from dataclasses import dataclass
from typing import List, Optional, Dict
from ..scenario.loader import Scenario


@dataclass
class Participant:
    """Represents a study participant."""

    id: str


@dataclass
class ParticipantMetrics:
    """Tracks participant behavior during experiment"""

    time_spent: float
    num_document_checks: int
    questions_asked: List[str]
    final_decision: str
    suspicion_score: int
    confidence_score: int
    reasoning: str


@dataclass
class InteractionResult:
    """Represents a single interaction between helper and participant"""

    question: str
    helper_response: str
    timestamp: float


@dataclass
class ExperimentResult:
    """Records the outcome of one participant's experiment."""

    experiment_type: str
    scenario: Scenario
    participant: Participant
    participant_metrics: ParticipantMetrics
    models: List[Dict]  # Maybe put base model in here
    interactions: List[InteractionResult]
    success: bool = True
    completion_status: Optional[str] = None

    def to_dict(self):
        return {
            "experiment_type": self.experiment_type,
            "scenario": self.scenario.to_dict(),
            "participant": self.participant.id,
            "participant_metrics": self.participant_metrics.__dict__,
            "models": self.models,
            "interactions": [interaction.__dict__ for interaction in self.interactions],
        }
