# A supervisor routes work to specialists and keeps a handoff log. Workers are plain functions here.
def researcher(task):  return f"facts about {task['topic']}: 3 sources found"
def coder(task):       return f"wrote analysis.py for {task['topic']}"
def reviewer(task):    return "approved" if "analysis.py" in task.get("artifact", "") else "rejected: no artifact"

WORKERS = {"research": researcher, "code": coder, "review": reviewer}

def supervisor(goal):
    plan = ["research", "code", "review"]          # an LLM would produce this; fixed here for clarity
    state, log = {"topic": goal}, []
    for step in plan:
        result = WORKERS[step](state)
        log.append((step, result))
        if step == "code":
            state["artifact"] = result
        if result.startswith("rejected"):
            log.append(("supervisor", "stop: review failed, hand to human"))
            break
    return log

for who, what in supervisor("Q3 card-decline rates"):
    print(f"{who:>10}: {what}")
