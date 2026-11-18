# NL-to-SQL failure modes you can reproduce in SQLite, and a validator that catches the dangerous ones.
import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE orders(id INTEGER PRIMARY KEY, category TEXT, revenue REAL, order_date TEXT);
CREATE TABLE shipments(id INTEGER PRIMARY KEY, order_id INTEGER, carrier TEXT);
INSERT INTO orders VALUES (1,'books',100,'2024-01-15'),(2,'books',50,'2024-02-03'),(3,'toys',80,'2024-02-20'),
                          (4,'toys',NULL,'2024-03-01'),(5,'books',70,'2023-12-30');
INSERT INTO shipments VALUES (1,1,'DHL'),(2,1,'UPS'),(3,2,'DHL'),(4,3,'DHL');   -- order 1 shipped in two parts
""")
q = lambda sql: db.execute(sql).fetchall()

print("Question: total 2024 revenue by category")
correct = "SELECT category, SUM(revenue) FROM orders WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01' GROUP BY category"
print("  correct            :", q(correct))
fanout = ("SELECT o.category, SUM(o.revenue) FROM orders o JOIN shipments s ON s.order_id = o.id "
          "WHERE o.order_date LIKE '2024%' GROUP BY o.category")
print("  join fan-out bug   :", q(fanout), "<- order 1 counted twice")
print("  'last year' ambiguity: relative to today, or the last complete fiscal year? Must be resolved, not guessed.")
print("  AVG with NULLs     :", q("SELECT AVG(revenue) FROM orders WHERE category='toys'"), "<- NULL row silently excluded")

def validate(sql):
    s = sql.strip().rstrip(";")
    if not s.lower().startswith(("select", "with")): return "rejected: not read-only"
    if ";" in s: return "rejected: multiple statements"
    try:
        db.execute("EXPLAIN QUERY PLAN " + s)              # parses and plans without executing
    except sqlite3.Error as e:
        return f"rejected: {e}"
    return "ok" + ("" if " limit " in s.lower() else " (add LIMIT before running)")

for sql in [correct, "DROP TABLE orders", "SELECT * FROM order_items", "SELECT 1; DELETE FROM orders"]:
    print(f"validate {sql[:42]!r:<46} -> {validate(sql)}")
