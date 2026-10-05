import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from part4_agent.mock_agent_runner import run


def inspect_scenarios():
    print("==================================================")
    print("SCENARIO 1: MAY RUN (April -> May)")
    print("==================================================")
    may_output = run(
        "May",
        "April",
        "part4_agent/temp_fixtures/april.csv",
        "part4_agent/temp_fixtures/may.csv",
    )
    print(json.dumps(may_output, indent=2))

    print("\n==================================================")
    print("SCENARIO 2: JUNE RUN (May -> June)")
    print("==================================================")
    june_output = run(
        "June",
        "May",
        "part4_agent/temp_fixtures/may.csv",
        "part4_agent/temp_fixtures/june.csv",
    )
    print(json.dumps(june_output, indent=2))

    print("\n==================================================")
    print("SCENARIO 3: CORRUPTED FEED (Hard Stop)")
    print("==================================================")
    corrupt_output = run(
        "May",
        "April",
        "part4_agent/temp_fixtures/april.csv",
        "part2_engine/fixtures/corrupted_feed.csv",
    )
    print(json.dumps(corrupt_output, indent=2))


if __name__ == "__main__":
    inspect_scenarios()