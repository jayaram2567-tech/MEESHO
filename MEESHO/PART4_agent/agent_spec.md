Agent Specification
Goal
Keep Meesho category managers informed of any category whose month-on-month revenue moves beyond the 8% threshold, with a human approving every message before it goes out.

Tools

validate_feed: Validates the current month's CSV for missing data and negative values (from Part 2).

mom_growth: Calculates the exact month-over-month growth percentage (from Part 2).

is_flagged: Evaluates if the growth percentage crosses the ±8.0% threshold (from Part 2).

template_fill: Populates the Part 3 Context → Insight → Implication narrative template with verified data.

Memory / State
The agent must remember the previous month's revenue figures for each category to compute the current run's MoM growth, as well as the names of the current and prior months being compared.

Planner
The agent follows a deterministic, 8-step ordered sequence of subtasks (detailed in Section 4.2).

Feedback Loop
A human-approval checkpoint is required before any drafted message is considered "sent". The agent simulates this by outputting a flag marking the payload as "drafted and held for approval", ensuring no automated dispatch happens.

Guardrails

Input Guardrail: validate_feed must pass with exactly zero errors before any computations or drafting steps execute.

Action Guardrail: No message is ever auto-sent; all generated narratives are only drafted and held.

Output Guardrail: Every numeric figure in a drafted message must deterministically trace back to a Part 1 or Part 2 value. The AI is restricted to template-filling to prevent inventing figures.

Stopping Conditions

Success: Drafts are successfully produced (or zero drafts if no category crossed the threshold), with every number traceable to the input dataset.

Error: If validate_feed returns False, the run hits a Hard Stop. It does not silently skip rows; it halts immediately and surfaces the validation errors.

Given-When-Then Specs

GIVEN April→May Ethnic Wear revenue moves from 104520.77 to 185107.61, WHEN the agent evaluates it, THEN it calculates 77.1% growth, flags the category, and drafts an update message.

GIVEN May→June Beauty & Personal Care revenue moves from 35542.11 to 37559.07, WHEN the agent evaluates it, THEN it calculates 5.67% growth, marks it as "not_flagged", and ignores it (no draft, no suppression).

GIVEN a synthetic pair previous=100000, current=108000, WHEN the agent evaluates it, THEN it identifies the growth as exactly 8.0%, logs it as "escalate_exact_boundary" in escalated_categories, and holds it for manual review without drafting a message.

GIVEN the corrupted feed fixture, WHEN the agent runs validate_feed on it, THEN it hits a Hard Stop and returns exactly 3 validation errors (negative revenue, missing category, missing revenue) without computing growth or drafting messages.