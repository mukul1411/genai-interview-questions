# Reference-based metrics: exact match, token F1, and ROUGE-L (longest common subsequence).
import re

def norm(s): return re.findall(r"[a-z0-9]+", s.lower())

def exact_match(pred, gold): return float(norm(pred) == norm(gold))

def token_f1(pred, gold):
    p, g = norm(pred), norm(gold)
    common = sum(min(p.count(t), g.count(t)) for t in set(p))
    if common == 0: return 0.0
    prec, rec = common / len(p), common / len(g)
    return 2 * prec * rec / (prec + rec)

def rouge_l(pred, gold):
    a, b = norm(pred), norm(gold)
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a)):
        for j in range(len(b)):
            dp[i + 1][j + 1] = dp[i][j] + 1 if a[i] == b[j] else max(dp[i][j + 1], dp[i + 1][j])
    lcs = dp[-1][-1]
    if lcs == 0: return 0.0
    p, r = lcs / len(a), lcs / len(b)
    return 2 * p * r / (p + r)

gold = "Refunds above 500 USD require manager approval"
for pred in ["Refunds above 500 USD require manager approval",
             "A manager must approve refunds over 500 USD",
             "Refunds above 500 USD do not require approval"]:
    print(f"EM={exact_match(pred, gold):.0f}  F1={token_f1(pred, gold):.2f}  "
          f"ROUGE-L={rouge_l(pred, gold):.2f} | {pred}")
print("\nNote the third answer: high lexical overlap, opposite meaning. Lexical metrics alone are not enough.")
