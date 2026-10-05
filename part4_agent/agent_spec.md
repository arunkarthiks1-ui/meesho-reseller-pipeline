# Part 4 — Agentic Specification (`agent_spec.md`)

## 1. Five Core Agentic Components

- **Goal**: Keep Meesho category managers informed of any category whose month-on-month revenue moves beyond the 8.0% threshold, with a human approving every message before it goes out.
- **Tools**:
  - `part2_engine.growth_engine.validate_feed`: Pre-ingestion validation of CSV feeds.
  - `part2_engine.growth_engine.mom_growth`: Precision calculation of Month-on-Month revenue change.
  - `part2_engine.growth_engine.is_flagged`: Evaluates growth against the 8.0% threshold (`flagged`, `not_flagged`, `escalate_exact_boundary`).
  - `part3_narrative.prompt_pack`: Fills executive update templates using verified Part 1/Part 2 metrics.
- **Memory/State**: The agent maintains the prior month's revenue per category to evaluate MoM growth against the current month's feed during execution.
- **Planner**: An ordered 8-step execution workflow (see Section 2).
- **Feedback Loop**: A mandatory human-approval checkpoint (`drafted_and_held_for_approval`) where all generated draft messages are held for human review before any dispatch occurs.

---

## 2. Guardrails & System Stopping Conditions

### Guardrails
- **Input Guardrail**: `validate_feed` must pass with zero errors before any analytical or growth computation begins.
- **Action Guardrail**: Messages are never auto-sent; every drafted message is assigned `drafted = True` and held for human approval.
- **Output Guardrail**: Every numeric value in a drafted update must trace back directly to validated Part 1 / Part 2 figures (no hallucinated values allowed).

### Stopping Conditions
- **Success Condition**: Input feed passes validation, growth is evaluated, top flagged updates are drafted and held (or zero drafts if no category crosses the threshold), and a structured JSON payload is emitted.
- **Error Condition (Hard Stop)**: If `validate_feed` fails, execution halts immediately with `action_taken = "hard_stop"`, surfacing all feed errors and preventing any growth calculations or message drafting.

---

## 3. Ordered Subtasks (Planner Sequence)

1. **Load & Validate**: Ingest the monthly revenue feed and execute `validate_feed`.
2. **Hard Stop Check**: If invalid, trigger a Hard Stop and report all detected error strings.
3. **Compute MoM Growth**: If valid, compute `mom_growth` for each category against the previous month.
4. **Evaluate Flag Status**: Run `is_flagged` on every category.
5. **Rank Flagged Items**: Sort all flagged categories in descending order of `abs(mom_pct)`.
6. **Cap & Draft**: Generate a draft message using the Part 3 template for at most the top 3 flagged categories to prevent notification flooding.
7. **Handle Overflow & Boundaries**:
   - Log any remaining flagged categories beyond the top 3 as suppressed (`suppressed_categories`).
   - Log any category returning `escalate_exact_boundary` into `escalated_categories` without drafting.
8. **Emit JSON Payload**: Output one structured JSON object summarizing the run results.

---

## 4. Given-When-Then Agent Specs

### Spec 1: Standard MoM Calculation & Flagging
- **Given** revenue for Ethnic Wear in April is INR 104,520.77 and in May is INR 185,107.61,
- **When** the agent computes `mom_growth` and evaluates `is_flagged`,
- **Then** `mom_pct` equals `77.10` and `is_flagged` evaluates to `"flagged"`.

### Spec 2: Unflagged Category Baseline
- **Given** revenue for Beauty & Personal Care in May is INR 125,400.00 and in June is INR 132,510.00,
- **When** the agent evaluates MoM growth (+5.67%),
- **Then** `is_flagged` returns `"not_flagged"`, and the category appears in neither `flagged_categories` nor `suppressed_categories`.

### Spec 3: Exact Boundary Escalation
- **Given** a category's MoM growth evaluates to exactly `8.00%` or `-8.00%`,
- **When** `is_flagged` runs on the category,
- **Then** `is_flagged` evaluates to `"escalate_exact_boundary"`, and the category is placed into `escalated_categories` without drafting a message.

### Spec 4: Corrupted Feed Hard Stop
- **Given** an incoming CSV feed containing negative revenue values, unparseable floats, or missing categories,
- **When** the agent executes `validate_feed`,
- **Then** `validate_feed` returns `False`, execution triggers a Hard Stop (`action_taken = "hard_stop"`), all error strings are surfaced, and no growth calculation or message drafting is attempted.