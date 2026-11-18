# Scaled dot-product self-attention with a causal mask, in pure Python.
import math

tokens = ["The", "river", "bank"]
# Toy 4-d vectors (in a real model these come from learned projections W_q, W_k, W_v).
Q = [[1.0, 0.0, 0.5, 0.0], [0.0, 1.0, 0.0, 0.5], [0.2, 0.9, 0.1, 0.8]]
K = [[1.0, 0.1, 0.0, 0.0], [0.1, 1.0, 0.2, 0.9], [0.0, 0.3, 1.0, 0.2]]
V = [[1.0, 0.0], [0.0, 1.0], [0.5, 0.5]]
d_k = len(Q[0])

def softmax(xs):
    m = max(xs)
    e = [math.exp(x - m) for x in xs]
    s = sum(e)
    return [x / s for x in e]

for i, q in enumerate(Q):
    scores = []
    for j, k in enumerate(K):
        if j > i:                       # causal mask: no peeking at future tokens
            scores.append(float("-inf"))
        else:
            scores.append(sum(a * b for a, b in zip(q, k)) / math.sqrt(d_k))
    w = softmax(scores)
    out = [sum(w[j] * V[j][c] for j in range(len(V))) for c in range(2)]
    pretty = ", ".join(f"{tokens[j]}={w[j]:.2f}" for j in range(len(tokens)))
    print(f"{tokens[i]:>5} attends to -> {pretty}   output={[round(x, 3) for x in out]}")
