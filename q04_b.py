# Same prompt, 10 samples at two temperatures (seeded so the output is reproducible).
import math, random

logits = {"sunny": 3.2, "cloudy": 2.5, "rainy": 2.1, "warm": 1.6, "cold": 1.2, "purple": -0.5}

def sample(T, rng):
    w = [math.exp(v / T) for v in logits.values()]
    return rng.choices(list(logits), weights=w)[0]

rng = random.Random(7)
for T in [0.2, 1.5]:
    draws = [sample(T, rng) for _ in range(10)]
    print(f"T={T}: {draws}")
