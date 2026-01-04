from langgraph.graph import StateGraph, END
from typing import TypedDict
from .testcase_generator import generate_test_cases
from .testcase_validator import validate_test_cases

class State(TypedDict):
    metadata: dict
    test_cases: list
    valid_test_cases: list

def generate_node(state: State) -> State:
    state['test_cases'] = generate_test_cases(state['metadata'], num_cases=10)
    return state

def validate_node(state: State) -> State:
    state['valid_test_cases'] = validate_test_cases(state['test_cases'], state['metadata'])
    return state

def build_workflow():
    workflow = StateGraph(State)
    workflow.add_node("generate", generate_node)
    workflow.add_node("validate", validate_node)

    workflow.set_entry_point("generate")
    workflow.add_edge("generate", "validate")
    workflow.add_edge("validate", END)

    return workflow.compile()