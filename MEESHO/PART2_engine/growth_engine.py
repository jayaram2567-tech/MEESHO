import csv


def mom_growth(previous: float, current: float) -> float:
  """Calculates Month-on-Month (MoM) growth percentage rounded to 2 decimal places."""
  if previous == 0:
    raise ValueError("Previous month revenue cannot be zero for MoM growth.")
  growth = ((current - previous) / previous) * 100
  return round(growth, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
  """Determines if MoM growth triggers a flag, no-flag, or boundary escalation.

  Returns:
      "flagged": if abs(mom_pct) > threshold
      "not_flagged": if abs(mom_pct) < threshold
      "escalate_exact_boundary": if abs(mom_pct) == threshold
  """
  abs_mom = abs(mom_pct)
  if abs_mom > threshold:
    return "flagged"
  elif abs_mom < threshold:
    return "not_flagged"
  else:
    return "escalate_exact_boundary"


def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
  """Validates CSV data against guardrail rules line-by-line.

  Header is Line 1; data starts at Line 2.
  Returns (True, []) if no errors, else (False, list_of_errors).
  """
  errors = []

  with open(csv_path, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader, None)  # Line 1: Header

    for line_num, row in enumerate(reader, start=2):
      if not row:
        continue

      month = row[0].strip() if len(row) > 0 else ""
      category = row[1].strip() if len(row) > 1 else ""
      revenue_str = row[2].strip() if len(row) > 2 else ""

      # Check 1: Missing category
      if not category:
        errors.append(f"line {line_num}: missing category (month={month})")
      # Check 2: Missing revenue
      elif not revenue_str:
        errors.append(
            f"line {line_num}: missing revenue (category={category})"
        )
      # Check 3 & 4: Numeric parse and non-negative check
      else:
        try:
          revenue_val = float(revenue_str)
          if revenue_val < 0:
            errors.append(
                f"line {line_num}: negative revenue ({revenue_val}) for"
                f" category={category}"
            )
        except ValueError:
          errors.append(
              f"line {line_num}: revenue not numeric: {revenue_str!r}"
          )

  is_valid = len(errors) == 0
  return is_valid, errors



import csv
import os


def export_growth_report(input_csv_path: str, output_csv_path: str):
  """Reads the monthly category revenue CSV, calculates MoM growth and flag status

  for each category across months, and exports the final report to a new CSV
  file.
  """
  # Step 1: Validate input feed first using your validate_feed function
  is_valid, errors = validate_feed(input_csv_path)
  if not is_valid:
    print(f"Validation failed for {input_csv_path}. Please fix these errors:")
    for err in errors:
      print(f"  - {err}")
    return False

  # Step 2: Read rows from input CSV
  rows = []
  with open(input_csv_path, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
      rows.append(row)

  # Step 3: Group data by category to track previous month revenue chronologically
  category_data = {}
  for row in rows:
    cat = row["category"].strip()
    month = row["month"].strip()
    revenue = float(row["revenue"])

    if cat not in category_data:
      category_data[cat] = []
    category_data[cat].append((month, revenue, row))

  output_rows = []

  # Define chronological month mapping for correct sorting
  month_order = {"April": 1, "May": 2, "June": 3, "July": 4}

  # Step 4: Calculate MoM growth and flag status for each category
  for cat, records in category_data.items():
    # Sort records by month order (April -> May -> June)
    records_sorted = sorted(records, key=lambda x: month_order.get(x[0], 0))

    prev_revenue = None
    for month, revenue, original_row in records_sorted:
      if prev_revenue is None:
        # First month has no previous month data for comparison
        mom_pct = "N/A"
        flag_status = "N/A"
      else:
        # Using your mom_growth and is_flagged functions
        mom_pct = mom_growth(prev_revenue, revenue)
        flag_status = is_flagged(mom_pct)

      # Build output dictionary
      out_row = {
          "month": month,
          "category": cat,
          "revenue": revenue,
          "previous_revenue": prev_revenue if prev_revenue is not None else "",
          "mom_pct": mom_pct,
          "flag_status": flag_status,
      }
      output_rows.append(out_row)
      prev_revenue = revenue

  # Step 5: Ensure output directory exists
  os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

  # Step 6: Write results to output CSV file
  fieldnames = [
      "month",
      "category",
      "revenue",
      "previous_revenue",
      "mom_pct",
      "flag_status",
  ]
  with open(output_csv_path, mode="w", newline="", encoding="utf-8") as out_file:
    writer = csv.DictWriter(out_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output_rows)

  print(f"Growth report successfully exported to: {output_csv_path}")
  return True