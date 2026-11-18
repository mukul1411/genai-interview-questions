# GraphRAG in miniature: entities -> graph -> communities -> community summaries -> global answer.
from collections import Counter, defaultdict

# Entities already extracted per document (GraphRAG uses an LLM for this step).
doc_entities = {
    "d1": ["Card Fraud Team", "Chargebacks", "Issuer Banks"],
    "d2": ["Chargebacks", "Issuer Banks", "Dispute Portal"],
    "d3": ["Card Fraud Team", "Dispute Portal"],
    "d4": ["Treasury", "FX Hedging", "Liquidity"],
    "d5": ["FX Hedging", "Liquidity", "Treasury"],
}
adj = defaultdict(Counter)                       # co-occurrence graph
for ents in doc_entities.values():
    for a in ents:
        for b in ents:
            if a != b: adj[a][b] += 1

label = {n: n for n in adj}                      # label propagation community detection
for _ in range(5):
    for n in sorted(adj):
        votes = Counter()
        for m, w in adj[n].items(): votes[label[m]] += w
        label[n] = max(sorted(votes), key=lambda l: votes[l])

communities = defaultdict(list)
for n, l in label.items(): communities[l].append(n)
summaries = {f"C{i}": f"Theme around {', '.join(sorted(m))}" for i, m in enumerate(communities.values(), 1)}
for cid, s in summaries.items():
    print(cid, "->", s)

# A GLOBAL question ("what are the main themes?") is answered map-reduce style over community
# summaries, not over the few chunks a vector search would return.
print("\nGlobal answer: the corpus covers", len(summaries), "themes:",
      "; ".join(s.replace("Theme around ", "") for s in summaries.values()))
