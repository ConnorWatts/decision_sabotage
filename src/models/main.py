from typing import Union
from .types import ModelType, ModelBehaviourType, ModelConfig
from .helper import HelperModel
from .participant import ParticipantModel
from .debate import DebateModel
from .judge import JudgeModel
from ..llms.main import create_language_model

# Type mapping for model classes
MODEL_CLASS_MAP = {
    ModelType.HELPER: HelperModel,
    ModelType.PARTICIPANT: ParticipantModel,
    ModelType.DEBATE: DebateModel,
    ModelType.JUDGE: JudgeModel,
}


def create_model(
    model_type: ModelType, model_config: ModelConfig
) -> Union[HelperModel, ParticipantModel, DebateModel, JudgeModel]:
    """
    Create a model instance of the specified type with given configuration.

    Args:
        model_type: Type of model to create.
        model_config: Configuration dictionary for the model.

    Returns:
        An instance of the specified model type.

    Raises:
        ValueError: If the configuration is invalid.
        KeyError: If required configuration keys are missing.
    """
    # Validate configuration
    required_keys = {"source", "name"}
    if model_type != ModelType.PARTICIPANT:
        required_keys.add("behavior")

    missing_keys = required_keys - set(model_config.keys())
    if missing_keys:
        raise KeyError(f"Missing required configuration keys: {missing_keys}")

    # Create language model
    model_lm = create_language_model(model_config)

    # Create appropriate model instance
    model_class = MODEL_CLASS_MAP[model_type]
    if model_type == ModelType.PARTICIPANT:
        return model_class(model_lm)

    # For models that require behavior configuration
    try:
        model_behavior = ModelBehaviourType(model_config["behavior"])
    except ValueError:
        valid_behaviors = ", ".join([b.value for b in ModelBehaviourType])
        raise ValueError(
            f"Invalid behavior type: {model_config['behavior']}. "
            f"Valid behaviors are: {valid_behaviors}"
        )

    return model_class(model_lm, model_behavior)


# Factory functions for specific model types
def get_helper_model(model_config: ModelConfig) -> HelperModel:
    """Create a helper model instance."""
    return create_model(ModelType.HELPER, model_config)


def get_participant_model(model_config: ModelConfig) -> ParticipantModel:
    """Create a participant model instance."""
    return create_model(ModelType.PARTICIPANT, model_config)


def get_debate_model(model_config: ModelConfig) -> DebateModel:
    """Create a debate model instance."""
    return create_model(ModelType.DEBATE, model_config)


def get_judge_model(model_config: ModelConfig) -> JudgeModel:
    """Create a judge model instance."""
    return create_model(ModelType.JUDGE, model_config)
