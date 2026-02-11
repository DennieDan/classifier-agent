import json

from graph import AgentGraph
from langchain_core.messages import HumanMessage
from tools.agent_tools import evaluate_search_results

user_input_1 = "What is the HS-Code of Virgin Olive Oil?"
search_results_1 = """
The possible HS-Codes for virgin olive oil are:

1. 1509.30.00 - This code corresponds to "Virgin olive oil", which is a specific category of olive oil.

2. Other subcodes under 15.09 and other categories may also include virgin olive oil, but the most direct match would be 1509.30.00.

3. Although not explicitly stated in the given information, it's possible that some HS-Codes for blends or fractions might also encompass virgin olive oil; however, they are not listed here as they're less specific.
"""
user_input = "What is the HS-Code of Pasta?"
graph = AgentGraph()
result = graph.app.invoke(
    {
        "messages": [HumanMessage(content=user_input)],
    }
)
# result_json = json.dumps(result.final_answer, indent=4)
print("--------------------------------")
for key, value in result.items():
    print(f"{key}: {value}")
print("--------------------------------")

# result = evaluate_search_results.invoke(
#     {
#         "input": user_input_1,
#         "search_results": search_results_1,
#     }
# )
# print(json.dumps(result.evaluation, indent=4))
