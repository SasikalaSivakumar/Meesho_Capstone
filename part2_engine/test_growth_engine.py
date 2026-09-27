from pathlib import Path

from growth_engine import mom_growth, is_flagged, validate_feed


BASE_DIR = Path(__file__).resolve().parent
FIXTURES = BASE_DIR / "fixtures"


# Test 1: April → May Ethnic Wear
growth = mom_growth(104520.77, 185107.61)
assert growth == 77.1
assert is_flagged(growth) == "flagged"


# Test 2: May → June Beauty & Personal Care
growth = mom_growth(35542.11, 37559.07)
assert growth == 5.67
assert is_flagged(growth) == "not_flagged"


# Test 3: Exact 8% boundary
growth = mom_growth(100000, 108000)
assert growth == 8.0
assert is_flagged(growth) == "escalate_exact_boundary"


# Test 4: Corrupted feed
result, errors = validate_feed(
    str(FIXTURES / "corrupted_feed.csv")
)

assert result is False

assert errors == [
    "line 3: negative revenue (-4200.0) for category=Western Wear",
    "line 4: missing category (month=July)",
    "line 6: missing revenue (category=Home & Kitchen)",
]


# Test 5: Valid Part 1 feed
result, errors = validate_feed(
    str(FIXTURES / "monthly_category_revenue.csv")
)

assert result is True
assert errors == []


print("All tests passed!")

# Full May vs April MoM checks

may_vs_april = {
    "Ethnic Wear": (104520.77, 185107.61, 77.1, "flagged"),
    "Western Wear": (113866.15, 86998.18, -23.6, "flagged"),
    "Kids Wear": (59847.27, 45793.78, -23.48, "flagged"),
    "Home & Kitchen": (100446.23, 91152.57, -9.25, "flagged"),
    "Beauty & Personal Care": (40737.01, 35542.11, -12.75, "flagged"),
}

for category, (previous, current, expected_growth, expected_status) in may_vs_april.items():
    growth = mom_growth(previous, current)
    assert growth == expected_growth
    assert is_flagged(growth) == expected_status


# Full June vs May MoM checks

june_vs_may = {
    "Ethnic Wear": (185107.61, 76371.53, -58.74, "flagged"),
    "Western Wear": (86998.18, 97415.64, 11.97, "flagged"),
    "Kids Wear": (45793.78, 56737.78, 23.9, "flagged"),
    "Home & Kitchen": (91152.57, 129971.22, 42.59, "flagged"),
    "Beauty & Personal Care": (35542.11, 37559.07, 5.67, "not_flagged"),
}

for category, (previous, current, expected_growth, expected_status) in june_vs_may.items():
    growth = mom_growth(previous, current)
    assert growth == expected_growth
    assert is_flagged(growth) == expected_status


print("Full MoM tables passed!")