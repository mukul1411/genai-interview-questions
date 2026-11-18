# A latency model you can reason with: total = queueing + TTFT (prefill) + output_tokens / decode speed.
def latency(prompt_tok, out_tok, prefill_tok_s=5000, decode_tok_s=60, overhead_s=0.15, cached_frac=0.0):
    ttft = overhead_s + prompt_tok * (1 - cached_frac) / prefill_tok_s
    return ttft, ttft + out_tok / decode_tok_s

scenarios = {
    "baseline (8k prompt, 600 out)": dict(prompt_tok=8000, out_tok=600),
    "trim prompt to 3k": dict(prompt_tok=3000, out_tok=600),
    "+ cap output at 200": dict(prompt_tok=3000, out_tok=200),
    "+ 80% prefix cache hit": dict(prompt_tok=3000, out_tok=200, cached_frac=0.8),
    "+ smaller model (2.5x decode)": dict(prompt_tok=3000, out_tok=200, cached_frac=0.8, decode_tok_s=150),
}
for name, kw in scenarios.items():
    ttft, total = latency(**kw)
    print(f"{name:<32} TTFT {ttft:5.2f}s   total {total:5.2f}s")
print("\nOutput length dominates: decode is sequential. Streaming hides it; it does not remove it.")
