# A complete (toy) RAG pipeline: chunk -> index -> retrieve -> grounded prompt -> answer with citation.
import math, re
from collections import Counter

docs = {
    "refund-policy-2026.md": "Refunds above 500 USD require manager approval. "
                             "Refunds are paid to the original payment method within 5 business days. "
                             "Card refunds older than 120 days are paid by bank transfer instead.",
    "fees.md": "International card payments carry a 1.5 percent cross-border fee. "
               "Domestic card payments carry no cross-border fee.",
}

def chunks(doc_id, text):                                      # 1. chunk by sentence
    return [(f"{doc_id}#{i}", s.strip()) for i, s in enumerate(re.split(r"(?<=\.)\s+", text)) if s.strip()]

def vec(text):                                                 # 2. embed (bag of words stand-in)
    return Counter(re.findall(r"[a-z0-9]+", text.lower()))

def cosine(a, b):
    dot = sum(a[t] * b[t] for t in a)
    return dot / (math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values())) or 1)

index = [(cid, text, vec(text)) for d, t in docs.items() for cid, text in chunks(d, t)]

def retrieve(q, k=2):                                          # 3. retrieve
    qv = vec(q)
    return sorted(index, key=lambda r: cosine(qv, r[2]), reverse=True)[:k]

def grounded_prompt(q, hits):                                  # 4. augment
    ctx = "\n".join(f"[{cid}] {text}" for cid, text, _ in hits)
    return (f"Answer using ONLY the sources below. Cite the source id. "
            f"If the answer is not in the sources, say you don't know.\n\nSOURCES:\n{ctx}\n\nQUESTION: {q}")

q = "How long do card refunds take to arrive?"
hits = retrieve(q)
print(grounded_prompt(q, hits))
print("\nTop source:", hits[0][0])                             # 5. the generator would answer from here
