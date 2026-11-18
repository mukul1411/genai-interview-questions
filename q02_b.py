# Why attention cost matters: the score matrix grows with the square of sequence length.
for n in [1_000, 8_000, 32_000, 128_000]:
    entries = n * n                      # one score per (query, key) pair, per head, per layer
    mb = entries * 2 / 1e6               # if materialised naively in fp16 (2 bytes per score)
    print(f"n={n:>7,}  score entries={entries:>16,}  naive fp16 memory per head per layer = {mb:>10,.1f} MB")
print("\nFlashAttention-style kernels avoid materialising this matrix, but compute is still O(n^2).")
