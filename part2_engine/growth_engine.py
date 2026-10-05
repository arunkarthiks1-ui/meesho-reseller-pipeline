import csv
import os


def mom_growth(previous: float, current: float) -> float:
    """Computes Month-on-Month growth percentage rounded to 2 decimals."""
    if previous == 0:
        return 0.0
    growth = ((current - previous) / previous) * 100
    return round(growth, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    """Evaluates MoM percentage against a threshold."""
    abs_val = abs(mom_pct)
    if abs_val == threshold:
        return "escalate_exact_boundary"
    elif abs_val > threshold:
        return "flagged"
    else:
        return "not_flagged"


def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
    """Validates input CSV feed for data integrity errors."""
    errors = []

    if not os.path.exists(csv_path):
        return False, [f"File not found: {csv_path}"]

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=2):
            month = row.get("month", "").strip()
            category = row.get("category", "").strip()
            revenue_raw = row.get("revenue", "").strip()

            try:
                rev_val = float(revenue_raw) if revenue_raw != "" else None
                if rev_val is not None and rev_val < 0:
                    errors.append(
                        f"Line {idx}: negative revenue ({rev_val}) for category={category}"
                    )
            except ValueError:
                pass

            if not category:
                errors.append(f"line {idx}: missing category (month {month})")

            if revenue_raw == "":
                errors.append(f"line {idx}: missing revenue (category {category})")
            else:
                try:
                    float(revenue_raw)
                except ValueError:
                    errors.append(f"line {idx}: revenue not numeric: {revenue_raw!r}")

    if errors:
        return False, errors
    return True, []