from langgraph.graph import StateGraph, END
from typing import TypedDict
import requests
from .testcase_generator import generate_test_cases
from .testcase_validator import validate_test_cases
from .models import TestCase

class State(TypedDict):
    metadata: dict
    test_cases: list
    valid_test_cases: list
    final_test_cases: list

def generate_node(state: State) -> State:
    """Generate test case inputs."""
    state['test_cases'] = generate_test_cases(state['metadata'])
    return state

def validate_node(state: State) -> State:
    """Validate generated test case inputs."""
    state['valid_test_cases'] = validate_test_cases(state['test_cases'], state['metadata'])
    return state


def process_node(state: State) -> State:
    """Send valid test cases to the external API and collect clean input-output pairs."""
    api_url = "https://code-runner-lhdb.onrender.com/run-custom-tests"
    headers = {"Content-Type": "application/json"}

    payload = {
        "code": state['metadata']['code'],
        "language": state['metadata']['language'],
        "timeLimit": state['metadata']['timeLimit'],
        "memoryLimit": state['metadata']['memoryLimit'],
        "testcases": state['valid_test_cases']
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        api_response = response.json()

        results = api_response.get("results", [])
        clean_cases = []

        for case in results:
            inp = case.get("input", "").strip()
            out = case.get("output", "").strip()

            # Skip Markdown/formatting junk
            if inp in ["```json", "```", "[", "]"] or not inp:
                continue

            # Remove surrounding quotes and commas like '"6 6 4",'
            inp = inp.strip('",')

            clean_cases.append({"input": inp, "output": out})

        # Save final cleaned test cases
        state["final_test_cases"] = clean_cases

    except Exception as e:
        print(f"Error processing test cases: {e}")
        state["final_test_cases"] = []

    return state


def build_workflow():
    """Build the LangGraph workflow."""
    workflow = StateGraph(State)
    workflow.add_node("generate", generate_node)
    workflow.add_node("validate", validate_node)
    workflow.add_node("process", process_node)

    workflow.set_entry_point("generate")
    workflow.add_edge("generate", "validate")
    workflow.add_edge("validate", "process")
    workflow.add_edge("process", END)

    return workflow.compile()