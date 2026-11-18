# What a reducer actually does, without any framework: merge partial updates into shared state.
def merge(state, update, reducers):
    new = dict(state)
    for key, value in update.items():
        new[key] = reducers[key](state.get(key), value) if key in reducers else value
    return new

reducers = {"messages": lambda old, new: (old or []) + new}
state = {"messages": [], "status": "open"}

# Two nodes ran in the same step and both returned updates:
for update in [{"messages": ["agent A: checked ledger"]},
               {"messages": ["agent B: checked vendor"], "status": "investigating"}]:
    state = merge(state, update, reducers)
print(state)
print("Without the append reducer, one agent's message would silently overwrite the other's.")
