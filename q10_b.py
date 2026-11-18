# A crude faithfulness check: is each answer sentence supported by some retrieved sentence?
# (Production systems use an NLI model or an LLM judge; the shape of the metric is the same.)
import re

context = ["Refunds above 500 USD require manager approval.",
           "Refunds settle in 5 business days."]
answer = ("Refunds above 500 USD need manager approval. They settle in 5 business days. "
          "Refunds under 50 USD are processed instantly.")

words = lambda s: set(re.findall(r"[a-z0-9]+", s.lower())) - {"the", "in", "are", "they", "a"}

def supported(claim, ctx, threshold=0.6):
    return max(len(words(claim) & words(c)) / len(words(claim)) for c in ctx) >= threshold

claims = [c for c in re.split(r"(?<=\.)\s+", answer) if c]
for c in claims:
    print(("SUPPORTED   " if supported(c, context) else "UNSUPPORTED ") + c)
score = sum(supported(c, context) for c in claims) / len(claims)
print(f"\nfaithfulness = {score:.2f}  (1 of 3 claims is invented)")
