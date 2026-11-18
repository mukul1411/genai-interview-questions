# Base vs instruction-tuned: the same intent needs a different prompt shape.
question = "What is the capital of France?"

# A base model only continues text, so you frame the task as a document to complete.
base_prompt = (
    "Q: What is the capital of Japan?\nA: Tokyo\n\n"
    "Q: What is the capital of Kenya?\nA: Nairobi\n\n"
    f"Q: {question}\nA:"
)

# An instruction-tuned model was trained on role-tagged conversations.
# Each vendor has its own template; this ChatML-style layout is illustrative.
def chat_template(messages):
    out = []
    for m in messages:
        out.append(f"<|im_start|>{m['role']}\n{m['content']}<|im_end|>")
    out.append("<|im_start|>assistant\n")          # generation starts here
    return "\n".join(out)

instruct_prompt = chat_template([
    {"role": "system", "content": "Answer in one word."},
    {"role": "user", "content": question},
])

print("BASE MODEL PROMPT\n" + base_prompt + "\n")
print("INSTRUCT MODEL PROMPT\n" + instruct_prompt)
