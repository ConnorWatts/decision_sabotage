from enum import Enum
from dataclasses import dataclass
from typing import Dict, List


class ScenarioType(Enum):
    """Types of scenarios available for experiments."""

    BUSINESS_EXPANSION = "business_expansion"
    MERGER_DECISION = "merger_decision"  # Not Supported
    PRODUCT_LAUNCH = "product_launch"  # Not Supported
    WORKFORCE_STRATEGY = "workforce_strategy"  # Not Supported
    TECHNOLOGY_ADOPTION = "technology_adoption"  # Not Supported


@dataclass
class Document:
    """Represents a single document in the scenario."""

    title: str
    content: str
    key_points: List[str]
    metadata: Dict


# this needs to be improved
@dataclass
class Scenario:
    """Represents a business decision scenario."""

    decision: str
    correct_answer: str
    context: str
    documents: List[Dict]
