# Context-window budgeting: keep the system prompt and recent turns, summarise the rest.
WINDOW, RESERVE_OUTPUT = 8_000, 1_000

def tokens(text):                         # rough heuristic: ~4 characters per token in English
    return max(1, len(text) // 4)

system = "You are a support assistant for Acme Payments. " * 20
history = [f"Turn {i}: " + "customer and agent discussed refund details. " * 30 for i in range(1, 21)]
retrieved = ["Policy chunk: refunds over 500 need approval. " * 25 for _ in range(4)]

def build(system, history, retrieved):
    budget = WINDOW - RESERVE_OUTPUT - tokens(system) - sum(map(tokens, retrieved))
    kept, used = [], 0
    for turn in reversed(history):        # newest first
        if used + tokens(turn) > budget * 0.8:
            break
        kept.insert(0, turn)
        used += tokens(turn)
    dropped = history[: len(history) - len(kept)]
    summary = f"[Summary of {len(dropped)} earlier turns: refund discussion, no decision yet]" if dropped else ""
    parts = [system] + retrieved + ([summary] if summary else []) + kept
    return parts, len(dropped)

parts, dropped = build(system, history, retrieved)
total = sum(map(tokens, parts))
print(f"history turns: {len(history)}, kept verbatim: {len(history) - dropped}, summarised: {dropped}")
print(f"prompt tokens ~{total:,} + output reserve {RESERVE_OUTPUT:,} = {total + RESERVE_OUTPUT:,} of {WINDOW:,}")
