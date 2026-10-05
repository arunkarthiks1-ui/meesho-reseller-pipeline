import csv
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "meesho_reseller.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "part1_sql", "output")
P2_FIXTURE_DIR = os.path.join(BASE_DIR, "part2_engine", "fixtures")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(P2_FIXTURE_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# 1. Monthly revenue by category
cur.execute("""
SELECT month, category, ROUND(SUM(quantity * unit_price), 2) AS revenue, COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY CASE month WHEN 'April' THEN 1 WHEN 'May' THEN 2 WHEN 'June' THEN 3 END, category;
""")
q1_rows = cur.fetchall()

with open(os.path.join(OUTPUT_DIR, "monthly_category_revenue.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["month", "category", "revenue", "n_orders"])
    w.writerows(q1_rows)

# Copy to Part 2 fixtures directory as required by specification
with open(os.path.join(P2_FIXTURE_DIR, "monthly_category_revenue.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["month", "category", "revenue", "n_orders"])
    w.writerows(q1_rows)

# 2. Region-wise revenue
cur.execute("""
SELECT r.region, ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue, COUNT(*) AS total_orders
FROM orders o
JOIN resellers r ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY total_revenue DESC;
""")
q2_rows = cur.fetchall()
with open(os.path.join(OUTPUT_DIR, "region_revenue.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["region", "total_revenue", "total_orders"])
    w.writerows(q2_rows)

# 3. Top Resellers
cur.execute("""
SELECT r.reseller_id, r.reseller_name, ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM resellers r
JOIN orders o ON r.reseller_id = o.reseller_id
GROUP BY r.reseller_id
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;
""")
q3_rows = cur.fetchall()
with open(os.path.join(OUTPUT_DIR, "top_resellers.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["reseller_id", "reseller_name", "total_spend"])
    w.writerows(q3_rows)

# 4. Zero Order Resellers
cur.execute("""
SELECT r.reseller_id, r.reseller_name, r.region
FROM resellers r
LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;
""")
q4_rows = cur.fetchall()
with open(os.path.join(OUTPUT_DIR, "zero_order_resellers.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["reseller_id", "reseller_name", "region"])
    w.writerows(q4_rows)

# 4b. Zero Order Count Demo
cur.execute("""
SELECT r.reseller_id, COUNT(*) AS count_star, COUNT(o.order_id) AS count_order_id
FROM resellers r
LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id;
""")
q4b_rows = cur.fetchall()
with open(os.path.join(OUTPUT_DIR, "zero_order_count_demo.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["reseller_id", "count_star", "count_order_id"])
    w.writerows(q4b_rows)

# 5. June Delivered AOV
cur.execute("""
SELECT ROUND(SUM(quantity * unit_price) / COUNT(*), 2) AS june_delivered_aov
FROM orders
WHERE month = 'June' AND status = 'Delivered';
""")
q5_rows = cur.fetchall()
with open(os.path.join(OUTPUT_DIR, "june_delivered_aov.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["june_delivered_aov"])
    w.writerows(q5_rows)

conn.close()
print("All Part 1 SQL output files successfully created!")