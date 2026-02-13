import os
from typing import List

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_ollama import ChatOllama

load_dotenv()


def validate_user(user_id: int, addresses: List) -> bool:
    """
    Validate the user by checking if the user ID is valid and the addresses are valid.

    Args:
        user_id: The user ID to validate.
        addresses: The addresses to validate.

    Returns:
        True if the user is valid, False otherwise.
    """
    return True


llm = ChatOllama(model="llama3-groq-tool-use", temperature=0).bind_tools(
    [validate_user]
)

messages = [
    HumanMessage(
        content="Could you validate the user with ID 123 and addresses ['123 Main St', '456 Elm St']? Give me answer whether they are valid or not."
    )
]

# Turn 1: LLM often returns empty content + tool_calls when it wants to use a tool
# response = llm.invoke(messages)
# print(
#     "Turn 1 (after first invoke):",
#     repr(response.content),
#     "tool_calls:",
#     response.tool_calls,
# )

# # If the model requested tool calls, run them and call the LLM again with the results
# if response.tool_calls:
#     # Build the next message list: previous messages + AI message with tool_calls + tool results
#     messages = messages + [response]
#     for tc in response.tool_calls:
#         result = validate_user(**tc["args"])
#         messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))
#     # Turn 2: LLM gets tool results and produces the final answer in content
#     response = llm.invoke(messages)
#     print("Turn 2 (after tool results):", repr(response.content))
# else:
#     print("No tool calls; content:", response.content)
