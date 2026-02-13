from constants import get_local_ollama_llm
from langchain.agents import create_react_agent

# from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from prompts.supervisor_prompt_tools import SUPERVISOR_PROMPT
from tools.agent_tools import (
    evaluate_search_results,
    get_best_confidence_score_and_compare_with_threshold,
    identify_primary_function,
)
from tools.regulatory_server import get_regulatory_rules, search_stcced_pdf


async def setup_agent():
    """Initialize the agent with MCP tools"""
    global agent, client

    try:
        print("Getting tools from MCP client...")
        tools = [
            identify_primary_function,
            search_stcced_pdf,
            evaluate_search_results,
            get_regulatory_rules,
            get_best_confidence_score_and_compare_with_threshold,
        ]
        print(f"Found {len(tools)} tools")

        print("Creating LLM...")
        llm = get_local_ollama_llm(model="llama3.1:8b-instruct-q8_0")

        print("Creating agent...")
        prompt = PromptTemplate.from_template(SUPERVISOR_PROMPT)
        agent = create_react_agent(llm, tools, prompt=prompt)
        print("Agent created successfully")
        return agent
    except Exception as e:
        print(f"Error setting up agent: {e}")
        print(f"Error type: {type(e).__name__}")
        return None


async def run_agent(input: str):
    agent = await setup_agent()
    result = await agent.ainvoke({"input": input})
    return result
