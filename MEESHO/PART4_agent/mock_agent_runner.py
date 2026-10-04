import csv
import json
import os
import sys
from pathlib import Path

# --- DYNAMIC PROJECT ROOT SETUP ---
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent if SCRIPT_DIR.name == "part4_agent" else SCRIPT_DIR

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# --- IMPORT PART 2 ENGINE FUNCTIONS ---
try:
    import part2_engine.growth_engine as ge
    validate_feed = ge.validate_feed
    is_flagged = ge.is_flagged

    # Map the MoM calculation function name dynamically
    if hasattr(ge, 'mom_growth'):
        calculate_mom = ge.mom_growth
    elif hasattr(ge, 'calculate_mom'):
        calculate_mom = ge.calculate_mom
    elif hasattr(ge, 'compute_mom'):
        calculate_mom = ge.compute_mom
    else:
        raise AttributeError("Could not find a MoM calculation function in growth_engine.py")

except Exception as e:
    print(f"Error importing growth_engine: {e}")
    sys.exit(1)


def get_month_from_filename(filename: str) -> str:
    """Extracts a clean month name from a filename like 'april.csv'."""
    basename = os.path.basename(filename)
    return basename.split('.')[0].capitalize()


def load_revenue_data(csv_path: str) -> dict:
    """Loads CSV into a dictionary of {category: revenue}."""
    data = {}
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('category') and row.get('revenue'):
                data[row['category']] = float(row['revenue'])
    return data


def apply_template(category: str, month: str, previous_month: str, mom_pct: float) -> str:
    """Applies Part 3 Narrative prompt-pack template."""
    direction = "Growth" if mom_pct > 0 else "Decline"
    return (
        f"Context: Measurement of month-over-month revenue performance for {category} "
        f"comparing {month} against {previous_month}.\n"
        f"Insight: The category experienced an extreme {abs(mom_pct)}% {direction} ({mom_pct}%).\n"
        f"Implication: This performance deviation requires immediate review by the category manager."
    )


def run(month: str, previous_month_csv: str, current_month_csv: str) -> dict:
    """
    Executes the 8-step mock agent planner:
    1. Validate feed
    2. Hard Stop if invalid
    3. Compute MoM growth
    4. Check flag status
    5. Sort flagged descending by abs(mom_pct)
    6. Draft messages for top 3
    7. Suppress remaining flagged
    7b. Escalate exact boundaries
    8. Return structured JSON dict
    """
    # 1 & 2. Load and Validate current feed (Guardrail check)
    is_valid, validation_errors = validate_feed(current_month_csv)

    if not is_valid:
        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": validation_errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop"
        }

    # 3. Compute MoM growth for all categories
    prev_data = load_revenue_data(previous_month_csv)
    curr_data = load_revenue_data(current_month_csv)

    analyzed_categories = []

    for category, curr_rev in curr_data.items():
        if category in prev_data:
            prev_rev = prev_data[category]
            mom_pct = calculate_mom(prev_rev, curr_rev)

            # 4. Check flag status
            status = is_flagged(mom_pct)

            analyzed_categories.append({
                "category": category,
                "mom_pct": mom_pct,
                "previous_revenue": prev_rev,
                "current_revenue": curr_rev,
                "status": status
            })

    # 5. Sort flagged categories descending by absolute magnitude
    flagged = [cat for cat in analyzed_categories if cat["status"] == "flagged"]
    flagged.sort(key=lambda x: abs(x["mom_pct"]), reverse=True)

    # 6 & 7. Cap drafts at top 3, suppress the rest
    top_3 = flagged[:3]
    suppressed = flagged[3:]

    # 7b. Log exact boundary escalations
    escalated = [
        cat["category"] for cat in analyzed_categories
        if cat["status"] == "escalate_exact_boundary"
    ]

    previous_month_name = get_month_from_filename(previous_month_csv)
    drafted_list = []

    for item in top_3:
        message = apply_template(
            category=item["category"],
            month=month,
            previous_month=previous_month_name,
            mom_pct=item["mom_pct"]
        )

        drafted_list.append({
            "category": item["category"],
            "mom_pct": item["mom_pct"],
            "previous_revenue": item["previous_revenue"],
            "current_revenue": item["current_revenue"],
            "drafted": True,
            "message": message
        })

    suppressed_list = [item["category"] for item in suppressed]

    # 8. Return structured dict
    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": drafted_list,
        "suppressed_categories": suppressed_list,
        "escalated_categories": escalated,
        "action_taken": "drafted_and_held_for_approval"
    }


def ensure_fixtures_exist(fixtures_dir: Path):
    """Auto-generates fixture CSV files matching the exact Part 2 dataset if missing."""
    fixtures_dir.mkdir(parents=True, exist_ok=True)

    fixtures = {
        "april.csv": "category,revenue\nBeauty & Personal Care,40737.01\nEthnic Wear,104520.77\nHome & Kitchen,100446.23\nKids Wear,59847.27\nWestern Wear,113866.15\n",
        "may.csv": "category,revenue\nBeauty & Personal Care,35542.11\nEthnic Wear,185107.61\nHome & Kitchen,91152.57\nKids Wear,45793.78\nWestern Wear,86998.18\n",
        "june.csv": "category,revenue\nBeauty & Personal Care,37559.07\nEthnic Wear,76371.53\nHome & Kitchen,129971.22\nKids Wear,56737.78\nWestern Wear,97415.64\n",
        "corrupted_feed.csv": "category,revenue\nBeauty & Personal Care,-1000\nEthnic Wear,\n,50000\n"
    }

    for filename, content in fixtures.items():
        file_path = fixtures_dir / filename
        if not file_path.exists():
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)


if __name__ == "__main__":
    fixtures_dir = PROJECT_ROOT / "part2_engine" / "fixtures"
    ensure_fixtures_exist(fixtures_dir)

    april_csv = str(fixtures_dir / "april.csv")
    may_csv = str(fixtures_dir / "may.csv")
    june_csv = str(fixtures_dir / "june.csv")
    corrupt_csv = str(fixtures_dir / "corrupted_feed.csv")

    print("=== MAY SCENARIO ===")
    print(json.dumps(run("May", april_csv, may_csv), indent=2))

    print("\n=== JUNE SCENARIO ===")
    print(json.dumps(run("June", may_csv, june_csv), indent=2))

    print("\n=== CORRUPTED FEED SCENARIO ===")
    print(json.dumps(run("June", may_csv, corrupt_csv), indent=2))