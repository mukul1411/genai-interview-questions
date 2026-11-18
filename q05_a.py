# Top-k keeps a fixed number of tokens; top-p keeps the smallest set whose mass reaches p.
peaked = {"Paris": 0.90, "Lyon": 0.04, "France": 0.03, "the": 0.02, "Nice": 0.01}
flat = {"blue": 0.22, "calm": 0.20, "vast": 0.18, "grey": 0.15, "deep": 0.13, "wild": 0.12}

def top_k(p, k):
    keep = sorted(p, key=p.get, reverse=True)[:k]
    return renorm({t: p[t] for t in keep})

def top_p(p, threshold):
    keep, mass = [], 0.0
    for t in sorted(p, key=p.get, reverse=True):
        keep.append(t)
        mass += p[t]
        if mass >= threshold:
            break
    return renorm({t: p[t] for t in keep})

def renorm(p):
    s = sum(p.values())
    return {t: round(v / s, 3) for t, v in p.items()}

for name, p in [("peaked (factual)", peaked), ("flat (creative)", flat)]:
    print(name)
    print("  top-k=3   ->", top_k(p, 3))
    print("  top-p=0.9 ->", top_p(p, 0.9))
