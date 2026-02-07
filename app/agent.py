from typing import TypedDict

from langgraph.graph import END, StateGraph


# --- 1. Define the Shared State ---
# This dictionary acts as the "memory" passed between agents.
class AgentState(TypedDict):
    user_input: str
    classification: str
    confidence: float
    next_step: str  # Used by Supervisor to route


# --- 2. Define the Agents (Nodes) ---


def supervisor_agent(state: AgentState):
    """
    The Supervisor: Analyzes the input and decides which worker to call.
    In a complex system, this would use an LLM to choose between multiple workers.
    """
    print(f"\n[Supervisor] Analyzing request: '{state['user_input']}'")

    # Simple Logic: If it looks like a classification task, send to Classifier.
    # In a real system, this is where the LLM decides routing.
    if state["user_input"]:
        return {"next_step": "classifier_worker"}
    else:
        return {"next_step": "error"}


def classifier_worker(state: AgentState):
    """
    The Worker: Performs the specific task (Classification).
    """
    print(f"[Worker] Classifying item...")

    item = state["user_input"].lower()

    # Mocking the AI Logic (Replace this with an LLM call)
    foods = ["apple", "burger", "rice", "bread"]
    drinks = ["water", "coke", "juice", "milk"]

    if any(f in item for f in foods):
        result = "FOOD"
        conf = 0.95
    elif any(d in item for d in drinks):
        result = "DRINK"
        conf = 0.98
    else:
        result = "UNKNOWN"
        conf = 0.0

    print(f"[Worker] Result found: {result}")
    return {"classification": result, "confidence": conf}


# --- 3. Build the Graph (Workflow) ---

# Initialize the Graph
workflow = StateGraph(AgentState)

# Add Nodes (The Agents)
workflow.add_node("supervisor", supervisor_agent)
workflow.add_node("classifier_worker", classifier_worker)

# Set Entry Point
workflow.set_entry_point("supervisor")

# Add Conditional Edges (The Routing Logic)
# The Supervisor output ("next_step") determines where we go next.
workflow.add_conditional_edges(
    "supervisor",
    lambda x: x["next_step"],
    {"classifier_worker": "classifier_worker", "error": END},
)

# Add Edge from Worker back to END (Task Complete)
workflow.add_edge("classifier_worker", END)

# Compile the app
app = workflow.compile()

# --- 4. Run the System ---

if __name__ == "__main__":
    # Test Case 1
    inputs = {
        "user_input": "I want a glass of water",
        "classification": "",
        "confidence": 0.0,
        "next_step": "",
    }
    result = app.invoke(inputs)
    print(
        f"Final Output: {result['classification']} (Confidence: {result['confidence']})"
    )

    # Test Case 2
    inputs = {
        "user_input": "Give me an apple",
        "classification": "",
        "confidence": 0.0,
        "next_step": "",
    }
    result = app.invoke(inputs)
    print(
        f"Final Output: {result['classification']} (Confidence: {result['confidence']})"
    )
