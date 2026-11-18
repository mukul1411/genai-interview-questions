# Two classic naive-RAG failures and their fixes: stale versions and missing metadata filters.
import re
from collections import Counter

chunks = [
    {"id": "p2023", "year": 2023, "text": "Refund approval threshold is 1000 USD for all refunds."},
    {"id": "p2025", "year": 2025, "text": "Refund approval threshold is 500 USD for card refunds."},
    {"id": "hr", "year": 2025, "text": "Expense approval threshold for travel is 300 USD."},
]
tok = lambda s: Counter(re.findall(r"[a-z0-9]+", s.lower()))
score = lambda q, c: sum((tok(q) & tok(c["text"])).values())

q = "What is the refund approval threshold for refunds?"
naive = sorted(chunks, key=lambda c: -score(q, c))
print("NAIVE top-1   :", naive[0]["id"], "->", naive[0]["text"])

# Fix: filter on metadata first (current documents only), then rank.
current = [c for c in chunks if c["year"] == max(x["year"] for x in chunks)]
fixed = sorted(current, key=lambda c: -score(q, c))
print("FILTERED top-1:", fixed[0]["id"], "->", fixed[0]["text"])
