import csv
import json
import os
import sys

# Add project root to sys.path to allow absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from part2_engine.growth_engine import is_flagged, mom_growth, validate_feed


def load_revenue_csv(filepath: str) -> list[dict]:
    """Utility to read monthly category revenue CSV into a list of dicts."""
    records = []
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return records


def parse_revenue(row: dict) -> float:
    """Safely extracts revenue from either 'revenue' or 'total_revenue' column."""
    val = row.get("revenue") or row.get("total_revenue") or row.get("monthly_revenue")
    return float(val) if val is not None else 0.0


def draft_message(
    category: str,
    prev_month: str,
    curr_month: str,
    prev_rev: float,
    curr_rev: float,
    mom_pct: float,
) -> str:
    """Fills the Part 3 template for stakeholder updates."""
    direction = "an increase" if mom_pct >= 0 else "a drop"
    return (
        f"Context: Revenue performance update for {category} comparing {curr_month} against {prev_month}.\n"
        f"Insight: Revenue moved from INR {prev_rev:,.2f} in {prev_month} to INR {curr_rev:,.2f} in {curr_month}, "
        f"representing {direction} of {mom_pct}% Month-on-Month (Fact).\n"
        f"Implication: Operational review recommended for {category} to align supply capacity and marketing spend (Hypothesis)."
    )


def run(
    run_month: str,
    prev_month_name: str,
    previous_month_csv: str,
    current_month_csv: str,
) -> dict:
    """Executes the 8-step agentic workflow subtask sequence."""
    # Subtask 1: Validate input feed
    is_valid, validation_errors = validate_feed(current_month_csv)

    # Subtask 2: Hard Stop if feed is invalid
    if not is_valid:
        output = {
            "run_month": run_month,
            "validation_status": "invalid",
            "validation_errors": validation_errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop",
        }
        return output

    # Load data if feed is valid using flexible parse_revenue helper
    prev_records = load_revenue_csv(previous_month_csv)
    curr_records = load_revenue_csv(current_month_csv)

    prev_data = {r["category"]: parse_revenue(r) for r in prev_records}
    curr_data = {r["category"]: parse_revenue(r) for r in curr_records}

    flagged_candidates = []
    suppressed_categories = []
    escalated_categories = []

    # Subtasks 3 & 4: Compute MoM growth and evaluate flag status
    for category, curr_rev in curr_data.items():
        prev_rev = prev_data[category]
        pct = mom_growth(prev_rev, curr_rev)
        flag_status = is_flagged(pct)

        # Subtask 7b: Exact boundary escalation
        if flag_status == "escalate_exact_boundary":
            escalated_categories.append(category)
        elif flag_status == "flagged":
            flagged_candidates.append(
                {
                    "category": category,
                    "mom_pct": pct,
                    "previous_revenue": prev_rev,
                    "current_revenue": curr_rev,
                }
            )

    # Subtask 5: Sort flagged categories by abs(mom_pct) descending
    flagged_candidates.sort(key=lambda x: abs(x["mom_pct"]), reverse=True)

    # Subtasks 6 & 7: Cap at top 3, draft messages, and mark overflow as suppressed
    flagged_categories = []
    for idx, item in enumerate(flagged_candidates):
        if idx < 3:
            msg = draft_message(
                item["category"],
                prev_month_name,
                run_month,
                item["previous_revenue"],
                item["current_revenue"],
                item["mom_pct"],
            )
            flagged_categories.append(
                {
                    "category": item["category"],
                    "mom_pct": item["mom_pct"],
                    "previous_revenue": item["previous_revenue"],
                    "current_revenue": item["current_revenue"],
                    "drafted": True,
                    "message": msg,
                }
            )
        else:
            suppressed_categories.append(item["category"])

    # Subtask 8: Emit structured JSON object
    output = {
        "run_month": run_month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": flagged_categories,
        "suppressed_categories": suppressed_categories,
        "escalated_categories": escalated_categories,
        "action_taken": "drafted_and_held_for_approval",
    }
    return output


if __name__ == "__main__":
    print("Executing Mock Agent Runner direct test...")