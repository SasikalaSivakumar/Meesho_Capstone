import csv
import json
import sys
from pathlib import Path

# Allow this file to import the Part 2 engine.
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR.parent / "part2_engine"))

from growth_engine import validate_feed, mom_growth, is_flagged


def load_feed(csv_path: str) -> list[dict]:
    """Load a CSV feed into a list of rows."""
    with open(csv_path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def previous_month(month: str) -> str:
    """Return the calendar month immediately before the given month."""
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    index = months.index(month)

    if index == 0:
        return "December"

    return months[index - 1]


def fill_prompt(
    category: str,
    previous_revenue: float,
    current_revenue: float,
    mom_pct: float,
    month: str,
    prev_month: str,
) -> str:
    """
    Part 3 prompt-pack template-fill logic.

    Uses the required Context -> Insight -> Implication structure.
    """
    return (
    f"Context: {category} revenue changed from {prev_month} to {month}. "
    f"Previous revenue: {previous_revenue}. "
    f"Current revenue: {current_revenue}. "
    f"Insight — Fact: {category} recorded a month-on-month change of "
    f"{mom_pct}%. "
    f"Implication — Hypothesis: Review the category's recent performance "
    f"and investigate the factors behind this flagged movement before "
    f"deciding on follow-up action."
)


def run(
    month: str,
    previous_month_csv: str,
    current_month_csv: str,
) -> dict:
    """Run the monitoring agent for one month."""

    # Input guardrail: validate the current feed before processing anything else.
    is_valid, validation_errors = validate_feed(current_month_csv)

    if not is_valid:
        result = {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": validation_errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop",
        }

        print(json.dumps(result, indent=2))
        return result

    current_rows = load_feed(current_month_csv)
    previous_rows = load_feed(previous_month_csv)

    prev_month = previous_month(month)

    current_data = {
        row["category"]: float(row["revenue"])
        for row in current_rows
        if row["month"] == month
    }

    previous_data = {
        row["category"]: float(row["revenue"])
        for row in previous_rows
        if row["month"] == prev_month
    }

    flagged = []
    suppressed = []
    escalated = []

    for category, current_revenue in current_data.items():
        previous_revenue = previous_data[category]

        mom_pct = mom_growth(previous_revenue, current_revenue)
        status = is_flagged(mom_pct)

        item = {
            "category": category,
            "mom_pct": mom_pct,
            "previous_revenue": previous_revenue,
            "current_revenue": current_revenue,
        }

        if status == "flagged":
            flagged.append(item)

        elif status == "escalate_exact_boundary":
            escalated.append(category)

    # Sort by absolute MoM magnitude, largest first.
    flagged.sort(key=lambda item: abs(item["mom_pct"]), reverse=True)

    # Draft only the top 3.
    top_flagged = flagged[:3]
    remaining_flagged = flagged[3:]

    final_flagged = []

    for item in top_flagged:
        message = fill_prompt(
            category=item["category"],
            previous_revenue=item["previous_revenue"],
            current_revenue=item["current_revenue"],
            mom_pct=item["mom_pct"],
            month=month,
            prev_month=prev_month,
        )

        final_flagged.append(
            {
                "category": item["category"],
                "mom_pct": item["mom_pct"],
                "previous_revenue": item["previous_revenue"],
                "current_revenue": item["current_revenue"],
                "drafted": True,
                "message": message,
            }
        )

    for item in remaining_flagged:
        suppressed.append(item["category"])

    result = {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": final_flagged,
        "suppressed_categories": suppressed,
        "escalated_categories": escalated,
        "action_taken": "drafted_and_held_for_approval",
    }

    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    fixtures_dir = BASE_DIR.parent / "part2_engine" / "fixtures"
    valid_csv = str(fixtures_dir / "monthly_category_revenue.csv")
    corrupted_csv = str(fixtures_dir / "corrupted_feed.csv")

    print("=== SCENARIO 1: May (April -> May) ===")
    run("May", valid_csv, valid_csv)

    print("\n=== SCENARIO 2: June (May -> June) ===")
    run("June", valid_csv, valid_csv)

    print("\n=== SCENARIO 3: Corrupted Feed Hard Stop ===")
    run("July", valid_csv, corrupted_csv)