import sys
from pathlib import Path
from typing import List

# Allow running this file directly (e.g. python tools/agent_tools.py): ensure app is on path
_here = Path(__file__).resolve().parent
_app = _here.parent
if str(_app) not in sys.path:
    sys.path.insert(0, str(_app))

from constants import get_local_ollama_llm
from fastmcp import FastMCP
from graph import logger
from langchain_core.tools import tool
from prompts.evaluate_prompt import EVALUATE_PROMPT
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


mcp = FastMCP("Agent Tools")


@mcp.tool()
def evaluate_search_results(
    input: str, previous_feedback: str, search_results: str
) -> EvaluateSearchResultsDecision:
    """
    Evaluate the search results and give confidence score for each possible HS-Code.
    input: the user input
    previous_feedback: the previous feedback from the supervisor
    search_results: the search results
    return: the evaluation results with confidence score for each possible HS-Code
    """
    logger.info(f"--- [Evaluate Search Results] Input: {input} ---")
    llm = get_local_ollama_llm(model="llama3.1:8b-instruct-q8_0")
    structured_llm = llm.with_structured_output(EvaluateSearchResultsDecision)
    response = structured_llm.invoke(
        EVALUATE_PROMPT.format(
            input=input,
            previous_feedback=previous_feedback,
            search_results=search_results,
        )
    )
    logger.info(f"--- [Evaluate Search Results] Response: {response} ---")
    return response


@mcp.tool()
def get_best_confidence_score_and_compare_with_threshold(
    confidence_score: List[float],
) -> bool:
    """
    Get the best confidence score and compare it with the threshold.
    """
    best_confidence_score = max(confidence_score)
    return best_confidence_score > 0.9


if __name__ == "__main__":
    mcp.run()
