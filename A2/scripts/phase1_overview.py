"""
Phase 1: Dataset Overview
Produces: results/phase1_overview.json

Computes shape, distributions, data quality, and structural summaries
of the Boston residential real estate dataset.
"""
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "A2_EDA_Residential.csv"
OUT_PATH  = Path(__file__).parent.parent / "results" / "phase1_overview.json"


def load_rows():
    with open(DATA_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def price_histogram(rows):
    """Bucket sale prices into $500K-wide bins, cap at $10M."""
    bucket_size = 500_000
    n_buckets = 20
    counts = [0] * n_buckets
    for r in rows:
        try:
            p = float(r["price"])
            if 0 < p < bucket_size * n_buckets:
                counts[int(p // bucket_size)] += 1
        except (ValueError, KeyError):
            pass
    labels = [f"${i*500}K–${(i+1)*500}K" for i in range(n_buckets)]
    return {"labels": labels, "counts": counts, "bucket_size_usd": bucket_size}


def annual_summary(rows):
    """Median price and transaction count per year."""
    by_year = defaultdict(list)
    for r in rows:
        try:
            y = int(r["year"])
            p = float(r["price"])
            if p > 0:
                by_year[y].append(p)
        except (ValueError, KeyError):
            pass
    years = sorted(by_year)
    return {
        "years":  years,
        "counts": [len(by_year[y]) for y in years],
        "median": [statistics.median(by_year[y]) for y in years],
    }


def style_price_per_sqft(rows):
    """Median price-per-sqft and sale count by building style."""
    by_style = defaultdict(list)
    for r in rows:
        try:
            p  = float(r["price"])
            sf = float(r["intersf"])
            s  = r["style"].strip()
            if p > 50_000 and sf > 100 and s:
                by_style[s].append(p / sf)
        except (ValueError, KeyError):
            pass
    result = []
    for style, vals in sorted(by_style.items(), key=lambda x: -statistics.median(x[1])):
        if len(vals) >= 50:
            result.append({
                "style":      style,
                "median_psf": round(statistics.median(vals), 2),
                "count":      len(vals),
            })
    return result


def construction_era(rows):
    """Median price and count by 20-year construction era."""
    era_prices = defaultdict(list)
    for r in rows:
        try:
            yb = int(r["yearbuilt"])
            p  = float(r["price"])
            if p > 0 and 1800 <= yb <= 2022:
                era = (yb // 20) * 20
                era_prices[era].append(p)
        except (ValueError, KeyError):
            pass
    result = []
    for era in sorted(era_prices):
        vals = era_prices[era]
        result.append({
            "era":    f"{era}s",
            "range":  f"{era}–{era+19}",
            "median": round(statistics.median(vals)),
            "count":  len(vals),
        })
    return result


def data_quality(rows):
    """Count missing and zero values for key fields."""
    fields = {
        "price":      {"note": "Complete; 1 record = $999,999,999 (likely data error)"},
        "intersf":    {"note": "Zero-sqft records excluded from $/sqft analyses"},
        "bedrooms":   {"note": "Many condos legitimately coded as 0-bedroom studios"},
        "bathrooms":  {"note": "Similar pattern to bedrooms"},
        "yearbuilt":  {"note": "~3% of records lack construction year"},
        "lat":        {"note": "Un-geocoded records excluded from geographic analyses"},
        "lon":        {"note": "Un-geocoded records excluded from geographic analyses"},
        "zip":        {"note": "Complete; 38 unique ZIP codes"},
    }
    result = {}
    for col, meta in fields.items():
        missing = sum(1 for r in rows if not r.get(col, "").strip())
        zero    = sum(1 for r in rows if r.get(col, "").strip() == "0")
        result[col] = {"missing": missing, "zero": zero, "note": meta["note"]}
    return result


def bedroom_distribution(rows):
    counts = defaultdict(int)
    for r in rows:
        try:
            b = int(float(r["bedrooms"]))
            if 0 <= b <= 10:
                counts[b] += 1
        except (ValueError, KeyError):
            pass
    beds = sorted(counts)
    return {"bedrooms": beds, "counts": [counts[b] for b in beds]}


def main():
    rows = load_rows()
    out = {
        "total_rows":           len(rows),
        "price_histogram":      price_histogram(rows),
        "annual_summary":       annual_summary(rows),
        "style_price_per_sqft": style_price_per_sqft(rows),
        "construction_era":     construction_era(rows),
        "data_quality":         data_quality(rows),
        "bedroom_distribution": bedroom_distribution(rows),
    }
    OUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Saved → {OUT_PATH}")
    print(f"  Total rows:    {out['total_rows']:,}")
    print(f"  Year range:    {out['annual_summary']['years'][0]}–{out['annual_summary']['years'][-1]}")
    print(f"  Styles w/ data:{len(out['style_price_per_sqft'])}")


if __name__ == "__main__":
    main()
