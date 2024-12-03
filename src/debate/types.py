from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DebateRound:
    """Represents a single round of debate."""

    round_number: int
    debater_a_argument: Optional[str] = None
    debater_b_argument: Optional[str] = None
    debater_a_rebuttal: Optional[str] = None
    debater_b_rebuttal: Optional[str] = None
    judge_comment: Optional[str] = None


@dataclass
class DebateResult:
    """Contains the complete debate results and final decision."""

    rounds: List[DebateRound]
    judge_decision: str
    judge_confidence: float
    judge_explanation: str
