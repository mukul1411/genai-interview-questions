# Fine-tune or RAG? Encode the decision as explicit questions so the trade-off is reviewable.
def recommend(knowledge_changes_often, needs_citations, problem_is_behaviour_or_format,
              has_quality_labelled_examples, latency_or_cost_critical):
    reasons = []
    rag = knowledge_changes_often or needs_citations
    ft = problem_is_behaviour_or_format and has_quality_labelled_examples
    if knowledge_changes_often: reasons.append("facts change -> keep them out of weights")
    if needs_citations: reasons.append("answers must cite sources -> retrieval")
    if problem_is_behaviour_or_format: reasons.append("problem is style/format/skill -> tuning can help")
    if not has_quality_labelled_examples: reasons.append("no labelled data -> fine-tuning not ready")
    if latency_or_cost_critical: reasons.append("long prompts are costly -> tuning or distillation may pay")
    verdict = "both: RAG for facts, fine-tune for behaviour" if rag and ft else \
              "RAG" if rag else "fine-tune" if ft else "prompting first"
    return verdict, reasons

cases = {
    "HR policy assistant": (True, True, False, False, False),
    "Invoice JSON extractor (10k labelled)": (False, False, True, True, True),
    "Support bot with brand voice + KB": (True, True, True, True, False),
}
for name, args in cases.items():
    v, why = recommend(*args)
    print(f"{name}: {v}\n   " + "; ".join(why))
