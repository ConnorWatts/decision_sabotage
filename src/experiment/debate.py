from typing import Dict, List, Optional
import time
from .base import BaseSingleExperiment
from ..debate.manager import DebateManager
from ..models.debate import DebateModel
from ..models.judge import JudgeModel
from ..models.participant import ParticipantModel
from ..scenario.loader import Scenario
from .types import ExperimentResult, InteractionResult, ParticipantMetrics
from ..logger import get_experiment_logger
import json


class SingleDebateExperiment(BaseSingleExperiment):
    def __init__(
        self,
        experiment_config: Dict,
        debator_1: DebateModel,
        debator_2: DebateModel,
        judge: JudgeModel,
        participant: ParticipantModel,
        scenario: Scenario,
        time_limit: int = 1800,  # 30 minutes as in paper
    ):
        self.validate_config(experiment_config)
        self.config = experiment_config
        self.logger = get_experiment_logger("debate_experiment")
        self.logger.info(f"Initializing DebateExperiment with config: {self.config}")

        self.debator_1 = debator_1
        self.debator_2 = debator_2
        self.judge = judge
        self.participant_model = participant
        self.scenario = scenario
        self.time_limit = time_limit
        self.num_interactions = self.config["environment"]["num_interactions"]
        self.interactions: List[InteractionResult] = []
        self.start_time: Optional[float] = None
        self.debate_manager = DebateManager(self.debator_1, self.debator_2, self.judge)

    @staticmethod
    def validate_config(config: Dict) -> None:
        required_keys = {"models", "environment"}
        if not all(key in config for key in required_keys):
            raise ValueError(f"Missing required config keys: {required_keys}")

    def _check_time_remaining(self) -> float:
        """Check remaining time in experiment"""
        if self.start_time is None:
            raise ValueError("Experiment hasn't started")
        elapsed = time.time() - self.start_time
        remaining = self.time_limit - elapsed
        if remaining <= 0:
            raise TimeoutError("Experiment time limit reached")
        return remaining

    async def run(self) -> ExperimentResult:
        """Run a single experimental trial."""
        self.start_time = time.time()
        debate_responses = []
        participant_metrics = ParticipantMetrics(
            time_spent=0,
            num_document_checks=0,
            questions_asked=[],
            final_decision="",
            suspicion_score=0,
            confidence_score=0,
            reasoning="",
        )

        try:
            # Initial scenario review period (Not really relevant for LLMs)
            await self.participant_model.review_scenario(self.scenario)

            # Question-answer interactions
            for _ in range(self.num_interactions):
                # Generate contextual question
                question = await self.participant_model.generate_question(
                    scenario=self.scenario,
                    previous_interactions=self.interactions,
                    remaining_time=self._check_time_remaining(),
                )

                # Record question
                participant_metrics.questions_asked.append(question)

                # Get debate response (this needs to be fixed)
                debate_response = await self.debate_manager.run_debate(
                    scenario=self.scenario,
                    question=question,
                    # previous_interactions=self.interactions
                )

                # Record interaction
                interaction = InteractionResult(
                    question=question,
                    helper_response=debate_response,
                    timestamp=time.time(),
                )
                self.interactions.append(interaction)
                debate_responses.append(debate_response)

            # Final decision phase
            final_result = await self.participant_model.make_decision(
                scenario=self.scenario,
                previous_interactions=self.interactions,
                remaining_time=self._check_time_remaining(),
            )

            # Update metrics
            participant_metrics.time_spent = time.time() - self.start_time
            participant_metrics.final_decision = final_result["decision"]
            participant_metrics.suspicion_score = final_result["suspicion_rating"]
            participant_metrics.confidence_score = final_result.get("confidence", 0)
            participant_metrics.reasoning = final_result["reasoning"]

            return ExperimentResult(
                experiment_type=self.config["experiment_name"],
                scenario=self.scenario,
                participant=self.participant_model,
                participant_metrics=participant_metrics,
                models=[self.debator_1, self.debator_2, self.judge],
                interactions=self.interactions,
            )

        except TimeoutError:
            self.logger.warning("Experiment timed out")
            return ExperimentResult(
                experiment_type=self.config["experiment_name"],
                scenario=self.scenario,
                participant=self.participant_model,
                participant_metrics=participant_metrics,
                models=[self.debator_1, self.debator_2, self.judge],
                interactions=self.interactions,
                success=False,
                completion_status="timeout",
            )
        except Exception as e:
            self.logger.error(f"Experiment failed: {str(e)}")
            return ExperimentResult(
                experiment_type=self.config["experiment_name"],
                scenario=self.scenario,
                participant=self.participant_model,
                participant_metrics=participant_metrics,
                models=[self.debator_1, self.debator_2, self.judge],
                interactions=self.interactions,
                success=False,
                completion_status="error",
            )

    def save_results(self, result: ExperimentResult, output_path: str):
        """Save experimental results to file."""
        with open(output_path, "w") as f:
            json.dump(result.to_dict(), f, indent=2)
