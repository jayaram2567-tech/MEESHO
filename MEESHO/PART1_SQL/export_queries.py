import sqlite3
import csv
import os

# 1. Base directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. SQL File Auto-Detect
SQL_FILE = os.path.join(SCRIPT_DIR, "queries.sql")
if not os.path.exists(SQL_FILE):
    SQL_FILE = os.path.join(SCRIPT_DIR, "quries.sql")

# 3. Database File Auto-Detect
DB_FILE = os.path.join(SCRIPT_DIR, "meesho_reseller.db")
if not os.path.exists(DB_FILE):
    PARENT_DIR = os.path.dirname(SCRIPT_DIR)
    DB_FILE = os.path.join(PARENT_DIR, "meesho_reseller.db")

# 4. OUTPUT Folder Auto-Setup
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "OUTPUT")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------
# 5. DEFINE YOUR CUSTOM CSV FILENAMES HERE (in order of queries)
# -------------------------------------------------------------
CUSTOM_FILENAMES = [
    "Monthly_revenue_by_category.csv",          # Query 1
    "Region_wise_revenue.csv",                  # Query 2
    "Top_five_resellers.csv",                   # Query 3
    "Resellers_Who_NEVER_Placed_an_Orders.csv", # Query 4
    "COUNT_star_VS_COUNT_order_id.csv",         # Query 5 (Changed * to star because Windows doesn't allow * in filenames)
    "AOV.csv",                                  # Query 6
    "Top_Five_Orders.csv"                       # Query 7
    "Total_revenue.csv"                         # Query 8
]

print("--- PATH CHECK ---")
print(f"Using DB File:  {DB_FILE}")
print(f"Using SQL File: {SQL_FILE}")
print(f"Output Folder: {OUTPUT_DIR}")
print("-------------------\n")

try:
    if not os.path.exists(DB_FILE):
        raise FileNotFoundError(f"Database file not found: {DB_FILE}. Make sure to run generate_dataset.py first.")

    if not os.path.exists(SQL_FILE):
        raise FileNotFoundError(f"SQL file not found at: {SQL_FILE}")

    # Connect to Database
    conn = sqlite3.connect(DB_FILE)
    
    # Read SQL file
    with open(SQL_FILE, "r", encoding="utf-8") as file:
        sql_text = file.read()

    # Split queries by semicolon (;)
    raw_queries = sql_text.split(";")
    query_index = 0

    for raw_query in raw_queries:
        # Remove standalone SQL comment lines
        query_lines = [
            line for line in raw_query.splitlines()
            if not line.strip().startswith("--")
        ]
        query = "\n".join(query_lines).strip()
        
        # Skip empty queries
        if not query:
            continue

        try:
            cursor = conn.execute(query)
            rows = cursor.fetchall()

            # Only generate CSV if query returned tabular data (SELECT queries)
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]

                # Use custom name if in list; otherwise fallback to query_XX.csv
                if query_index < len(CUSTOM_FILENAMES):
                    filename = CUSTOM_FILENAMES[query_index]
                else:
                    filename = f"query_{query_index + 1:02d}.csv"

                output_path = os.path.join(OUTPUT_DIR, filename)

                with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(columns)
                    writer.writerows(rows)

                print(f"SUCCESS: Saved {filename}")
                query_index += 1

        except Exception as e:
            print(f"Error in Query {query_index + 1}: {e}")

    conn.close()
    print("\n🎉 ALL QUERY OUTPUTS EXPORTED SUCCESSFULLY TO 'OUTPUT' FOLDER!")

except Exception as main_err:
    print(f"Critical Error: {main_err}")