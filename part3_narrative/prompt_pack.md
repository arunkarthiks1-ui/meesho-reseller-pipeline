# Reusable Prompt Pack: Flagged Category Stakeholder Update

## 1. Trigger
A category's `is_flagged` status evaluates to `"flagged"` (Month-on-Month revenue change exceeds the 8.0% threshold).

## 2. Input List
- `{category}`: Category name (e.g., Ethnic Wear)
- `{prev_month}`: Prior month name (e.g., April)
- `{month}`: Current month name (e.g., May)
- `{previous_revenue}`: Previous month's revenue figure in INR
- `{current_revenue}`: Current month's revenue figure in INR
- `{mom_pct}`: Computed MoM growth percentage

## 3. Prompt Template
```text
You are a senior reseller-operations analyst writing a concise update for a regional manager.

Context: Revenue performance for {category} comparing {month} against {prev_month}.
Insight: Revenue moved from INR {previous_revenue} in {prev_month} to INR {current_revenue} in {month}, representing a Month-on-Month change of {mom_pct}% (Fact).
Implication: [Actionable recommendation specific to {category}]. If proposing a cause not directly proven by the data, explicitly label it as a (Hypothesis).

Rules:
- Never state any number that is not one of the provided input variables.
- Maintain a professional Context -> Insight -> Implication structure.