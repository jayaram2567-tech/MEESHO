import csv
import os
import sqlite3

# 1. Database and Output path set panrathu
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "meesho_reseller.db")
output_csv = os.path.join(current_dir, "fixtures", "mom_growth_report.csv")

# 2. Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 3. Neenga sonna antha SQL Query
query = """
WITH ranked_revenue AS (
    SELECT 
        month,
        category,
        revenue,
        CASE month
            WHEN 'January' THEN 1
            WHEN 'February' THEN 2
            WHEN 'March' THEN 3
            WHEN 'April' THEN 4
            WHEN 'May' THEN 5
            WHEN 'June' THEN 6
            WHEN 'July' THEN 7
            WHEN 'August' THEN 8
            WHEN 'September' THEN 9
            WHEN 'October' THEN 10
            WHEN 'November' THEN 11
            WHEN 'December' THEN 12
            ELSE 0
        END as month_num
    FROM Monthly_revenue_by_category
),
with_previous AS (
    SELECT 
        month,
        month_num,
        category,
        revenue,
        LAG(revenue) OVER (PARTITION BY category ORDER BY month_num) AS previous_revenue
    FROM ranked_revenue
),
with_growth AS (
    SELECT 
        month,
        month_num,
        category,
        revenue,
        previous_revenue,
        CASE 
            WHEN previous_revenue IS NULL OR previous_revenue = 0 THEN NULL
            ELSE ROUND(((revenue - previous_revenue) * 100.0) / previous_revenue, 2)
        END AS mom_pct
    FROM with_previous
)
SELECT 
    month,
    category,
    revenue,
    COALESCE(CAST(previous_revenue AS TEXT), 'N/A') AS previous_revenue,
    COALESCE(CAST(mom_pct AS TEXT), 'N/A') AS mom_pct,
    CASE 
        WHEN mom_pct IS NULL THEN 'N/A'
        WHEN ABS(mom_pct) > 8.0 THEN 'flagged'
        WHEN ABS(mom_pct) < 8.0 THEN 'not_flagged'
        ELSE 'escalate_exact_boundary'
    END AS flag_status
FROM with_growth
ORDER BY category, month_num;
"""

# 4. Execute query and fetch results
cursor.execute(query)
rows = cursor.fetchall()

# Get column headers from cursor description
column_names = [description[0] for description in cursor.description]

# 5. Export results to CSV file
os.makedirs(os.path.dirname(output_csv), exist_ok=True)
with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
  writer = csv.writer(f)
  writer.writerow(column_names)  # Write header
  writer.writerows(rows)  # Write data rows

conn.close()
print(f"Success! SQL Report exported as CSV at: {output_csv}")