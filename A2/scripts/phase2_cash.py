"""
Phase 2, Q3: Cash Purchase Analysis
Produces: results/phase2_cash.json

Investigates the prevalence and distribution of all-cash
residential purchases by year, investor type, and ZIP code.
"""
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "A2_EDA_Residential.csv"
OUT_PATH  = Path(__file__).parent.parent / "results" / "phase2_cash.json"

INVESTOR_TYPES = ["Non-investor", "Small", "Medium", "Large", "Institutional"]


def load_rows():
    with open(DATA_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def annual_cash_rate(rows):
    """Cash sale count, total sales, and rate per year."""
    cash_by_year  = defaultdict(int)
    total_by_year = defaultdict(int)

    for r in rows:
        try:
            y = int(r["year"])
            total_by_year[y] += 1
            if r.get("cash_sale") == "1":
                cash_by_year[y] += 1
        except (ValueError, KeyError):
            pass

    years = sorted(total_by_year)
    return {
        "years":  years,
        "cash":   [cash_by_year[y]  for y in years],
        "totals": [total_by_year[y] for y in years],
        "rate":   [
            round(cash_by_year[y] / total_by_year[y] * 100, 2) if total_by_year[y] else 0
            for y in years
        ],
    }


def cash_rate_by_investor_type(rows):
    """Cash rate for each investor type classification."""
    by_type = defaultdict(lambda: {"cash": 0, "total": 0})

    for r in rows:
        inv = r.get("investor_type_purchase", "").strip() or "Non-investor"
        by_type[inv]["total"] += 1
        if r.get("cash_sale") == "1":
            by_type[inv]["cash"] += 1

    return [
        {
            "type":     t,
            "cash":     by_type[t]["cash"],
            "total":    by_type[t]["total"],
            "rate":     round(by_type[t]["cash"] / by_type[t]["total"] * 100, 2)
                        if by_type[t]["total"] else 0,
        }
        for t in INVESTOR_TYPES
    ]


def cash_rate_by_zip(rows, min_sales=200):
    """Cash rate per ZIP code, filtered to meaningful sample sizes."""
    by_zip = defaultdict(lambda: {"cash": 0, "total": 0})

    for r in rows:
        z = r.get("zip", "").strip()
        if not z:
            continue
        by_zip[z]["total"] += 1
        if r.get("cash_sale") == "1":
            by_zip[z]["cash"] += 1

    result = []
    for z, d in by_zip.items():
        if d["total"] < min_sales:
            continue
        result.append({
            "zip":   z,
            "cash":  d["cash"],
            "total": d["total"],
            "rate":  round(d["cash"] / d["total"] * 100, 2) if d["total"] else 0,
        })
    result.sort(key=lambda x: -x["rate"])
    return result


def overall_stats(rows):
    """Top-line cash sale statistics."""
    total = len(rows)
    cash  = sum(1 for r in rows if r.get("cash_sale") == "1")
    return {
        "total_sales": total,
        "cash_sales":  cash,
        "cash_rate":   round(cash / total * 100, 2) if total else 0,
    }


def main():
    rows = load_rows()
    out = {
        "overall_stats":              overall_stats(rows),
        "annual_cash_rate":           annual_cash_rate(rows),
        "cash_rate_by_investor_type": cash_rate_by_investor_type(rows),
        "cash_rate_by_zip":           cash_rate_by_zip(rows),
    }
    OUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2)

    s = out["overall_stats"]
    print(f"Saved → {OUT_PATH}")
    print(f"  Total sales:   {s['total_sales']:,}")
    print(f"  Cash sales:    {s['cash_sales']:,}")
    print(f"  Overall rate:  {s['cash_rate']}%")
    print("  By investor type:")
    for row in out["cash_rate_by_investor_type"]:
        print(f"    {row['type']:20s} {row['rate']:5.1f}%  (n={row['total']:,})")


if __name__ == "__main__":
    main()
