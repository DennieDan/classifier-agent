import sys
from pathlib import Path

from langchain_core.language_models import BaseChatModel

# Allow imports when run by promptfoo from repo root (config next to app/)
_here = Path(__file__).resolve().parent
_app = _here.parent
if str(_app) not in sys.path:
    sys.path.insert(0, str(_app))

from constants import get_cloud_groq_llm
from graph import AgentGraph
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama


def _run_and_return_output(
    prompt: str, options: dict, context: dict, *, llm: BaseChatModel
):
    graph = AgentGraph(llm)
    result = graph.app.invoke(
        {
            "messages": [HumanMessage(content=prompt)],
        }
    )
    # LangGraph returns the final state as a dict; use dict access, not getattr
    out = result.get("search_results") or ""
    if not isinstance(out, str):
        out = str(out)
    return {"output": out}


def local_llama_3_1_8b_instruct_q8_0(prompt: str, options: dict, context: dict):
    # Use LangChain ChatOllama so the graph can call llm.invoke() (LlamaIndex Ollama has no .invoke)
    llm = ChatOllama(
        model="llama3.1:8b-instruct-q8_0",
        temperature=0,
        request_timeout=600,
    )
    return _run_and_return_output(prompt, options, context, llm=llm)


def cloud_groq_llama_3_3_70b_versatile(prompt: str, options: dict, context: dict):
    llm = get_cloud_groq_llm(model="llama-3.3-70b-versatile-q8_0")
    return _run_and_return_output(prompt, options, context, llm=llm)
