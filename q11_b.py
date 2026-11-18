# A position-sensitivity harness. The 'model' here is SIMULATED with a U-shaped accuracy
# curve so the harness can run offline; swap in a real model call to measure your own.
import random

def simulated_model_correct(position, n_docs, rng):
    rel = position / (n_docs - 1)                    # 0 = start, 1 = end
    p = 0.75 - 0.45 * (1 - abs(2 * rel - 1))         # high at edges, low in the middle
    return rng.random() < p

rng, n_docs, trials = random.Random(0), 20, 400
for pos in [0, 4, 9, 14, 19]:
    acc = sum(simulated_model_correct(pos, n_docs, rng) for _ in range(trials)) / trials
    print(f"answer document at position {pos + 1:>2}/{n_docs}: accuracy {acc:.0%}  " + "#" * int(acc * 40))
