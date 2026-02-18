"""
Phase 2, Q1: Investor Activity
Produces: results/phase2_investors.json

Investigates how investor participation has evolved over time
and whether investor buyers pay systematically different prices.
"""
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "A2_EDA_Residential.csv"
OUT_PATH  = Path(__file__).parent.parent / "results" / "phase2_investors.json"

INVESTOR_TYPES = ["Non-investor", "Small", "Medium", "Large", "Institutional"]


def load_rows():
    with open(DATA_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def annual_composition(rows):
    """Count of each investor type per year."""
    by_year = defaultdict(lambda: defaultdict(int))
    for r in rows:
        try:
            y   = int(r["year"])
            inv = r["investor_type_purchase"].strip() or "Non-investor"
            by_year[y][inv] += 1
        except (ValueError, KeyError):
            pass

    years = sorted(by_year)
    totals = [sum(by_year[y].values()) for y in years]
    result = {
        "years":  years,
        "totals": totals,
        "types":  {},
    }
    for t in INVESTOR_TYPES:
        counts = [by_year[y].get(t, 0) for y in years]
        pct    = [round(c / tot * 100, 2) if tot else 0 for c, tot in zip(counts, totals)]
        result["types"][t] = {"counts": counts, "pct": pct}
    return result


def price_by_type(rows):
    """Median purchase price and count for each investor type."""
    by_type = defaultdict(list)
    for r in rows:
        try:
            p   = float(r["price"])
            inv = r["investor_type_purchase"].strip() or "Non-investor"
            if p > 0:
                by_type[inv].append(p)
        except (ValueError, KeyError):
            pass

    return [
        {
            "type":   t,
            "median": round(statistics.median(by_type[t])) if by_type[t] else None,
            "mean":   round(statistics.mean(by_type[t]))   if by_type[t] else None,
            "count":  len(by_type[t]),
        }
        for t in INVESTOR_TYPES
    ]


def investor_share_vs_price(rows):
    """Per-year: investor share (%) paired with median price — for scatter analysis."""
    annual = annual_composition(rows)
    years   = annual["years"]
    totals  = annual["totals"]
    non_inv = annual["types"]["Non-investor"]["counts"]

    # Re-compute median price per year
    by_year = defaultdict(list)
    for r in rows:
        try:
            y = int(r["year"])
            p = float(r["price"])
            if p > 0:
                by_year[y].append(p)
        except (ValueError, KeyError):
            pass

    return [
        {
            "year":         y,
            "investor_pct": round((1 - non_inv[i] / totals[i]) * 100, 2) if totals[i] else 0,
            "median_price": round(statistics.median(by_year[y])) if by_year[y] else None,
            "total_sales":  totals[i],
        }
        for i, y in enumerate(years)
    ]


def main():
    rows = load_rows()
    out = {
        "annual_composition":       annual_composition(rows),
        "price_by_type":            price_by_type(rows),
        "investor_share_vs_price":  investor_share_vs_price(rows),
    }
    OUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Saved → {OUT_PATH}")
    print("  Price by investor type:")
    for row in out["price_by_type"]:
        print(f"    {row['type']:20s} median=${row['median']:>10,.0f}  n={row['count']:,}")


if __name__ == "__main__":
    main()
