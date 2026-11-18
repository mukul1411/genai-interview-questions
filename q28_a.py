# Multi-tenant RAG: why tenant filtering must happen INSIDE the search, not after it.
docs = [  # (tenant, text, similarity to the query) -- similarity precomputed for clarity
    ("acme", "Acme refund limit is 500 USD", 0.71),
    ("globex", "Globex refund limit is 2000 USD", 0.93),
    ("globex", "Globex refund approvals go to finance", 0.90),
    ("globex", "Globex refund FAQ", 0.88),
    ("acme", "Acme refund timelines", 0.65),
]

def post_filter(tenant, k=3):
    top = sorted(docs, key=lambda d: -d[2])[:k]        # search across everyone, THEN filter
    return [d[1] for d in top if d[0] == tenant]

def pre_filter(tenant, k=3):
    mine = [d for d in docs if d[0] == tenant]         # filter is part of the query
    return [d[1] for d in sorted(mine, key=lambda d: -d[2])[:k]]

def unfiltered(tenant, k=3):                           # the bug: someone forgot the filter
    return [d[1] for d in sorted(docs, key=lambda d: -d[2])[:k]]

print("post-filter (acme):", post_filter("acme"), "<- empty: recall destroyed")
print("pre-filter  (acme):", pre_filter("acme"))
print("no filter   (acme):", unfiltered("acme"), "<- cross-tenant leak")
