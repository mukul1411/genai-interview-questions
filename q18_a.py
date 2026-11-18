# A loop guard that stops agents for four distinct reasons.
class LoopGuard:
    def __init__(self, max_steps=8, max_cost=0.50, repeat_window=3, stall_window=3):
        self.max_steps, self.max_cost = max_steps, max_cost
        self.repeat_window, self.stall_window = repeat_window, stall_window
        self.history, self.cost, self.facts_seen = [], 0.0, []

    def check(self, action, cost, new_facts):
        self.history.append(action); self.cost += cost; self.facts_seen.append(new_facts)
        if len(self.history) >= self.max_steps:
            return "stop: step budget"
        if self.cost >= self.max_cost:
            return "stop: cost budget"
        recent = self.history[-self.repeat_window:]
        if len(recent) == self.repeat_window and len(set(recent)) == 1:
            return "stop: repeated identical action"
        tail = self.facts_seen[-self.stall_window:]
        if len(tail) == self.stall_window and sum(tail) == 0:
            return "stop: no new information"
        return "continue"

g = LoopGuard()
trace = [("search('refund policy')", 0.02, 3), ("search('refund policy v2')", 0.02, 1),
         ("lookup('INV-9')", 0.01, 0), ("lookup('INV-9')", 0.01, 0), ("lookup('INV-9')", 0.01, 0)]
for step, (action, cost, facts) in enumerate(trace, 1):
    verdict = g.check(action, cost, facts)
    print(f"step {step}: {action:<28} -> {verdict}")
    if verdict != "continue":
        break
