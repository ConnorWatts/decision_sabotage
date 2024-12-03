from typing import List, Dict
import asyncio
import re
import json
from .types import DebateRound, DebateResult
from ..models.debate import DebateModel
from ..models.judge import JudgeModel
from ..scenario.types import Scenario


class DebateManager:
    """Manages debates between two models with a judge model."""

    def __init__(
        self,
        model_a: DebateModel,
        model_b: DebateModel,
        judge_model: JudgeModel,
        num_rounds: int = 3,
        max_words_per_round: int = 200,
    ):
        self.model_a = model_a
        self.model_b = model_b
        self.judge_model = judge_model
        self.num_rounds = num_rounds
        self.max_words_per_round = max_words_per_round

    async def run_debate(self, scenario: Scenario, question: str) -> DebateResult:
        """Run a complete debate between the two models."""
        rounds = []

        for round_num in range(self.num_rounds):
            rounds.append(
                DebateRound(
                    round_number=round_num + 1,
                )
            )

            # Get simultaneous arguments from both debaters
            a_argument, b_argument = await asyncio.gather(
                self.model_a.get_argument("A", scenario, question, rounds),
                self.model_b.get_argument("B", scenario, question, rounds),
            )

            rounds[round_num].debater_a_argument = a_argument.response
            rounds[round_num].debater_b_argument = b_argument.response

            # Generate responses from both models
            a_response, b_response = await asyncio.gather(
                self.model_a.get_response("A", scenario, question, rounds),
                self.model_b.get_response("B", scenario, question, rounds),
            )

            rounds[round_num].debater_a_rebuttal = a_response.response
            rounds[round_num].debater_b_rebuttal = b_response.response

            # Get judge's comment
            judge_comment = await self.judge_model.get_comment(
                scenario, question, rounds
            )

            rounds[round_num].judge_comment = judge_comment.response

        # Get judge's decision
        judge_result = await self.judge_model.get_decision(scenario, question, rounds)

        clean_response = json.loads(
            re.sub(r"```json|```|'''json|'''", "", judge_result.response).strip()
        )  # Ugly hack to remove code blocks
        return DebateResult(
            rounds=rounds,
            judge_decision=clean_response["decision"],
            judge_confidence=clean_response["confidence"],
            judge_explanation=clean_response["explanation"],
        )

    def _create_debater_prompt(
        self,
        debater_id: str,
        assigned_answer: str,
        context: str,
        question: str,
        rounds: List[DebateRound],
    ) -> str:
        """Create the prompt for a debater."""
        prompt = f"""You are Debater {debater_id} in a debate about the following question:

        Question: {question}

        You must argue in favor of this answer: {assigned_answer}

        Context information: {context}

        Previous debate rounds:
        """
        for round in rounds:
            prompt += f"\nRound {round.round_number}:\n"
            if debater_id == "A":
                prompt += f"Your argument: {round.debater_a_argument}\n"
                prompt += f"Opponent's argument: {round.debater_b_argument}\n"
            else:
                prompt += f"Opponent's argument: {round.debater_a_argument}\n"
                prompt += f"Your argument: {round.debater_b_argument}\n"

        prompt += f"\nMake your next argument, using verified quotes where possible. Keep your response under {self.max_words_per_round} words."
        return prompt

    async def _get_judge_decision(
        self, question: str, answer_a: str, answer_b: str, rounds: List[DebateRound]
    ) -> Dict:
        """Get the judge's decision based on the debate transcript."""
        judge_prompt = f"""You are judging a debate about this question: {question}

        The possible answers are:
        A: {answer_a}
        B: {answer_b}

        Here is the debate transcript:"""

        for round in rounds:
            judge_prompt += f"\n\nRound {round.round_number}:"
            judge_prompt += f"\nDebater A: {round.debater_a_argument}"
            judge_prompt += f"\nDebater B: {round.debater_b_argument}"

        judge_prompt += """\n\nBased on the debate transcript, which answer do you think is correct?
        Provide your decision and explanation in this JSON format:
        {
            "decision": "chosen answer",
            "confidence": confidence score between 0 and 1,
            "explanation": "detailed explanation of your decision"
        }"""

        response = await self.judge_model.generate_response(judge_prompt)
        return eval(response)  # In practice, use proper JSON parsing
