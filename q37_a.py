# The critique-and-revise loop at the heart of Constitutional AI's supervised phase.
# The critic here is rule-based so it runs offline; in CAI the same model critiques itself
# against each principle, and the revisions become training data.
import re

CONSTITUTION = [
    ("no_guarantees", r"\bguarantee(d)?\b", "Do not promise outcomes you cannot guarantee.",
     lambda t: re.sub(r"is guaranteed", "is expected", re.sub(r"\bguarantee\b", "expect", t))),
    ("no_personal_data", r"\b\d{4} \d{4} \d{4} \d{4}\b", "Do not repeat full card numbers.",
     lambda t: re.sub(r"\b\d{4} \d{4} \d{4} (\d{4})\b", r"card ending \1", t)),
    ("cite_policy", r"^(?!.*policy).*$", "Ground refund statements in the stated policy.",
     lambda t: t + " (per refund policy section 4.2)"),
]

draft = "Your refund for 4111 1111 1111 1111 is guaranteed within 5 days."
response = draft
for name, pattern, principle, revise in CONSTITUTION:
    if re.search(pattern, response, re.I | re.S):
        print(f"critique [{name}]: {principle}")
        response = revise(response)
print("\ndraft   :", draft)
print("revision:", response)
