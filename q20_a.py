# Memory for agents: a short-term rolling buffer with summarisation, plus a gated long-term store.
from collections import deque

class ShortTermMemory:
    def __init__(self, max_turns=4):
        self.turns, self.summary = deque(), ""
        self.max_turns = max_turns

    def add(self, turn):
        self.turns.append(turn)
        if len(self.turns) > self.max_turns:
            old = self.turns.popleft()
            self.summary = (self.summary + " | " if self.summary else "") + old[:40]   # an LLM would summarise

    def context(self):
        return ([f"[earlier: {self.summary}]"] if self.summary else []) + list(self.turns)

class LongTermMemory:
    """Only facts confirmed by the user or a reviewer are written; each keeps its provenance."""
    def __init__(self):
        self.facts = {}

    def write(self, key, value, source, confirmed):
        if not confirmed:
            return False
        self.facts[key] = {"value": value, "source": source}
        return True

    def recall(self, keyword):
        return {k: v for k, v in self.facts.items() if keyword in k}

stm, ltm = ShortTermMemory(), LongTermMemory()
for i in range(1, 7):
    stm.add(f"turn {i}: user discussed invoice {100 + i} and its due date")
print("short-term context:", *stm.context(), sep="\n  ")
print("write unconfirmed  :", ltm.write("vendor:V-22:currency", "EUR", "turn 3", confirmed=False))
print("write confirmed    :", ltm.write("vendor:V-22:currency", "EUR", "reviewer alice", confirmed=True))
print("recall vendor:V-22 :", ltm.recall("vendor:V-22"))
