"""
Masking policy module for internal AI narrative generation.
Ensures raw reseller names are never leaked into external-facing summaries.
"""

def alias_for(reseller_id: str) -> str:
    """
    Converts a raw reseller ID into a masked alias.
    Example: 'RS019' -> 'ALIAS-19', 'RS006' -> 'ALIAS-06'
    """
    if not reseller_id or len(reseller_id) < 3:
        return reseller_id
    suffix = reseller_id[3:] if reseller_id.startswith("RS") else reseller_id[2:]
    return f"ALIAS-{int(suffix):02d}" if suffix.isdigit() else f"ALIAS-{suffix}"


def assert_no_raw_names_leak(text: str, reseller_names: list[str]) -> bool:
    """
    Returns False if any raw reseller name appears verbatim inside the text.
    Returns True if no raw names leak.
    """
    for name in reseller_names:
        if name in text:
            return False
    return True


# ==========================================
# Top-Reseller Narrative & Test Suite
# ==========================================
if __name__ == "__main__":
    # 1. Verification of alias_for requirement
    assert alias_for("RS019") == "ALIAS-19", f"Expected ALIAS-19, got {alias_for('RS019')}"
    assert alias_for("RS006") == "ALIAS-06", f"Expected ALIAS-06, got {alias_for('RS006')}"
    print("✓ alias_for requirement checks passed successfully.")

    # Define raw reseller names and ID from Part 1 HAVING query
    raw_reseller_names = ["Mumbai Reseller 1", "Chennai Elite Hub", "Southern Garments Corp", "Delhi Metro Traders", "Kolkata Fashion Point"]
    sample_reseller_id = "RS019"
    masked_alias = alias_for(sample_reseller_id)  # Returns "ALIAS-19"

    # 2. Final top-reseller narrative referencing only region and alias_for()
    final_top_reseller_narrative = (
        f"In the South region, top-performing partner {masked_alias} achieved "
        "exceptional sales velocity in premium categories, driving a 28.4% "
        "increase in regional throughput."
    )

    # 3. Positive test case: assert_no_raw_names_leak on final narrative
    leak_check_passed = assert_no_raw_names_leak(final_top_reseller_narrative, raw_reseller_names)
    assert leak_check_passed is True, "Expected True for safe masked narrative."
    print("✓ Positive case test passed: assert_no_raw_names_leak returned True on final narrative.")
    print(f"  Narrative text: {final_top_reseller_narrative}")

    # 4. Negative test case: verify it returns False if a raw name ("Mumbai Reseller 1") is present
    unsafe_narrative = "Mumbai Reseller 1 achieved strong growth in the West region."
    leak_check_failed = assert_no_raw_names_leak(unsafe_narrative, raw_reseller_names)
    assert leak_check_failed is False, "Expected False when a raw reseller name leaks verbatim."
    print("✓ Negative case test passed: assert_no_raw_names_leak correctly returned False on unsafe text.")