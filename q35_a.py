# Where keyword search wins, where semantic search wins.
import re
from collections import Counter

docs = {"D1": "Reset your passcode from the security settings page",
        "D2": "Error code PX-2231 indicates an expired certificate",
        "D3": "Error code PX-2213 indicates a revoked certificate"}
SYN = {"password": "passcode", "credentials": "passcode"}     # stand-in for learned similarity
tok = lambda s: re.findall(r"[a-z0-9-]+", s.lower())

def keyword(q, d): return len(set(tok(q)) & set(tok(d)))
def semantic(q, d):
    # embeddings capture meaning but blur near-identical identifiers
    norm = lambda t: "px-code" if re.fullmatch(r"px-\d+", t) else SYN.get(t, t)
    return len({norm(t) for t in tok(q)} & {norm(t) for t in tok(d)})

for q in ["how do I change my password", "PX-2231"]:
    kw = sorted(docs, key=lambda k: -keyword(q, docs[k]))
    se = sorted(docs, key=lambda k: -semantic(q, docs[k]))
    print(f"{q!r}\n  keyword : {[(k, keyword(q, docs[k])) for k in kw]}\n  semantic: {[(k, semantic(q, docs[k])) for k in se]}")
