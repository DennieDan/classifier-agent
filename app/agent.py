import asyncio
import os
import sys
import uuid
from typing import Annotated

from constants import get_cloud_groq_llm, get_cloud_openai_gpt_4o, get_local_ollama_llm
from langchain_core.messages.tool import tool_call
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig, RunnableLambda
from langgraph.graph.message import BaseMessage, add_messages
from langgraph.graph.state import END, START, StateGraph
from prompts.supervisor_prompt_tools import SUPERVISOR_PROMPT
from tools.agent_tools import (
    evaluate_search_results,
    get_best_confidence_score_and_compare_with_threshold,
    identify_primary_function,
)
from tools.regulatory_server import get_regulatory_rules, search_stcced_pdf
from typing_extensions import TypedDict

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import ToolNode

load_dotenv()
load_dotenv(os.path.join(_SCRIPT_DIR, ".env"))

# llm = ChatOllama(model="llama3-groq-tool-use", temperature=0)


class ReactGraph:
    def __init__(
        self, model: str = "llama-3.3-70b-versatile-q8_0", host: str = "cloud groq"
    ):
        if host == "cloud groq":
            self.llm = get_cloud_groq_llm(model=model)
        elif host == "local":
            self.llm = get_local_ollama_llm(model=model)
        elif host == "cloud openai":
            self.llm = get_cloud_openai_gpt_4o(model=model)
        else:
            raise ValueError(f"Invalid host: {host}")
        self.supervisor_runnable = primary_supervisor_prompt | self.llm.bind_tools(
            tools
        )
        self.builder = StateGraph(State)
        self.builder.add_node("supervisor", Supervisor(self.supervisor_runnable))
        self.builder.add_node("tool", create_tool_node_with_fallback(tools))

        self.builder.add_edge(START, "supervisor")
        self.builder.add_conditional_edges("supervisor", tools_condition)
        self.builder.add_edge("tool", "supervisor")
        self.graph = self.builder.compile()

    def run(self, user_input: str):
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        state = self.graph.invoke({"messages": ("user", user_input)}, config=config)
        return {"response": state["messages"][-1].content, "messages": state}


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    error: Exception


class Supervisor:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        """
        Call method to invoke LLM and handle its responses.
        Re-prompt the assistant if the response is not a tool call or meaningful text.


        Args:
            state: The current state of the assistant containing the messages and error.
            config: The configuration for the runnable.

        Returns:
            The updated state of the assistant.
        """
        # Ensure the LLM sees the FULL history from the state
        # ChatPromptTemplate expects a mapping (dict); the template has placeholder "{messages}"
        while True:
            result = self.runnable.invoke(state)
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}


tools = [
    evaluate_search_results,
    get_best_confidence_score_and_compare_with_threshold,
    identify_primary_function,
    get_regulatory_rules,
    search_stcced_pdf,
]


def get_agent_tool_names() -> list[str]:
    """Return the names of tools the agent has access to (for debugging)."""
    names = []
    for t in tools:
        name = getattr(t, "name", None) or getattr(t, "__name__", "unknown")
        names.append(name)
    return names


def _tool_display(t):
    """Support both LangChain tools (.name, .description) and plain callables (__name__, __doc__)."""
    name = getattr(t, "name", None) or getattr(t, "__name__", "unknown")
    desc = (
        getattr(t, "description", None)
        or getattr(t, "__doc__", "")
        or "(No description)"
    )
    return f"- **{name}**: {(desc or "(No description)").strip().split(chr(10))[0]}"


tools_context = "\n".join(_tool_display(t) for t in tools)
primary_supervisor_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            SUPERVISOR_PROMPT.format(available_tools=tools_context),
        ),
        ("placeholder", "{messages}"),
    ]
)
# primary_supervisor_prompt = ChatPromptTemplate.from_messages(
#     [
#         SystemMessage(content=SUPERVISOR_PROMPT.format(available_tools=tools_context)),
#         ("placeholder", "{messages}"),
#     ]
# )

llm = get_cloud_groq_llm(model="llama-3.3-70b-versatile-q8_0")
supervisor_runnable = primary_supervisor_prompt | llm.bind_tools(tools)


def handle_tool_error(state: State) -> dict:
    error = state["error"]
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(content=str(error), tool_call_id=tc["id"]) for tc in tool_calls
        ]
    }


def create_tool_node_with_fallback(tools: list) -> dict:
    return ToolNode(tools=tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )


def tools_condition(state: State) -> str:
    if state["messages"][-1].tool_calls:
        return "tool"
    elif (
        state["messages"][-1].content
        and "Final Answer:" in state["messages"][-1].content
    ):
        return END
    else:
        return "supervisor"


# Graph
builder = StateGraph(State)

builder.add_node("supervisor", Supervisor(supervisor_runnable))
builder.add_node("tool", create_tool_node_with_fallback(tools))

builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", tools_condition)
builder.add_edge("tool", "supervisor")

# the Checkpointer let the graph persist the state across restarts
# memory = SqliteSaver.from_conn_string(":memory:")


react_graph = builder.compile()


def run_graph(user_input: str):
    """
    Run the graph with the user input.
    """
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    state = react_graph.invoke({"messages": ("user", user_input)}, config=config)
    return {"response": state["messages"][-1].content, "messages": state}
