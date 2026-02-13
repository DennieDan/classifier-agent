import json
import sys
from pathlib import Path
from typing import Dict, List, Union

# Allow running this file directly (e.g. python tools/agent_tools.py): ensure app is on path
_here = Path(__file__).resolve().parent
_app = _here.parent
if str(_app) not in sys.path:
    sys.path.insert(0, str(_app))

from constants import get_local_ollama_llm
from graph import logger
from prompts.evaluate_prompt import EVALUATE_PROMPT
from prompts.identify_function import IDENTIFY_PRIMARY_FUNCTION_PROMPT
from pydantic import BaseModel, Field


class EvaluateSearchResultsDecision(BaseModel):
    evaluation: List[Dict[str, Union[str, float]]] = Field(
        description="""The list of evaluation results {\"search_result\": \"one possible result from the search agent\", 
        \"reasoning\": \"feedback on the reasoning for the search result and for the search item\", 
        \"confidence_score\": \"a score between 0.0 and 1.0 representing confidence. 1.0 = Certain.\"}"""
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
    llm = get_local_ollama_llm(model="llama3.1:8b-instruct-q8_0")
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
    llm = get_local_ollama_llm(model="llama3.1:8b-instruct-q8_0")
    response = llm.invoke(IDENTIFY_PRIMARY_FUNCTION_PROMPT.format(item=item))
    logger.info(f"--- [Identify Primary Function] Response: {response} ---")
    return response
