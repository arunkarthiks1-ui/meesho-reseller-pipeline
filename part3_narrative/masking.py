def alias_for(reseller_id: str) -> str:
    """Converts a reseller ID (e.g., 'RS019') into a privacy alias (e.g., 'ALIAS-19')."""
    if reseller_id.startswith("RS"):
        return f"ALIAS-{reseller_id[2:].lstrip('0')}"
    return f"ALIAS-{reseller_id}"


def assert_no_raw_names_leak(text: str, reseller_names: list[str]) -> bool:
    """Returns False if any raw reseller name appears inside text, True otherwise."""
    for name in reseller_names:
        if name in text:
            return False
    return True


if __name__ == "__main__":
    # Internal Unit Tests for Privacy Protection
    assert alias_for("RS019") == "ALIAS-19"
    assert alias_for("RS005") == "ALIAS-5"

    test_names = ["Mumbai Reseller 1", "Lucknow Reseller 6"]
    clean_text = "Top seller in West region (ALIAS-19) generated INR 75,295.09."
    leaky_text = "Top seller Mumbai Reseller 1 generated INR 75,295.09."

    assert assert_no_raw_names_leak(clean_text, test_names) is True
    assert assert_no_raw_names_leak(leaky_text, test_names) is False

    print("✓ All Part 3 Privacy Masking unit tests passed successfully!")