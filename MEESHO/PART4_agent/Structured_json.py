{
  "run_month": "String (The current month being analyzed, e.g., 'May')",
  "validation_status": "String (Either 'valid' or 'invalid')",
  "validation_errors": [
    "List of Strings (Contains error messages if invalid, empty [] if valid)"
  ],
  "flagged_categories": [
    {
      "category": "String (e.g., 'Ethnic Wear')",
      "mom_pct": "Float (e.g., 77.1)",
      "previous_revenue": "Float (e.g., 104520.77)",
      "current_revenue": "Float (e.g., 185107.61)",
      "drafted": "Boolean (true)",
      "message": "String (The final drafted stakeholder narrative)"
    }
  ],
  "suppressed_categories": [
    "List of Strings (Category names that were flagged but exceeded the top-3 cap)"
  ],
  "escalated_categories": [
    "List of Strings (Category names that hit exactly the 8.0% boundary)"
  ],
  "action_taken": "String (Either 'drafted_and_held_for_approval' or 'hard_stop')"
}