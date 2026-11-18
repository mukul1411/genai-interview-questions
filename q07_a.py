# Three chunking strategies on the same text, and why boundaries matter.
import re

text = ("Section 4.2 Refund limits. Refunds above 500 USD require manager approval. "
        "Exception: refunds for duplicate charges are approved automatically, "
        "regardless of amount.\n\nSection 4.3 Timelines. Refunds settle in 5 business days.")

def fixed(text, size=80, overlap=0):
    step = size - overlap
    return [text[i:i + size] for i in range(0, len(text), step)]

def sentences(text, max_chars=200):
    out, cur = [], ""
    for s in re.split(r"(?<=[.!?])\s+", text):
        if len(cur) + len(s) > max_chars and cur:
            out.append(cur.strip()); cur = ""
        cur += s + " "
    return out + ([cur.strip()] if cur.strip() else [])

def recursive(text, max_chars=200, seps=("\n\n", ". ", " ")):
    # split on the largest structural separator first; recurse only into pieces still too long
    if len(text) <= max_chars or not seps:
        return [text.strip()] if text.strip() else []
    out = []
    for piece in text.split(seps[0]):
        out += recursive(piece, max_chars, seps[1:])
    return out

for name, cs in [("fixed 80, no overlap", fixed(text)), ("sentence-packed", sentences(text)),
                 ("recursive, paragraph first", recursive(text))]:
    print(f"--- {name}: {len(cs)} chunks")
    for c in cs:
        flag = "  <-- rule split from its exception" if "500 USD" in c and "duplicate" not in c else ""
        print(f"  | {c!r}{flag}")
