from typing import Dict, List, Union

from constants import get_llm
from langchain_core.tools import tool
from prompts.evaluate_prompt import EVALUATE_PROMPT
from pydantic import BaseModel, Field


class EvaluateSearchResultsDecision(BaseModel):
    evaluation: List[Dict[str, Union[str, float]]] = Field(
        description="""The list of evaluation results {\"search_result\": \"one possible result from the search agent\", 
        \"reasoning\": \"feedback on the reasoning for the search result and for the search item\", 
        \"confidence_score\": \"a score between 0.0 and 1.0 representing confidence. 1.0 = Certain.\"}"""
    )


@tool
def evaluate_search_results(
    input: str, search_results: str
) -> EvaluateSearchResultsDecision:
    """
    Evaluate the search results and give confidence score for each possible HS-Code.
    """
    llm = get_llm()
    structured_llm = llm.with_structured_output(EvaluateSearchResultsDecision)
    response = structured_llm.invoke(
        EVALUATE_PROMPT.format(input=input, search_results=search_results)
    )
    return response
