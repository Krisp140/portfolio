"""
Phase 2, Q2: Property Flipping
Produces: results/phase2_flips.json

Investigates flip prevalence by year, profit distribution,
and geographic concentration by ZIP code.
"""
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "A2_EDA_Residential.csv"
OUT_PATH  = Path(__file__).parent.parent / "results" / "phase2_flips.json"

# Clamp profit % outliers for distribution analysis
PROFIT_MIN = -100
PROFIT_MAX =  200
BUCKET_SIZE = 10


def load_rows():
    with open(DATA_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def annual_flip_rate(rows):
    """Flip count and rate per year."""
    flips_by_year = defaultdict(int)
    total_by_year = defaultdict(int)
    for r in rows:
        try:
            y = int(r["year"])
            total_by_year[y] += 1
            if r["flip_ind"] == "1":
                flips_by_year[y] += 1
        except (ValueError, KeyError):
            pass

    years = sorted(total_by_year)
    return {
        "years":  years,
        "flips":  [flips_by_year[y] for y in years],
        "totals": [total_by_year[y] for y in years],
        "rate":   [
            round(flips_by_year[y] / total_by_year[y] * 100, 2) if total_by_year[y] else 0
            for y in years
        ],
    }


def profit_distribution(rows):
    """Histogram of flip profit % in BUCKET_SIZE-wide bins."""
    n_buckets = int((PROFIT_MAX - PROFIT_MIN) / BUCKET_SIZE)
    counts    = [0] * n_buckets

    for r in rows:
        if r.get("flip_ind") != "1":
            continue
        try:
            pch = float(r["price_diff_pch"])
            if PROFIT_MIN <= pch < PROFIT_MAX:
                idx = int((pch - PROFIT_MIN) // BUCKET_SIZE)
                counts[idx] += 1
        except (ValueError, KeyError):
            pass

    labels = [
        f"{PROFIT_MIN + i*BUCKET_SIZE}% to {PROFIT_MIN + (i+1)*BUCKET_SIZE}%"
        for i in range(n_buckets)
    ]
    lo = [PROFIT_MIN + i * BUCKET_SIZE for i in range(n_buckets)]
    return {"labels": labels, "bucket_lo": lo, "counts": counts}


def flip_stats_by_zip(rows, min_sales=200):
    """Flip rate and median profit for each ZIP (filtered to min_sales)."""
    by_zip = defaultdict(lambda: {"total": 0, "flips": 0, "profits": []})

    for r in rows:
        z = r.get("zip", "").strip()
        if not z:
            continue
        by_zip[z]["total"] += 1
        if r.get("flip_ind") == "1":
            by_zip[z]["flips"] += 1
            try:
                pch = float(r["price_diff_pch"])
                if PROFIT_MIN <= pch <= 500:
                    by_zip[z]["profits"].append(pch)
            except (ValueError, KeyError):
                pass

    result = []
    for z, d in by_zip.items():
        if d["total"] < min_sales:
            continue
        result.append({
            "zip":           z,
            "total":         d["total"],
            "flips":         d["flips"],
            "flip_rate":     round(d["flips"] / d["total"] * 100, 2),
            "median_profit": round(statistics.median(d["profits"]), 2) if d["profits"] else None,
            "n_profitable":  sum(1 for p in d["profits"] if p > 0),
        })
    result.sort(key=lambda x: -x["flip_rate"])
    return result


def overall_stats(rows):
    """Top-line flip statistics."""
    all_flips   = [r for r in rows if r.get("flip_ind") == "1"]
    profits     = []
    for r in all_flips:
        try:
            pch = float(r["price_diff_pch"])
            if PROFIT_MIN <= pch <= 500:
                profits.append(pch)
        except (ValueError, KeyError):
            pass

    return {
        "total_flips":    len(all_flips),
        "total_sales":    len(rows),
        "flip_rate_pct":  round(len(all_flips) / len(rows) * 100, 2),
        "median_profit":  round(statistics.median(profits), 2) if profits else None,
        "mean_profit":    round(statistics.mean(profits), 2)   if profits else None,
        "pct_profitable": round(sum(1 for p in profits if p > 0) / len(profits) * 100, 1) if profits else None,
        "profit_min":     round(min(profits), 2) if profits else None,
        "profit_max":     round(max(profits), 2) if profits else None,
        "profit_clamp":   {"min": PROFIT_MIN, "max": PROFIT_MAX},
    }


def main():
    rows = load_rows()
    out = {
        "overall_stats":       overall_stats(rows),
        "annual_flip_rate":    annual_flip_rate(rows),
        "profit_distribution": profit_distribution(rows),
        "flip_stats_by_zip":   flip_stats_by_zip(rows),
    }
    OUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2)

    s = out["overall_stats"]
    print(f"Saved → {OUT_PATH}")
    print(f"  Total flips:     {s['total_flips']:,} ({s['flip_rate_pct']}% of sales)")
    print(f"  Median profit:   {s['median_profit']}%")
    print(f"  % profitable:    {s['pct_profitable']}%")
    print(f"  ZIP codes:       {len(out['flip_stats_by_zip'])}")


if __name__ == "__main__":
    main()
