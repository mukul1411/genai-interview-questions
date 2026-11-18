# Bi-encoder vs cross-encoder (reranker), simulated to show the structural difference.
# Bi-encoder: query and document are encoded SEPARATELY, compared with a dot product.
# Cross-encoder: query and document are read TOGETHER, so word interactions (like "not") count.
import re
from collections import Counter

docs = {
    "A": "Refunds are not available for gift cards",
    "B": "Refunds are available for gift cards bought in the last 30 days",
    "C": "Gift cards can be used in any store",
}
query = "are refunds available for gift cards"
tok = lambda s: re.findall(r"[a-z]+", s.lower())

def bi_encoder(q, d):
    # independent bags of words: order and negation are invisible
    qv, dv = Counter(tok(q)), Counter(tok(d))
    return sum(qv[t] * dv[t] for t in qv) / (len(tok(d)) ** 0.5)

def cross_encoder(q, d):
    # joint reading: rewards overlap, but flips the score if the doc negates the asked predicate
    qt, dt = tok(q), tok(d)
    overlap = sum(1 for t in qt if t in dt) / len(qt)
    negated = any(dt[i] == "not" and i + 1 < len(dt) and dt[i + 1] in qt for i in range(len(dt)))
    return overlap * (0.3 if negated else 1.0)

print("bi-encoder ranking   :", sorted(docs, key=lambda k: -bi_encoder(query, docs[k])))
print("cross-encoder ranking:", sorted(docs, key=lambda k: -cross_encoder(query, docs[k])))
print("\nCost: bi-encoder doc vectors are precomputed once; a cross-encoder must run once per (query, doc) pair.")
for n in [20, 100, 10_000]:
    print(f"  rerank {n:>6} candidates at ~8 ms each (unbatched) = {n * 8 / 1000:8.2f} s")
