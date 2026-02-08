import json
import re
from typing import TypedDict

from constants import get_llm
from langgraph.graph import END, StateGraph
from prompts.classifier_prompt import CLASSIFIER_PROMPT


def parse_classifier_response(content: str) -> tuple[str, float, str]:
    """
    Parse LLM response to extract thought process and JSON result.
    Returns (result, confidence, thought_process).
    """
    thought_process = ""
    result = "OTHERS"
    conf = 0.5

    # Extract JSON from markdown code block (```json ... ```)
    json_match = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", content)
    if json_match:
        thought_process = content[: json_match.start()].strip()
        try:
            parsed = json.loads(json_match.group(1).strip())
            result = parsed.get("result", result)
            conf = float(parsed.get("conf", conf))
        except (json.JSONDecodeError, ValueError):
            pass
    else:
        # Fallback: try to find raw JSON in content
        brace_match = re.search(r"\{[^{}]*(?:\"result\"|\"conf\")[^{}]*\}", content)
        if brace_match:
            thought_process = content[: brace_match.start()].strip()
            try:
                parsed = json.loads(brace_match.group(0))
                result = parsed.get("result", result)
                conf = float(parsed.get("conf", conf))
            except (json.JSONDecodeError, ValueError):
                pass
        else:
            thought_process = content

    return result, conf, thought_process


# --- 1. Define the Shared State ---
# This dictionary acts as the "memory" passed between agents.
class AgentState(TypedDict):
    user_input: str
    classification: str
    confidence: float
    thought_process: str
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

    llm = get_llm()

    response = llm.invoke(CLASSIFIER_PROMPT.format(item=item))

    content = response.content if hasattr(response, "content") else str(response)
    result, conf, thought_process = parse_classifier_response(content)

    print(f"[Worker] Thought process: {thought_process}...")
    print(f"[Worker] Result found: {result} (conf: {conf})")
    return {
        "classification": result,
        "confidence": conf,
        "thought_process": thought_process,
    }


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
        "thought_process": "",
        "next_step": "",
    }
    result = app.invoke(inputs)
    print(f"Thought process: {result['thought_process']}")
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
