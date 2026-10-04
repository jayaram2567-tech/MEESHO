import csv
import os
import sqlite3

# 1. Get the current folder where this load_db.py script is running
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Automatically point to the CSV file location
# Ungaloda CSV file 'fixtures' folder kulla iruntha ithu podhum:
csv_path = os.path.join(current_dir, "fixtures", "Monthly_revenue_by_category.csv")

# Oru vela ungaloda CSV file 'part2_engine/fixtures' kulla iruntha, mela irukurathuku badhila kinna kodutha line use pannikonga:
# csv_path = os.path.join(current_dir, "part2_engine", "fixtures", "monthly_category_revenue.csv")

print(f"Searching CSV at: {csv_path}")

# 3. Connect to SQLite database
db_path = os.path.join(current_dir, "meesho_reseller.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 4. Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Monthly_revenue_by_category  (
        month TEXT,
        category TEXT,
        revenue REAL,
        n_orders INTEGER
    )
""")

cursor.execute("DELETE FROM Monthly_revenue_by_category")

# 5. Read CSV and insert into Database
with open(csv_path, mode="r", encoding="utf-8") as f:
  reader = csv.DictReader(f)
  for row in reader:
    cursor.execute(
        """
        INSERT INTO Monthly_revenue_by_category (month, category, revenue, n_orders)
        VALUES (?, ?, ?, ?)
    """,
        (row["month"], row["category"], float(row["revenue"]), int(row["n_orders"])),
    )

conn.commit()
conn.close()

print(
    "Success!Monthly_revenue_by_category table created and CSV loaded into"
    f" {db_path}"
)




