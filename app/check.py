from agent import get_agent_tool_names

print(get_agent_tool_names())
# Should include 'evaluate_search_results'
print("evaluate_search_results" in get_agent_tool_names())  # True
