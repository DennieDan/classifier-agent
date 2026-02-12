import json

from graph import AgentGraph
from index_query import IndexQuery
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

user_input_1 = "What is the HS-Code of Virgin Olive Oil?"
user_input_2 = "The user input mentions 'solar-powered', 'IoT sensors', and 'agricultural moisture tracking'. This suggests the item is a type of monitoring device. However, without further information or search results to evaluate, it's unclear which specific HS-Code applies. Check Chapter 85 Notes regarding 'monitors' vs 'static converters' to find the correct HS-Code."
search_results_1 = """
The possible HS-Codes for virgin olive oil are:

1. 1509.30.00 - This code corresponds to "Virgin olive oil", which is a specific category of olive oil.

2. Other subcodes under 15.09 and other categories may also include virgin olive oil, but the most direct match would be 1509.30.00.

3. Although not explicitly stated in the given information, it's possible that some HS-Codes for blends or fractions might also encompass virgin olive oil; however, they are not listed here as they're less specific.
"""
# user_input = "What is the HS-Code of Electric vehicle charging station with integrated advertising LED display?"
user_input = "What is the HS-Code of Modular solar-powered IoT sensors for agricultural moisture tracking?"

ollama_llm = ChatOllama(
    model="llama3.1:8b-instruct-q8_0",
    temperature=0,
    request_timeout=600,
)
graph = AgentGraph(ollama_llm)
result = graph.app.invoke(
    {
        "messages": [HumanMessage(content=user_input)],
    }
)

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

# index_query = IndexQuery()
# retrieval_result = index_query.index_query(query=user_input_2)
# print(retrieval_result)
