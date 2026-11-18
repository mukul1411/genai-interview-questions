# The minimum useful LLM trace: nested spans with latency, tokens and cost, aggregated per feature.
import time, uuid
from collections import defaultdict
from contextlib import contextmanager

PRICE = {"in": 3.0 / 1e6, "out": 15.0 / 1e6}       # illustrative USD per token
SPANS = []

@contextmanager
def span(name, feature, parent=None, **attrs):
    sid, t0 = uuid.uuid4().hex[:8], time.perf_counter()
    rec = {"id": sid, "parent": parent, "name": name, "feature": feature, **attrs}
    yield rec
    rec["ms"] = round((time.perf_counter() - t0) * 1000, 1)
    SPANS.append(rec)

def fake_llm(prompt_tokens, output_tokens):
    time.sleep(0.01)
    return {"in": prompt_tokens, "out": output_tokens}

for feature, n in [("refund_bot", 3), ("invoice_extract", 2)]:
    for _ in range(n):
        with span("invoke_agent", feature) as root:
            with span("retrieve", feature, parent=root["id"]):
                time.sleep(0.005)
            with span("chat", feature, parent=root["id"], model="model-x") as s:
                u = fake_llm(2400 if feature == "refund_bot" else 900, 300)
                s.update(tokens_in=u["in"], tokens_out=u["out"],
                         cost=u["in"] * PRICE["in"] + u["out"] * PRICE["out"])

agg = defaultdict(lambda: {"calls": 0, "cost": 0.0, "tokens": 0})
for s in SPANS:
    if s["name"] == "chat":
        a = agg[s["feature"]]; a["calls"] += 1; a["cost"] += s["cost"]; a["tokens"] += s["tokens_in"] + s["tokens_out"]
for f, a in agg.items():
    print(f"{f:<16} calls={a['calls']}  tokens={a['tokens']:>6,}  cost=${a['cost']:.4f}  "
          f"cost/call=${a['cost'] / a['calls']:.4f}")
print("example span:", {k: v for k, v in SPANS[1].items() if k != 'id'})
