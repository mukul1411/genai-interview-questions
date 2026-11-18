# Self-consistency: sample several chain-of-thought answers, extract the final answers, take a vote.
import re
from collections import Counter

# Five reasoning paths a model might produce at temperature > 0 (written out here so this runs offline).
samples = [
    "200 units at 4.00 is 800. Minus 10% discount is 720. Plus 18% tax: 720 * 1.18 = 849.60. Final answer: 849.60",
    "Subtotal 800, discount 80 gives 720, tax 129.60, total 849.60. Final answer: 849.60",
    "800 plus 18% tax is 944, minus 10% is 849.60. Final answer: 849.60",
    "800 minus 10% is 720. Tax 18% of 800 is 144. 720 + 144 = 864. Final answer: 864.00",
    "720 after discount; 720 * 0.18 = 129.6; total 849.6. Final answer: 849.60",
]

def final_answer(text):
    m = re.search(r"Final answer:\s*([0-9.,]+)", text)
    return m.group(1) if m else None

votes = Counter(final_answer(s) for s in samples)
answer, n = votes.most_common(1)[0]
print("votes:", dict(votes))
print(f"self-consistent answer: {answer}  (agreement {n}/{len(samples)})")
