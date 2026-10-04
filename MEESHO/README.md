PART1-The Foundation (SQL Business Query Engine)

Generating the Data: We start by running the provided generate_dataset.py script.
 This acts as our mock backend, spitting out orders.csv, resellers.csv, and a 
 SQLite database (meesho_reseller.db) pre-loaded with 900 orders.

Writing the Queries: We connect to that SQLite database. Instead of complex Python logic, 
we use pure SQL to answer the business questions. We group the data by month and category to get the revenue,
 join the orders and resellers tables to see which region spends the most, and find our top 5 VIP resellers as in csv files.

And also create a csv files as
=>Total revenue
=>Resellers who never placed an orders
=>Region wise Revenue
=>Monthly revenue by category
=>Average Order Value
=>Count vs count orders
=>Monthly sales

The Zero-Order Trap: For the reseller who never placed an order, we use a LEFT JOIN and check WHERE order_id IS NULL. The narrative catch here is understanding why COUNT(*) fails (it counts the empty joined row as "1") and why we must use COUNT(order_id) (which correctly sees "0").

The Output: We export the results of these queries into the part1_sql/output/ folder as CSV files. 
The most important file here is monthly_category_revenue.csv
This file is the golden source of truth that we will hand over to

Part 2: The Brain (Python Guardrail & Growth Engine)

The Goal: Build the mathematical rules and safety checks (guardrails) so an automated system doesn't crash or send bad data to a manager.

Building the Math: We create growth_engine.py. We write a simple function to calculate Month-over-Month (MoM) growth percentages.
 We write a second function that looks at that percentage and categorizes it: if it swings by more than 8%, it returns "flagged". If it's exactly 8%, it returns "escalate_exact_boundary" (because AI shouldn't guess on edge cases).

Building the Bouncer (Validate Feed): We write a validate_feed function. Before any math happens, this function reads the monthly_category_revenue.csv line by line. It actively hunts for missing categories, missing revenues, or negative numbers. If it finds one, it logs an error and shuts down the process.

Proving it Works: We write Given-When-Then unit tests (test_growth_engine.py).
 We feed it a deliberately corrupted CSV fixture. 
 The test proves that our engine successfully catches the negative revenue and blank fields, 
 outputting exactly three error messages.

Part 3: The Voice (Reliable AI Narrative)

The Goal: Translate the raw percentages from Part 2 into a professional, zero-hallucination text update for regional managers, while protecting user privacy.

The Prompt Pack: We create a Markdown file (prompt_pack.md) that acts as a strict template. It takes the variables calculated in Part 2 ({category}, {mom_pct}, etc.) and slots them into a "Context -> Insight -> Implication" structure.

The Golden Rule: The checklist enforces that no numbers are invented. If Ethnic Wear grew by 77.1% (a FACT based on Part 1's data), we state exactly that. We then propose a HYPOTHESIS for the manager to investigate (e.g., "check active reseller counts").

Data Masking: We write a Python script (masking.py) with a security function. It takes a raw ID like "RS019" and converts it to "ALIAS-19". We pass our drafted text through an assertion check to guarantee that real reseller names (like "Mumbai Reseller 1") never leak into the final report.

Visual Strategy: Instead of writing code to draw charts, we write a textual justification. We explain that we'd use a Bar Chart for comparing months (to see trends clearly) and a Donut Chart for April's category breakdown (to see part-to-whole relationships).

Part 4: The Conductor (Agentic Workflow & Mock Runner)
The Goal: Wire Parts 1, 2, and 3 together into a single, automated Python script (mock_agent_runner.py) that acts like an AI analyst running a monthly routine.

The Intake & Guardrail: The script starts by pointing validate_feed (from Part 2) at the current month's CSV. If it's the corrupted file, it triggers a "Hard Stop" and immediately outputs the validation errors.

The Analysis: If the feed is valid, it calculates the MoM growth for every category and checks their flag status.

The Anti-Spam Filter (Sorting & Capping): It takes all the flagged categories and sorts them by the biggest percentage change. To prevent spamming the manager, it takes only the top 3 and uses the Part 3 template to draft a narrative message for them.

The Output Generation: Any flagged category beyond the top 3 is logged as "suppressed".
 Finally, it bundles the status, the errors, the drafted messages, 
 and the suppressed list into a single, clean JSON object.


THE OVERALL STRUCTURE IS:

MEESHO
├── data/
│   ├── generate_dataset.py
│   ├── resellers.csv
│   ├── orders.csv
│   └── meesho_reseller.db
├── part1_sql/
│   ├── queries.sql
│   └── output/
│       └── <generated CSV files from part 1>
├── part2_engine/
│   ├── growth_engine.py
│   ├── test_growth_engine.py
│   └── fixtures/
│       ├── april.csv
│       ├── may.csv
│       ├── june.csv
│       └── corrupted_feed.csv
├── part3_ai_narrative/
│   ├── prompt_pack.md
│   ├── narrative_report.md
│   └── masking.py
├── part4_agent/
│   ├── agent_spec.md
│   └── mock_agent_runner.py
└── README.md


Finally The pipeline flow is:

Raw Data is summarized by SQL
(Part 1) -> passed to Python math/validation 
(Part 2) -> converted to text via Markdown Templates 
(Part 3) -> managed and output as JSON by the Agent Runner (Part 4).