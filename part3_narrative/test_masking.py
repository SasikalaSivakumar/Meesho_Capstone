from masking import alias_for, assert_no_raw_names_leak


# Test 1: Alias format
assert alias_for("RS019") == "ALIAS-19"


# Test 2: Raw reseller name must be detected
raw_name_text = "Mumbai Reseller 1 generated strong sales."
assert assert_no_raw_names_leak(
    raw_name_text,
    ["Mumbai Reseller 1"]
) is False


# Test 3: Alias-only text must pass
alias_only_text = "ALIAS-19 generated strong sales."
assert assert_no_raw_names_leak(
    alias_only_text,
    ["Mumbai Reseller 1"]
) is True


# Test 4: Final top-reseller narrative must contain no raw names
final_narrative = """
The Part 1 top-reseller query identified five resellers with total spend above INR 50000.
In the West region, ALIAS-19 recorded INR 75295.09 and ALIAS-22 recorded INR 73882.33.
In the South region, ALIAS-12 recorded INR 69936.46.
In the North region, ALIAS-06 recorded INR 64238.97 and ALIAS-05 recorded INR 61825.02.
"""

reseller_names = [
    "Mumbai Reseller 1",
    "Mumbai Reseller 4",
    "Hyderabad Reseller 6",
    "Lucknow Reseller 6",
    "Jaipur Reseller 5",
]

assert assert_no_raw_names_leak(
    final_narrative,
    reseller_names
) is True


print("All masking tests passed!")