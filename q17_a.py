# ReAct vs Plan-and-Execute on the same task with mock tools. Count the "LLM calls" each needs.
TOOLS = {
    "fx_rate": lambda a: {"EURUSD": 1.08}[a],
    "invoice_total": lambda a: {"INV-1": 1200.0}[a],
}

def react(goal):
    calls, observations = 0, []
    # Each iteration = one model call deciding the next action from everything seen so far.
    script = [("invoice_total", "INV-1"), ("fx_rate", "EURUSD"), ("finish", None)]
    for action, arg in script:
        calls += 1
        if action == "finish":
            return round(observations[0] * observations[1], 2), calls
        observations.append(TOOLS[action](arg))

def plan_and_execute(goal):
    calls = 1                                       # one planning call produces the whole plan
    plan = [("invoice_total", "INV-1"), ("fx_rate", "EURUSD")]
    results = [TOOLS[t](a) for t, a in plan]        # executor runs steps without re-planning
    calls += 1                                      # one call to synthesise the answer
    return round(results[0] * results[1], 2), calls

goal = "What is invoice INV-1 (EUR) in USD?"
print("ReAct           ->", dict(zip(["answer", "llm_calls"], react(goal))))
print("Plan-and-Execute->", dict(zip(["answer", "llm_calls"], plan_and_execute(goal))))
