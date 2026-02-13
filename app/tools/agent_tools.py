import json
import sys
from pathlib import Path
from typing import List

# Allow running this file directly (e.g. python tools/agent_tools.py): ensure app is on path
_here = Path(__file__).resolve().parent
_app = _here.parent
if str(_app) not in sys.path:
    sys.path.insert(0, str(_app))

from constants import get_cloud_groq_llm
from graph import logger
from prompts.evaluate_prompt import EVALUATE_PROMPT
from prompts.identify_function import IDENTIFY_PRIMARY_FUNCTION_PROMPT
from pydantic import BaseModel, Field


class EvaluationItem(BaseModel):
    """A single evaluation result. confidence_score must be a number, not an expression."""

    search_result: str = Field(description="One possible result from the search agent")
    reasoning: str = Field(description="Feedback on the reasoning for the search result")
    confidence_score: float = Field(
        ge=0.0,
        le=1.0,
        description="A single number between 0.0 and 1.0 (e.g. 0.9 or 1.0). Must be a number only, never a formula.",
    )


class EvaluateSearchResultsDecision(BaseModel):
    evaluation: List[EvaluationItem] = Field(
        description="The list of evaluation results, each with search_result, reasoning, and confidence_score (a number 0.0-1.0)."
    )


def evaluate_search_results(
    input: str, primary_function: str, search_results: str
) -> str:
    """
    Evaluate the search results and give confidence score for each possible HS-Code.
    Args:
        input: the user input
        primary_function: the primary function of the item
        search_results: the search results
    Returns:
        The evaluation results with confidence score for each possible HS-Code
    """
    logger.info(
        f"--- [Evaluate Search Results] Input: {input}, Primary Function: {primary_function} ---"
    )
    llm = get_cloud_groq_llm(model="llama-3.3-70b-versatile")
    structured_llm = llm.with_structured_output(EvaluateSearchResultsDecision)
    response = structured_llm.invoke(
        EVALUATE_PROMPT.format(
            input=input,
            primary_function=primary_function,
            search_results=search_results,
        )
    )
    logger.info(f"--- [Evaluate Search Results] Response: {response} ---")
    return response


def get_best_confidence_score_and_compare_with_threshold(
    confidence_score: List[float] | str,
) -> bool:
    """
    Get the best confidence score from a list of confidence scores and compare it with the threshold.
    Args:
        confidence_score: an array of confidence scores (or a JSON array string, e.g. "[0.9, 0.4, 0.3]")
    Returns:
        True if the best confidence score is greater than 0.9, False otherwise
    """
    if isinstance(confidence_score, str):
        confidence_score = json.loads(confidence_score)
    return max(confidence_score) > 0.9


def identify_primary_function(item: str) -> str:
    """
    Identify the primary function of the item.
    Args:
        item: the item
    Returns:
        The primary function of the item
    """
    logger.info(f"--- [Identify Primary Function] Item: {item} ---")
    llm = get_cloud_groq_llm(model="llama-3.3-70b-versatile")
    response = llm.invoke(IDENTIFY_PRIMARY_FUNCTION_PROMPT.format(item=item))
    logger.info(f"--- [Identify Primary Function] Response: {response} ---")
    return response
