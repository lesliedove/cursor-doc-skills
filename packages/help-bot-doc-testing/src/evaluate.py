"""Evaluate AI engine responses using DeepEval metrics."""

from __future__ import annotations

from dataclasses import dataclass, field
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    GEval,
)

from .engines.base import EngineResult
from .question_bank import TestQuestion


@dataclass
class EvalScore:
    """Evaluation scores for a single engine response."""

    question_id: str
    engine: str
    answer_relevancy: float | None = None
    faithfulness: float | None = None
    correctness: float | None = None
    cites_ansys_help: bool = False
    mentions_product: bool = False
    errors: list[str] = field(default_factory=list)

    @property
    def overall_pass(self) -> bool:
        """Pass if correctness >= 0.6 and faithfulness >= 0.5."""
        if self.correctness is None or self.faithfulness is None:
            return False
        return self.correctness >= 0.6 and self.faithfulness >= 0.5

    def to_dict(self) -> dict:
        return {
            "question_id": self.question_id,
            "engine": self.engine,
            "answer_relevancy": self.answer_relevancy,
            "faithfulness": self.faithfulness,
            "correctness": self.correctness,
            "cites_ansys_help": self.cites_ansys_help,
            "mentions_product": self.mentions_product,
            "overall_pass": self.overall_pass,
            "errors": self.errors,
        }


_correctness_metric = None


def _get_correctness_metric():
    global _correctness_metric
    if _correctness_metric is None:
        _correctness_metric = GEval(
            name="Correctness",
            criteria=(
                "Determine whether the actual output is factually correct based on the "
                "expected output. Focus on key technical facts: product names, version "
                "numbers, configuration steps, and prerequisites. Penalize hallucinated "
                "features or incorrect procedures."
            ),
            evaluation_params=[
                "input",
                "actual_output",
                "expected_output",
            ],
            threshold=0.6,
        )
    return _correctness_metric


async def evaluate_response(
    question: TestQuestion, result: EngineResult
) -> EvalScore:
    """Score a single engine response against ground truth."""
    score = EvalScore(
        question_id=question.id,
        engine=result.engine,
        cites_ansys_help=result.cites_ansys_help,
        mentions_product=result.mentions_product,
    )

    if result.error or not result.response_text:
        score.errors.append(result.error or "Empty response")
        return score

    ground_truth = question.ground_truth_text
    if not ground_truth:
        score.errors.append("No ground truth content available")
        return score

    test_case = LLMTestCase(
        input=question.question,
        actual_output=result.response_text,
        expected_output=ground_truth,
        retrieval_context=[ground_truth],
    )

    # Answer Relevancy
    try:
        relevancy = AnswerRelevancyMetric(threshold=0.5)
        await relevancy.a_measure(test_case)
        score.answer_relevancy = relevancy.score
    except Exception as e:
        score.errors.append(f"Relevancy metric failed: {e}")

    # Faithfulness
    try:
        faithful = FaithfulnessMetric(threshold=0.5)
        await faithful.a_measure(test_case)
        score.faithfulness = faithful.score
    except Exception as e:
        score.errors.append(f"Faithfulness metric failed: {e}")

    # Correctness (GEval)
    try:
        metric = _get_correctness_metric()
        await metric.a_measure(test_case)
        score.correctness = metric.score
    except Exception as e:
        score.errors.append(f"Correctness metric failed: {e}")

    return score
