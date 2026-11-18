# LoRA: freeze W, learn a low-rank update B@A, scale by alpha/r. Parameter count and a forward pass.
import random

d, k, r, alpha = 4096, 4096, 16, 32
full, lora = d * k, r * (d + k)
print(f"one {d}x{k} projection: full fine-tune {full:,} params, LoRA r={r}: {lora:,} params "
      f"({lora / full:.2%})")

# A tiny numeric forward pass (d=k=4, r=1) so you can check it by hand.
W = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]   # frozen pretrained weight
A = [[0.5, 0.0, 0.5, 0.0]]                                     # r x k  (initialised random)
B = [[0.0], [0.2], [0.0], [0.4]]                               # d x r  (initialised to ZERO in practice)
x = [1.0, 2.0, 3.0, 4.0]
scale = 2 / 1                                                  # alpha / r with alpha=2, r=1

matvec = lambda M, v: [sum(m * vi for m, vi in zip(row, v)) for row in M]
Ax = matvec(A, x)                                              # project down to r dims
delta = [scale * b[0] * Ax[0] for b in B]                      # project back up
y = [w + dl for w, dl in zip(matvec(W, x), delta)]
print("W x            =", matvec(W, x))
print("(alpha/r) B A x=", delta)
print("y              =", y)

# After training, merge for zero inference overhead: W' = W + (alpha/r) * B @ A
W_merged = [[W[i][j] + scale * B[i][0] * A[0][j] for j in range(4)] for i in range(4)]
print("merged W' x    =", [round(v, 6) for v in matvec(W_merged, x)], "(identical, no extra latency)")
