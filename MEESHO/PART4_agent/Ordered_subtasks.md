Ordered Subtasks (The Agent Planner)

The agent executes the following deterministic sequence to process the monthly revenue feed:

Load & Validate: Load the current month's revenue feed CSV and execute the validate_feed tool.

Guardrail Check (Hard Stop): If validation is invalid, initiate a Hard Stop, report the explicit validation errors, and skip all subsequent steps.

Compute Growth: If valid, calculate the mom_growth (Month-on-Month percentage) for every category by comparing current revenue against the previous month's revenue.

Determine Flag Status: Run the is_flagged tool on every computed mom_pct to categorize them as "flagged", "not_flagged", or "escalate_exact_boundary".

Sort: Sort all "flagged" categories in descending order based on the absolute magnitude of their mom_pct (abs(mom_pct)).

Draft Messages (Capped): Fill the Part 3 narrative template to draft a stakeholder message for at most the top 3 flagged categories by magnitude. (This hard cap prevents notification-flooding).

Suppress Overflow: Log any remaining "flagged" categories that exceeded the top-3 cap as "suppressed, review manually", ensuring no messages are drafted for them.

7b. Escalate Exact Boundaries: Separately log any category that returned "escalate_exact_boundary" into an escalated_categories list without drafting a message (ensuring threshold edge-cases are neither falsely flagged nor silently dropped).

Emit JSON: Output the final execution state as a single structured JSON object.