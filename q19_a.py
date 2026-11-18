# Shared state in LangGraph: a typed state, per-key reducers, parallel branches, and a checkpointer.
# Requires: pip install "langgraph>=1.0"   (verified here with langgraph 1.2)
import operator
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    question: str
    findings: Annotated[list[str], operator.add]   # reducer: parallel writes are APPENDED
    answer: str                                    # no reducer: last write wins


def search_policy(state: State) -> dict:
    return {"findings": ["policy: refunds > 500 USD need approval"]}


def search_history(state: State) -> dict:
    return {"findings": ["history: customer had 2 refunds this year"]}


def synthesise(state: State) -> dict:
    return {"answer": f"{len(state['findings'])} findings -> route to manager for approval"}


g = StateGraph(State)
g.add_node("search_policy", search_policy)
g.add_node("search_history", search_history)
g.add_node("synthesise", synthesise)
g.add_edge(START, "search_policy")                 # two edges from START = parallel fan-out
g.add_edge(START, "search_history")
g.add_edge(["search_policy", "search_history"], "synthesise")   # join waits for both
g.add_edge("synthesise", END)
app = g.compile(checkpointer=InMemorySaver())

config = {"configurable": {"thread_id": "case-42"}}
result = app.invoke({"question": "Refund 800 USD?", "findings": []}, config)
print("findings:", sorted(result["findings"]))
print("answer  :", result["answer"])
print("checkpoint persisted for thread case-42:", app.get_state(config).values["answer"] == result["answer"])
