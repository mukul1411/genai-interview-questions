# Temperature rescales logits before softmax: p_i = exp(z_i / T) / sum_j exp(z_j / T)
import math

logits = {"sunny": 3.2, "cloudy": 2.5, "rainy": 2.1, "warm": 1.6, "cold": 1.2, "purple": -0.5}

def dist(T):
    e = {k: math.exp(v / T) for k, v in logits.items()}
    s = sum(e.values())
    return {k: v / s for k, v in e.items()}

def entropy(p):
    return -sum(x * math.log2(x) for x in p.values() if x > 0)

for T in [0.2, 0.7, 1.0, 1.5]:
    p = dist(T)
    row = "  ".join(f"{k}:{v:5.1%}" for k, v in p.items())
    print(f"T={T:<4} entropy={entropy(p):.2f} bits | {row}")
