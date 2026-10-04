# Reusable Prompt Pack: Flagged Category Stakeholder Update

## 1. Trigger
The specific condition that initiates this prompt is when a product category's automated monthly evaluation yields an `is_flagged` result of `"flagged"` (indicating significant anomalous month-over-month growth or contraction).

# 2. Input List
* `{category}`: The name of the product category (e.g., "Ethnic Wear").
* `{previous_revenue}`: The total revenue generated in the prior month in INR (e.g., `59000.00`).
* `{current_revenue}`: The total revenue generated in the current month in INR (e.g., `104520.77`).
* `{mom_pct}`: The exact month-over-month percentage change (e.g., `77.1%`).
* `{month}`: The current reporting month (e.g., "May").
* `{prev_month}`: The prior reporting month used for direct comparison (e.g., "April").

## 3. Prompt Template
You are an expert retail analyst writing a concise operational update for a Regional Manager. 

Using ONLY the provided placeholder variables below, generate a professional update following the **Context -> Insight -> Implication** structure. 

**Strict Constraints:**
1. Never state a number or financial figure that is not derived directly from the supplied placeholder variables.
2. Clearly label data-driven statements as facts and analyst interpretations as hypotheses.
3. Keep recommendations strictly actionable—naming specific operational checks rather than vague directives.

### Supplied Data:
- Category: {category}
- Current Month: {month}
- Prior Month: {prev_month}
- Current Revenue: {current_revenue} INR
- Prior Revenue: {previous_revenue} INR
- MoM Growth: {mom_pct}%

## 4. Checklist
Before releasing or publishing the generated narrative, run the following 4 validation checks:
1. **Value Exactness Check**: Does every numerical figure in the draft match a supplied placeholder value exactly without rounding discrepancies or invented metrics?
2. **Fact vs. Hypothesis Labeling**: Is every data-driven statement explicitly labeled as a fact, and every proposed root-cause/recommendation explicitly labeled as a hypothesis?
3. **Actionability Check**: Is the recommendation specific and actionable (naming exact workflows or inventory checks to perform) rather than vague?
4. **Data Privacy Check**: Is any reseller or internal entity referenced exclusively by coded alias or region, ensuring no raw proprietary names leak?