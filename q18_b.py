# The framework-level backstop: LangGraph raises GraphRecursionError when a graph exceeds its step limit.
# Requires: pip install "langgraph>=1.0". Set recursion_limit explicitly; the default differs by version.
from typing import TypedDict

from langgraph.errors import GraphRecursionError
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    attempts: int


def call_tool(state: State) -> dict:
    return {"attempts": state["attempts"] + 1}          # the tool "fails" every time


def should_continue(state: State) -> str:
    return "retry"                                       # bug: no success test, no attempt cap


g = StateGraph(State)
g.add_node("call_tool", call_tool)
g.add_edge(START, "call_tool")
g.add_conditional_edges("call_tool", should_continue, {"retry": "call_tool", "done": END})
app = g.compile()

try:
    app.invoke({"attempts": 0}, {"recursion_limit": 6})
except GraphRecursionError as e:
    print("stopped by framework:", type(e).__name__)


def should_continue_fixed(state: State) -> str:          # the real fix lives in your routing logic
    return "done" if state["attempts"] >= 3 else "retry"


g2 = StateGraph(State)
g2.add_node("call_tool", call_tool)
g2.add_edge(START, "call_tool")
g2.add_conditional_edges("call_tool", should_continue_fixed, {"retry": "call_tool", "done": END})
print("with explicit stop condition:", g2.compile().invoke({"attempts": 0}, {"recursion_limit": 6}))
