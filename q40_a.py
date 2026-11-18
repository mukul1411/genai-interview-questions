# Offline evaluation (golden set with a confidence interval) and online evaluation (A/B test).
import math

def wilson(passed, n, z=1.96):
    p = passed / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return centre - half, centre + half

for name, passed, n in [("prompt v1", 172, 200), ("prompt v2", 181, 200)]:
    lo, hi = wilson(passed, n)
    print(f"OFFLINE {name}: {passed}/{n} = {passed / n:.1%}  95% CI [{lo:.1%}, {hi:.1%}]")
print("  -> intervals overlap: the offline gain alone is not conclusive.\n")

# Online: share of conversations resolved without human escalation
a_ok, a_n = 4_120, 5_000      # control (v1)
b_ok, b_n = 4_260, 5_000      # treatment (v2)
pa, pb = a_ok / a_n, b_ok / b_n
p = (a_ok + b_ok) / (a_n + b_n)
z = (pb - pa) / math.sqrt(p * (1 - p) * (1 / a_n + 1 / b_n))
pval = math.erfc(abs(z) / math.sqrt(2))
print(f"ONLINE resolution rate: control {pa:.1%}, treatment {pb:.1%}, lift {pb - pa:+.1%}, z={z:.2f}, p={pval:.4f}")
