# Mitigating "lost in the middle": put the strongest evidence at the edges of the context.
ranked = ["doc1 (best)", "doc2", "doc3", "doc4", "doc5", "doc6 (weakest)"]

def edge_reorder(docs):
    # alternate: rank 1 first, rank 2 last, rank 3 second, rank 4 second-to-last, ...
    front, back = [], []
    for i, d in enumerate(docs):
        (front if i % 2 == 0 else back).append(d)
    return front + back[::-1]

print("retriever order:", ranked)
print("edge reordered :", edge_reorder(ranked))
