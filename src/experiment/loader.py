from dataclasses import dataclass
from typing import Dict, Type, TypeVar, Mapping
from enum import Enum, auto

from .base import BaseSingleExperiment
from .classic import SingleClassicExperiment
from .debate import SingleDebateExperiment
from ..models.main import (
    get_helper_model,
    get_participant_model,
    get_debate_model,
    get_judge_model,
)
from ..scenario.loader import ScenarioLoader

T = TypeVar("T", bound=BaseSingleExperiment)


class ExperimentType(Enum):
    """Supported experiment types with auto-generated values."""

    CLASSIC = auto()
    DEBATE = auto()
    # SAND = auto()  # Future support

    @classmethod
    def from_string(cls, name: str) -> "ExperimentType":
        """Convert string to ExperimentType, case-insensitive."""
        try:
            return cls[name.upper()]
        except KeyError:
            raise ValueError(
                f"Unknown experiment type: {name}. Valid types: {[e.name.lower() for e in cls]}"
            )


@dataclass
class ExperimentConfig:
    """Structured configuration for experiments."""

    experiment_name: str
    models: Dict[str, Dict]
    scenario: str
    environment: Dict

    @classmethod
    def from_dict(cls, config: Dict) -> "ExperimentConfig":
        """Create ExperimentConfig from dictionary with validation."""
        required_keys = {"experiment_name", "models", "scenario", "environment"}
        missing_keys = required_keys - set(config.keys())
        if missing_keys:
            raise ValueError(f"Missing required configuration keys: {missing_keys}")
        return cls(**{k: config[k] for k in required_keys})


class ExperimentLoader:
    """Factory for creating experiment instances."""

    _experiment_builders: Mapping[ExperimentType, Type[BaseSingleExperiment]] = {
        ExperimentType.CLASSIC: SingleClassicExperiment,
        ExperimentType.DEBATE: SingleDebateExperiment,
    }

    @classmethod
    def create_experiment(cls, config_dict: Dict) -> BaseSingleExperiment:
        """Create an experiment instance from configuration dictionary."""
        config = ExperimentConfig.from_dict(config_dict)
        experiment_type = ExperimentType.from_string(config.experiment_name)

        builder = cls._experiment_builders.get(experiment_type)
        if not builder:
            raise ValueError(
                f"No experiment implementation for type: {experiment_type}"
            )

        if experiment_type == ExperimentType.CLASSIC:
            return cls._create_classic_experiment(config)
        elif experiment_type == ExperimentType.DEBATE:
            return cls._create_debate_experiment(config)

        raise ValueError(f"Unhandled experiment type: {experiment_type}")

    @staticmethod
    def _create_classic_experiment(config: ExperimentConfig) -> SingleClassicExperiment:
        """Create a classic experiment with validated configuration."""
        try:
            helper_model = get_helper_model(config.models["helper"])
            participant_model = get_participant_model(config.models["participant"])
        except KeyError as e:
            raise ValueError(f"Missing required model configuration: {e}")

        scenario = ScenarioLoader(scenario_type=config.scenario).scenario

        return SingleClassicExperiment(
            experiment_config=config.__dict__,
            helper=helper_model,
            participant=participant_model,
            scenario=scenario,
        )

    @staticmethod
    def _create_debate_experiment(config: ExperimentConfig) -> SingleDebateExperiment:
        """Create a debate experiment with validated configuration."""
        try:
            debate_model_1 = get_debate_model(config.models["debater_1"])
            debate_model_2 = get_debate_model(config.models["debater_2"])
            judge_model = get_judge_model(config.models["judge"])
            participant_model = get_participant_model(config.models["participant"])
        except KeyError as e:
            raise ValueError(f"Missing required model configuration: {e}")

        scenario = ScenarioLoader(scenario_type=config.scenario).scenario

        return SingleDebateExperiment(
            experiment_config=config.__dict__,
            debator_1=debate_model_1,
            debator_2=debate_model_2,
            judge=judge_model,
            participant=participant_model,
            scenario=scenario,
        )
