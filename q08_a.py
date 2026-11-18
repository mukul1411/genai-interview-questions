# Hybrid search: BM25 (keyword) + vector (semantic) fused with Reciprocal Rank Fusion.
import math, re
from collections import Counter

docs = {
    "D1": "Error ERR-4012 means the card issuer declined the payment",
    "D2": "The bank refused the transaction because of insufficient funds",
    "D3": "How to reset your password and unlock your account",
    "D4": "Declined payments can be retried after the customer contacts their bank",
    "D5": "ERR-5001 indicates a timeout talking to the acquirer",
}
# Tiny "embedding": map words to concepts so synonyms land close together.
CONCEPTS = {"declined": "reject", "refused": "reject", "decline": "reject", "rejected": "reject",
            "payment": "txn", "transaction": "txn", "payments": "txn", "purchase": "txn",
            "bank": "issuer", "issuer": "issuer"}

tok = lambda s: re.findall(r"[a-z0-9-]+", s.lower())

def bm25_scores(q, k1=1.5, b=0.75):
    N = len(docs); avgdl = sum(len(tok(d)) for d in docs.values()) / N
    df = Counter(t for d in docs.values() for t in set(tok(d)))
    out = {}
    for did, d in docs.items():
        tf, dl, s = Counter(tok(d)), len(tok(d)), 0.0
        for t in tok(q):
            if t in tf:
                idf = math.log(1 + (N - df[t] + 0.5) / (df[t] + 0.5))
                s += idf * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * dl / avgdl))
        out[did] = s
    return out

def embed(s):
    # Real embeddings blur exact identifiers: every error code lands near every other one.
    norm = lambda t: "error-code" if re.fullmatch(r"err-\d+", t) else CONCEPTS.get(t, t)
    return Counter(norm(t) for t in tok(s) if len(t) > 3)

def vector_scores(q):
    qv = embed(q)
    def cos(a, b):
        dot = sum(a[t] * b[t] for t in a)
        return dot / (math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values())) or 1)
    return {did: cos(qv, embed(d)) for did, d in docs.items()}

def rank(scores):
    return [d for d, s in sorted(scores.items(), key=lambda x: -x[1]) if s > 0]

def rrf(*rankings, k=60):
    fused = Counter()
    for r in rankings:
        for pos, d in enumerate(r, 1):
            fused[d] += 1 / (k + pos)
    return [d for d, _ in fused.most_common()]

for q in ["ERR-4012", "my purchase was rejected"]:
    b, v = rank(bm25_scores(q)), rank(vector_scores(q))
    print(f"query: {q!r}\n  BM25  : {b}\n  vector: {v}\n  RRF   : {rrf(b, v)}\n")
