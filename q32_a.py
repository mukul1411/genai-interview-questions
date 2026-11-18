# Large schemas: retrieve only the relevant tables (plus join neighbours) before generating SQL.
import re

SCHEMA = {   # table -> (description, columns, foreign keys)
    "orders": ("customer orders with revenue", ["id", "customer_id", "category_id", "revenue", "order_date"],
               ["customers", "categories"]),
    "categories": ("product category names", ["id", "name"], []),
    "customers": ("customer master data", ["id", "name", "region"], []),
    "payroll": ("employee salaries", ["emp_id", "salary", "month"], ["employees"]),
    "employees": ("staff directory", ["id", "name", "dept"], []),
    "web_sessions": ("site visit logs", ["id", "customer_id", "started_at"], ["customers"]),
}
SYNONYMS = {"revenue": ["revenue", "sales", "income"], "category": ["category", "categories", "product"],
            "month": ["month", "monthly"], "customer": ["customer", "client"]}

def terms(text):
    t = set(re.findall(r"[a-z]+", text.lower()))
    return t | {k for k, syns in SYNONYMS.items() if t & set(syns)}

def relevant_tables(question, top=2):
    q = terms(question)
    def score(name):
        desc, cols, _ = SCHEMA[name]
        return len(q & (terms(name) | terms(desc) | {c for col in cols for c in terms(col.replace("_", " "))}))
    picked = [t for t in sorted(SCHEMA, key=score, reverse=True)[:top] if score(t) > 0]
    for t in list(picked):                                  # add FK neighbours so joins are possible
        picked += [n for n in SCHEMA[t][2] if n not in picked and n in terms(question) | {"categories"}]
    return picked

question = "Show me monthly sales by product category in 2024"
tables = relevant_tables(question)
print("question:", question)
print("tables sent to the model:", tables, f"({len(tables)} of {len(SCHEMA)})")
for t in tables:
    print(f"  CREATE TABLE {t}({', '.join(SCHEMA[t][1])});  -- {SCHEMA[t][0]}")
