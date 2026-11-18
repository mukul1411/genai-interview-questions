# What frameworks abstract: the same tool-using loop written with no framework at all.
# Reading this makes it clear what LangChain (components), LlamaIndex (data/indexing) and
# LangGraph (stateful graphs, checkpoints, interrupts) each take off your hands.
TOOLS = {"lookup_invoice": lambda inv: {"INV-7": {"amount": 950, "status": "unpaid"}}[inv]}

def model(messages):                     # stand-in for a chat model call with tool use
    last = messages[-1]
    if last["role"] == "user":
        return {"tool": "lookup_invoice", "args": {"inv": "INV-7"}}
    return {"answer": f"INV-7 is {last['content']['status']} for {last['content']['amount']} USD"}

def run(question, max_steps=5):
    messages = [{"role": "user", "content": question}]              # memory      (framework: message history)
    for _ in range(max_steps):                                      # loop guard  (framework: recursion limit)
        out = model(messages)                                       # model call  (framework: chat model wrapper)
        if "answer" in out:
            return out["answer"], messages
        result = TOOLS[out["tool"]](**out["args"])                  # tool exec   (framework: tool node)
        messages.append({"role": "tool", "content": result})        # state       (framework: reducer/checkpoint)
    return "stopped: step limit", messages

answer, msgs = run("Is invoice INV-7 paid?")
print(answer, f"({len(msgs)} messages)")
