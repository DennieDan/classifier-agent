"""
Fallback for LLMs that don't support with_structured_output (e.g. Ollama).
Invokes the LLM with a JSON instruction and parses the response into a Pydantic model.
"""

import json
import re
from typing import List, Union

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from pydantic import BaseModel


def _extract_json(text: str) -> str:
    """Extract JSON from response, handling markdown code blocks."""
    text = text.strip()
    # Try ```json ... ``` or ``` ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        return match.group(1).strip()
    return text


def invoke_structured(
    llm: BaseChatModel,
    model_class: type[BaseModel],
    messages: Union[List[BaseMessage], str],
) -> BaseModel:
    """
    Get structured output from an LLM that may not support with_structured_output
    (e.g. ChatOllama). Adds a JSON instruction and parses the response.

    :param llm: The chat model (e.g. ChatOllama, ChatGroq).
    :param model_class: Pydantic model class for the expected output.
    :param messages: Either a list of BaseMessage or a single string (turned into HumanMessage).
    :return: An instance of model_class.
    """
    schema = model_class.model_json_schema()
    json_instruction = (
        "\n\nRespond with a single valid JSON object only (no markdown, no explanation) "
        f"that matches this schema: {json.dumps(schema)}"
    )

    if isinstance(messages, str):
        messages = [HumanMessage(content=messages + json_instruction)]
    else:
        messages = list(messages)
        last = messages[-1]
        if isinstance(last, (HumanMessage, SystemMessage)):
            messages[-1] = type(last)(content=last.content + json_instruction)
        else:
            messages.append(HumanMessage(content=json_instruction))

    response = llm.invoke(messages)
    content = getattr(response, "content", str(response))
    json_str = _extract_json(content)
    data = json.loads(json_str)
    return model_class.model_validate(data)
