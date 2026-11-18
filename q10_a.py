# Evaluating retrieval with a labelled golden set: Recall@k, MRR, nDCG@k.
import math

golden = {   # question -> set of relevant chunk ids (labelled by a domain expert)
    "q1": {"c7"}, "q2": {"c2", "c9"}, "q3": {"c4"}, "q4": {"c1"},
}
retrieved = {  # what the system returned, in rank order
    "q1": ["c7", "c3", "c5"], "q2": ["c8", "c2", "c1"], "q3": ["c6", "c5", "c3"], "q4": ["c2", "c3", "c1"],
}

def recall_at_k(rel, ret, k): return len(rel & set(ret[:k])) / len(rel)
def mrr(rel, ret): return next((1 / i for i, d in enumerate(ret, 1) if d in rel), 0.0)
def ndcg(rel, ret, k):
    dcg = sum(1 / math.log2(i + 1) for i, d in enumerate(ret[:k], 1) if d in rel)
    ideal = sum(1 / math.log2(i + 1) for i in range(1, min(len(rel), k) + 1))
    return dcg / ideal

k = 3
for q in golden:
    print(f"{q}: recall@{k}={recall_at_k(golden[q], retrieved[q], k):.2f}  "
          f"MRR={mrr(golden[q], retrieved[q]):.2f}  nDCG@{k}={ndcg(golden[q], retrieved[q], k):.2f}")
avg = lambda f: sum(f(q) for q in golden) / len(golden)
print(f"\nMEAN recall@{k}={avg(lambda q: recall_at_k(golden[q], retrieved[q], k)):.2f}  "
      f"MRR={avg(lambda q: mrr(golden[q], retrieved[q])):.2f}  "
      f"nDCG@{k}={avg(lambda q: ndcg(golden[q], retrieved[q], k)):.2f}")
print("q3 is a retrieval miss: no generator can be faithful to a source it never saw.")
