import csv
import json
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from part4_agent.mock_agent_runner import run


def setup_temp_month_csvs():
    """Extracts isolated monthly CSVs matching Part 2 validation headers."""
    os.makedirs("part4_agent/temp_fixtures", exist_ok=True)
    months = ["April", "May", "June"]

    # Read original monthly category revenue CSV
    source_file = "part1_sql/output/monthly_category_revenue.csv"
    if not os.path.exists(source_file):
        source_file = "part2_engine/fixtures/monthly_category_revenue.csv"

    for m in months:
        records = []
        with open(source_file, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames or []
            
            for row in reader:
                # Match month if month column exists, otherwise take rows as-is
                if "month" in row and row["month"] != m:
                    continue
                records.append(row)

        if records:
            out_path = f"part4_agent/temp_fixtures/{m.lower()}.csv"
            with open(out_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(records)


def test_part4():
    setup_temp_month_csvs()

    # Scenario 1: May Run (April -> May)
    may_run = run(
        "May",
        "April",
        "part4_agent/temp_fixtures/april.csv",
        "part4_agent/temp_fixtures/may.csv",
    )
    
    # Debug print if validation fails
    if may_run["validation_status"] != "valid":
        print("Validation errors in May run:", may_run["validation_errors"])
        
    assert may_run["validation_status"] == "valid"
    assert may_run["action_taken"] == "drafted_and_held_for_approval"
    assert len(may_run["flagged_categories"]) == 3

    may_order = [x["category"] for x in may_run["flagged_categories"]]
    assert may_order == ["Ethnic Wear", "Western Wear", "Kids Wear"]
    assert may_run["flagged_categories"][0]["mom_pct"] == 77.1
    assert sorted(may_run["suppressed_categories"]) == [
        "Beauty & Personal Care",
        "Home & Kitchen",
    ]
    assert may_run["escalated_categories"] == []
    print("✓ Scenario 1 (May Run) Passed Perfectly!")

    # Scenario 2: June Run (May -> June)
    june_run = run(
        "June",
        "May",
        "part4_agent/temp_fixtures/may.csv",
        "part4_agent/temp_fixtures/june.csv",
    )
    assert june_run["validation_status"] == "valid"
    assert len(june_run["flagged_categories"]) == 3

    june_order = [x["category"] for x in june_run["flagged_categories"]]
    assert june_order == ["Ethnic Wear", "Home & Kitchen", "Kids Wear"]
    assert june_run["flagged_categories"][0]["mom_pct"] == -58.74
    assert june_run["suppressed_categories"] == ["Western Wear"]
    assert june_run["escalated_categories"] == []
    print("✓ Scenario 2 (June Run) Passed Perfectly!")

    # Scenario 3: Corrupted Feed Run
    corrupt_run = run(
        "May",
        "April",
        "part4_agent/temp_fixtures/april.csv",
        "part2_engine/fixtures/corrupted_feed.csv",
    )
    assert corrupt_run["validation_status"] == "invalid"
    assert corrupt_run["action_taken"] == "hard_stop"
    assert corrupt_run["flagged_categories"] == []
    assert corrupt_run["suppressed_categories"] == []
    assert len(corrupt_run["validation_errors"]) > 0
    print("✓ Scenario 3 (Corrupted Feed Hard Stop) Passed Perfectly!")

    print("\nALL PART 4 ACCEPTANCE CRITERIA PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_part4()