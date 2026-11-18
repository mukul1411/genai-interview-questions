# Two checks every LLM-as-judge setup needs: position-swap consistency and agreement with humans.
# The judge below is SIMULATED with a known first-position bias so the checks can run offline.
import random

rng = random.Random(1)
def biased_judge(answer_a_quality, answer_b_quality):
    # prefers the better answer, but adds a bonus to whatever is shown first
    return "A" if answer_a_quality + 0.15 + rng.gauss(0, 0.1) > answer_b_quality else "B"

pairs = [(rng.random(), rng.random()) for _ in range(200)]
consistent = 0
for qa, qb in pairs:
    first = biased_judge(qa, qb)              # A shown first
    swapped = biased_judge(qb, qa)            # same pair, order swapped
    consistent += (first == "A" and swapped == "B") or (first == "B" and swapped == "A")
print(f"position-swap consistency: {consistent / len(pairs):.0%}  (count only consistent verdicts)")

# Cohen's kappa between judge and human labels on a calibration sample.
def kappa(a, b):
    labels = set(a) | set(b); n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(l) / n) * (b.count(l) / n) for l in labels)
    return (po - pe) / (1 - pe)

human = ["pass", "pass", "fail", "pass", "fail", "pass", "fail", "pass", "pass", "fail"]
judge = ["pass", "pass", "fail", "pass", "pass", "pass", "fail", "pass", "fail", "fail"]
print(f"raw agreement {sum(h == j for h, j in zip(human, judge)) / len(human):.0%}, "
      f"Cohen's kappa {kappa(human, judge):.2f}")
