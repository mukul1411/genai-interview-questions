# A multi-hop question that a knowledge graph answers exactly and similarity search struggles with.
from collections import deque

edges = [  # (subject, relation, object)
    ("Acme Retail", "buys_from", "Northwind Parts"),
    ("Northwind Parts", "buys_from", "Delta Metals"),
    ("Delta Metals", "located_in", "Region X"),
    ("Region X", "has_sanction_status", "restricted"),
    ("Acme Retail", "buys_from", "Orbit Packaging"),
]
graph = {}
for s, r, o in edges:
    graph.setdefault(s, []).append((r, o))

def paths_to(start, predicate, max_hops=4):
    out, queue = [], deque([(start, [start])])
    while queue:
        node, path = queue.popleft()
        for rel, nxt in graph.get(node, []):
            p = path + [f"-{rel}->", nxt]
            if predicate(rel, nxt): out.append(" ".join(p))
            elif len(p) < max_hops * 2 + 1: queue.append((nxt, p))
    return out

print("Q: Is any supplier in Acme Retail's supply chain exposed to a restricted region?")
for p in paths_to("Acme Retail", lambda r, o: o == "restricted"):
    print("  ", p)
print("\nNo single document states this; the answer exists only as a 4-hop path.")
print("Vector search would retrieve chunks mentioning 'Acme' or 'restricted' and miss the chain between them.")
