# Few-shot prompting with DYNAMIC example selection: pick the labelled examples most similar to the input.
import re

labelled = [
    ("I was charged twice for one order", "duplicate_charge"),
    ("The parcel never arrived", "not_received"),
    ("I did not make this purchase", "fraud"),
    ("Two identical charges on my statement", "duplicate_charge"),
    ("Item arrived broken", "defective"),
    ("Someone used my card without permission", "fraud"),
]
words = lambda s: set(re.findall(r"[a-z]+", s.lower()))
sim = lambda a, b: len(words(a) & words(b)) / len(words(a) | words(b))

def build_prompt(text, k=3):
    shots = sorted(labelled, key=lambda ex: -sim(text, ex[0]))[:k]
    lines = ["Classify the dispute into one of: duplicate_charge, not_received, fraud, defective.", ""]
    lines += [f"Text: {t}\nLabel: {l}\n" for t, l in shots]
    lines += [f"Text: {text}\nLabel:"]
    return "\n".join(lines)

print(build_prompt("My card was charged twice for the same order"))
