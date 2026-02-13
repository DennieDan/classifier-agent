import sys
from pathlib import Path

from langchain_core.language_models import BaseChatModel

# Allow imports when run by promptfoo from repo root (config next to app/)
_here = Path(__file__).resolve().parent
_app = _here.parent
if str(_app) not in sys.path:
    sys.path.insert(0, str(_app))

from agent import ReactGraph
from constants import get_cloud_groq_llm
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama


def _run_and_return_output(
    prompt: str,
    options: dict,
    context: dict,
    *,
    model: str = "llama-3.3-70b-versatile",
    host: str
):
    agent = ReactGraph(model=model, host=host)
    result = agent.run(prompt)
    return {"output": result["response"]}


def local_llama_3_1_8b_instruct_q8_0(prompt: str, options: dict, context: dict):
    return _run_and_return_output(
        prompt, options, context, model="llama3.1:8b-instruct-q8_0", host="local"
    )


def cloud_groq_llama_3_3_70b_versatile(
    prompt: str, options: dict = {}, context: dict = {}
):
    return _run_and_return_output(
        prompt,
        options,
        context,
        model="llama-3.3-70b-versatile",
        host="cloud groq",
    )


def cloud_openai_gpt_4o(prompt: str, options: dict = {}, context: dict = {}):
    return _run_and_return_output(
        prompt,
        options,
        context,
        model="gpt-4o",
        host="cloud openai",
    )


def local_mistral_7b_instruct(prompt: str, options: dict = {}, context: dict = {}):
    return _run_and_return_output(
        prompt,
        options,
        context,
        model="mistral:7b",
        host="local",
    )


def local_llama_3_groq_tool_use(prompt: str, options: dict = {}, context: dict = {}):
    return _run_and_return_output(
        prompt,
        options,
        context,
        model="llama3-groq-tool-use",
        host="local",
    )
