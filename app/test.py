import asyncio
import json

from agent import run_graph
from graph import AgentGraph
from index_query import IndexQuery
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from pareto.agent_providers import cloud_groq_llama_3_3_70b_versatile
from tools.agent_tools import identify_primary_function

user_input_1 = "What is the HS-Code of Virgin Olive Oil?"
user_input_2 = "The user input mentions 'solar-powered', 'IoT sensors', and 'agricultural moisture tracking'. This suggests the item is a type of monitoring device. However, without further information or search results to evaluate, it's unclear which specific HS-Code applies. Check Chapter 85 Notes regarding 'monitors' vs 'static converters' to find the correct HS-Code."
search_results_1 = """
The possible HS-Codes for virgin olive oil are:

1. 1509.30.00 - This code corresponds to "Virgin olive oil", which is a specific category of olive oil.

2. Other subcodes under 15.09 and other categories may also include virgin olive oil, but the most direct match would be 1509.30.00.

3. Although not explicitly stated in the given information, it's possible that some HS-Codes for blends or fractions might also encompass virgin olive oil; however, they are not listed here as they're less specific.
"""
user_input_charging_station = "What is the HS-Code of Electric vehicle charging station with integrated advertising LED display?"
user_input_solar_powered_iot_sensors = "What is the HS-Code of Modular solar-powered IoT sensors for agricultural moisture tracking?"
user_input_polymer = (
    "What is the HS-Code of High-grade industrial polymers for medical 3D printing?"
)

# ollama_llm = ChatOllama(
#     model="llama3.1:8b-instruct-q8_0",
#     temperature=0,
#     request_timeout=600,
# )
# graph = AgentGraph(ollama_llm)

# initial_state = {
#     "messages": [HumanMessage(content=user_input)],
#     "rules": "",  # Start empty; Supervisor will fetch via MCP
#     "search_results": "",  # Start empty
#     "previous_search_results": "",
#     "instructions": "",
#     "confidence": 0.0,
#     "next_action": "supervisor",  # Start with Supervisor
# }

if __name__ == "__main__":

    # try:

    #     async def run_audit():
    #         # We stream the output to see steps happening in real-time
    #         async for event in graph.app.astream(initial_state):
    #             for node_name, node_state in event.items():
    #                 print(f"\n--- Finished Node: {node_name} ---")
    #                 if "supervisor_reasoning" in node_state:
    #                     print(
    #                         f"Supervisor Reasoning: {node_state.get('supervisor_reasoning')}"
    #                     )
    #                 if "final_answer" in node_state:
    #                     print(f"\n=== FINAL AUDIT DECISION ===")
    #                     print(f"Final Answer: {node_state['final_answer']}")
    #                     print(f"Confidence: {node_state['confidence'] * 100:.1f}%")

    #     asyncio.run(run_audit())

    # except KeyboardInterrupt:
    #     print("Audit stopped by user.")
    # except Exception as e:
    #     print(f"Error occurred: {e}")

    # result = evaluate_search_results.invoke(
    #     {
    #         "input": user_input_1,
    #         "search_results": search_results_1,
    #     }
    # )
    # print(json.dumps(result.evaluation, indent=4))

    # index_query = IndexQuery()
    # retrieval_result = index_query.index_query(query=user_input_2)
    # print(retrieval_result)

    # result = run_graph(user_input_polymer)
    # print(result)

    # async def main():
    #     result = await run_agent(user_input_1)
    #     print(json.dumps(result, indent=4))

    # asyncio.run(main())

    result = cloud_groq_llama_3_3_70b_versatile(user_input_1)
    print(result)
