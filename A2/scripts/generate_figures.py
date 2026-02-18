"""
Figure Generator
Produces: results/figures.js

Builds all 13 report figures using the Python plotly library, exports each as
a JSON spec (data + layout), and bundles them into a JS file. report.html loads
the bundle and calls Plotly.newPlot() so charts remain fully interactive.

Usage:
    python scripts/generate_figures.py
    (or via: python scripts/run_all.py)
"""
import json
import math
from pathlib import Path

import plotly.graph_objects as go

RESULTS_DIR = Path(__file__).parent.parent / "results"
OUT_PATH    = RESULTS_DIR / "figures.js"

# ── Colour palette (matches report.html) ────────────────────────────────────
C = dict(
    bg     = "#111114",
    surf   = "#17171c",
    grid   = "#1e1e24",
    text   = "#E8E6E1",
    muted  = "#6b6b78",
    amber  = "#F5A623",
    teal   = "#2DD4BF",
    purple = "#A78BFA",
    rose   = "#FB7185",
    sky    = "#38BDF8",
    green  = "#4ADE80",
)

ZIP_NAMES = {
    "2108": "Beacon Hill",          "2109": "N. End / Waterfront",
    "2110": "Financial District",   "2111": "Downtown / Chinatown",
    "2113": "North End",            "2114": "Beacon Hill / W. End",
    "2115": "Fenway / Mission Hill","2116": "Back Bay / South End",
    "2118": "South End / Roxbury",  "2199": "Back Bay Luxury",
    "2210": "Seaport / S. Boston",  "2215": "Brighton / Allston",
}

PAL5 = [C["sky"], C["amber"], C["purple"], C["teal"], C["rose"]]


# ── Helpers ──────────────────────────────────────────────────────────────────
def dollar_ticks(max_val, n_ticks=5):
    """Return tickvals/ticktext dicts with human-readable dollar labels."""
    raw_step = max_val / n_ticks
    mag  = 10 ** math.floor(math.log10(raw_step))
    step = next(
        (f * mag for f in [1, 2, 2.5, 5, 10] if max_val / (f * mag) <= n_ticks + 1),
        mag * 10,
    )
    vals = []
    v = 0
    while v <= max_val * 1.1:
        vals.append(round(v))
        v += step

    def fmt(v):
        if v == 0:
            return "$0"
        if v >= 1_000_000:
            return f"${int(v/1e6)}M" if v % 1_000_000 == 0 else f"${v/1e6:.1f}M"
        return f"${v/1e3:.0f}K"

    return dict(tickvals=vals, ticktext=[fmt(v) for v in vals])


def axis(**kw):
    base = dict(gridcolor=C["grid"], zerolinecolor=C["grid"],
                tickfont=dict(color=C["text"], size=12))
    base.update(kw)
    return base


def title_font(text):
    return dict(text=text, font=dict(color=C["text"], size=11), standoff=12)


BASE = dict(
    paper_bgcolor=C["bg"],
    plot_bgcolor =C["bg"],
    font   =dict(family="'JetBrains Mono', monospace", color=C["text"], size=12),
    margin =dict(t=20, b=52, l=72, r=24),
    xaxis  =axis(),
    yaxis  =axis(),
    legend =dict(font=dict(size=12, color=C["text"]), bgcolor="rgba(0,0,0,0)",
                 orientation="h", x=0, y=-0.18),
    hoverlabel=dict(bgcolor="#1d1d26", bordercolor=C["amber"],
                    font=dict(family="'JetBrains Mono', monospace",
                              color=C["text"], size=12),
                    namelength=-1),
)


def base_layout(**overrides):
    """Merge BASE with per-chart overrides (shallow)."""
    layout = dict(BASE)
    layout.update(overrides)
    return layout


def load_data():
    bundle = {}
    for key, fname in [
        ("phase1", "phase1_overview.json"),
        ("q1",     "phase2_investors.json"),
        ("q2",     "phase2_flips.json"),
        ("q3",     "phase2_cash.json"),
    ]:
        with open(RESULTS_DIR / fname) as f:
            bundle[key] = json.load(f)
    return bundle


def export(fig):
    """Return {data, layout} dict from a Plotly Figure."""
    raw = json.loads(fig.to_json())
    return {"data": raw["data"], "layout": raw["layout"]}


# ── Figure generators ────────────────────────────────────────────────────────

def fig1_price_hist(d):
    hist = d["phase1"]["price_histogram"]
    labels, counts = hist["labels"], hist["counts"]
    n = len(labels)
    colors = [
        C["amber"] if i < 2 else
        "rgba(245,166,35,0.75)" if i < 4 else
        "rgba(245,166,35,0.45)"
        for i in range(n)
    ]
    tick_vals = [labels[i] for i in range(0, n, 4)]

    fig = go.Figure(go.Bar(
        x=labels, y=counts,
        marker=dict(color=colors, line=dict(color="rgba(0,0,0,0)")),
        hovertemplate="<b>%{x}</b><br><b>%{y:,}</b> sales<extra></extra>",
    ))
    fig.update_layout(**base_layout(
        margin=dict(t=20, b=100, l=72, r=24),
        xaxis=axis(tickangle=-40, tickfont=dict(color=C["text"], size=11),
                   tickvals=tick_vals, ticktext=tick_vals,
                   title=dict(text="Sale Price Range", font=dict(color=C["text"], size=11), standoff=12)),
        yaxis=axis(tickformat=",.0f", tickfont=dict(color=C["text"], size=12),
                   title=dict(text="Transactions", font=dict(color=C["text"], size=11), standoff=12)),
    ))
    return export(fig)


def fig2_yr_overview(d):
    ann = d["phase1"]["annual_summary"]
    dt  = dollar_ticks(max(ann["median"]))

    fig = go.Figure([
        go.Bar(
            x=ann["years"], y=ann["counts"], name="Sales Volume", yaxis="y2",
            marker=dict(color="rgba(56,189,248,0.15)",
                        line=dict(color="rgba(56,189,248,0.45)", width=1)),
            hovertemplate="<b>%{x}</b> — %{y:,} sales<extra></extra>",
        ),
        go.Scatter(
            x=ann["years"], y=ann["median"],
            mode="lines+markers", name="Median Price",
            line=dict(color=C["amber"], width=3),
            marker=dict(color=C["amber"], size=7),
            fill="tozeroy", fillcolor="rgba(245,166,35,0.07)",
            hovertemplate="<b>%{x}</b> — median $%{y:,.0f}<extra></extra>",
        ),
    ])
    fig.update_layout(**base_layout(
        margin=dict(t=30, b=52, l=80, r=72),
        shapes=[
            dict(type="line", x0=2008, x1=2008, yref="paper", y0=0, y1=1,
                 line=dict(color=C["rose"], width=1.5, dash="dot")),
            dict(type="line", x0=2020, x1=2020, yref="paper", y0=0, y1=1,
                 line=dict(color=C["purple"], width=1.5, dash="dot")),
        ],
        annotations=[
            dict(x=2008, text="Financial Crisis", yref="paper", y=1.06,
                 showarrow=False, font=dict(color=C["rose"], size=11), xanchor="center"),
            dict(x=2020, text="COVID-19", yref="paper", y=1.06,
                 showarrow=False, font=dict(color=C["purple"], size=11), xanchor="center"),
        ],
        xaxis =axis(dtick=2, tickfont=dict(color=C["text"], size=12)),
        yaxis =axis(**dt, title=title_font("Median Sale Price")),
        yaxis2=dict(overlaying="y", side="right", gridcolor="rgba(0,0,0,0)",
                    showgrid=False, tickfont=dict(color=C["text"], size=12),
                    title=title_font("Annual Sales")),
        legend={**BASE["legend"], "y": -0.14},
    ))
    return export(fig)


def fig3_style_psf(d):
    rows = sorted(d["phase1"]["style_price_per_sqft"], key=lambda r: r["median_psf"])
    pal  = [C["muted"], "rgba(245,166,35,0.4)", C["green"], C["sky"],
            C["rose"], C["purple"], C["teal"], C["amber"], C["amber"]]

    fig = go.Figure(go.Bar(
        y=[r["style"] for r in rows],
        x=[r["median_psf"] for r in rows],
        orientation="h",
        marker=dict(color=pal[:len(rows)], line=dict(color="rgba(0,0,0,0)")),
        customdata=[r["count"] for r in rows],
        text=[f'${round(r["median_psf"])}/sqft' for r in rows],
        textposition="outside",
        textfont=dict(color=C["text"], size=12),
        hovertemplate="<b>%{y}</b><br>$%{x:,.0f}/sqft<br>%{customdata:,} sales<extra></extra>",
        name="",
    ))
    fig.update_layout(**base_layout(
        margin=dict(t=20, b=52, l=120, r=100),
        xaxis=axis(title=title_font("Median $/sqft"), range=[0, 1000]),
        yaxis=axis(tickfont=dict(color=C["text"], size=12)),
        showlegend=False,
        bargap=0.3,
    ))
    return export(fig)


def fig4_era(d):
    eras = d["phase1"]["construction_era"]
    dt   = dollar_ticks(max(e["median"] for e in eras))

    fig = go.Figure(go.Scatter(
        x=[e["era"] for e in eras],
        y=[e["median"] for e in eras],
        mode="lines+markers",
        name="Median Price",
        line=dict(color=C["teal"], width=3),
        marker=dict(
            color=[C["amber"] if e["count"] > 5000 else C["teal"] for e in eras],
            size=[max(8, math.sqrt(e["count"] / 20) + 4) for e in eras],
            line=dict(color=C["bg"], width=2),
        ),
        fill="tozeroy", fillcolor="rgba(45,212,191,0.07)",
        customdata=[[e["count"], e.get("range", "")] for e in eras],
        hovertemplate="<b>%{x}</b> (%{customdata[1]})<br>Median: $%{y:,.0f}<br>n=%{customdata[0]:,}<extra></extra>",
    ))
    fig.update_layout(**base_layout(
        margin=dict(t=20, b=52, l=80, r=24),
        xaxis=axis(tickfont=dict(color=C["text"], size=12)),
        yaxis=axis(**dt, title=title_font("Median Sale Price")),
        showlegend=False,
    ))
    return export(fig)


def fig5_investor_area(d):
    comp    = d["q1"]["annual_composition"]
    palette = {"Non-investor": C["sky"], "Small": C["amber"], "Medium": C["purple"],
               "Large": C["teal"], "Institutional": C["rose"]}
    fills   = {"Non-investor": "rgba(56,189,248,0.28)", "Small": "rgba(245,166,35,0.28)",
               "Medium": "rgba(167,139,250,0.28)", "Large": "rgba(45,212,191,0.28)",
               "Institutional": "rgba(251,113,133,0.28)"}

    traces = [
        go.Scatter(
            x=comp["years"], y=comp["types"][name]["pct"],
            name=name, mode="lines",
            stackgroup="one",
            line=dict(color=palette[name], width=2),
            fillcolor=fills[name],
            hovertemplate=f"<b>{name}</b>: %{{y:.1f}}%<extra></extra>",
        )
        for name in ["Non-investor", "Small", "Medium", "Large", "Institutional"]
    ]

    fig = go.Figure(traces)
    fig.update_layout(**base_layout(
        margin=dict(t=20, b=70, l=72, r=24),
        xaxis=axis(dtick=2, tickfont=dict(color=C["text"], size=12)),
        yaxis=axis(ticksuffix="%", range=[0, 100],
                   title=title_font("Share of Annual Purchases"), dtick=20),
        legend={**BASE["legend"], "y": -0.2},
    ))
    return export(fig)


def fig6_inv_price(d):
    rows = sorted(d["q1"]["price_by_type"], key=lambda r: r["median"])
    dt   = dollar_ticks(max(r["median"] for r in rows))

    fig = go.Figure(go.Bar(
        y=[r["type"] for r in rows],
        x=[r["median"] for r in rows],
        orientation="h",
        marker=dict(color=PAL5[:len(rows)], line=dict(color="rgba(0,0,0,0)")),
        customdata=[r["count"] for r in rows],
        text=[
            f'${r["median"]/1e6:.2f}M' if r["median"] >= 1e6 else f'${r["median"]/1e3:.0f}K'
            for r in rows
        ],
        textposition="outside",
        textfont=dict(color=C["text"], size=13),
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Median: $%{x:,.0f}<br>n=%{customdata:,}<extra></extra>",
        name="",
    ))
    max_median = max(r["median"] for r in rows)
    fig.update_layout(**base_layout(
        margin=dict(t=20, b=52, l=130, r=100),
        xaxis=axis(**dt, title=title_font("Median Purchase Price"),
                   range=[0, max_median * 1.32]),
        yaxis=axis(tickfont=dict(color=C["text"], size=13)),
        showlegend=False,
        bargap=0.3,
    ))
    return export(fig)


def fig7_inv_corr(d):
    pts = d["q1"]["investor_share_vs_price"]
    dt  = dollar_ticks(max(p["median_price"] for p in pts))

    fig = go.Figure(go.Scatter(
        x=[p["investor_pct"] for p in pts],
        y=[p["median_price"] for p in pts],
        mode="markers+text",
        text=[str(p["year"]) for p in pts],
        textposition="top center",
        textfont=dict(color=C["muted"], size=11, family="'JetBrains Mono', monospace"),
        marker=dict(color=C["amber"], size=11, opacity=0.9,
                    line=dict(color=C["bg"], width=2)),
        customdata=[p["total_sales"] for p in pts],
        hovertemplate=(
            "<b>%{text}</b><br>Investor share: %{x:.1f}%<br>"
            "Median price: $%{y:,.0f}<br>Sales: %{customdata:,}<extra></extra>"
        ),
        name="",
    ))
    fig.update_layout(**base_layout(
        margin=dict(t=28, b=60, l=80, r=24),
        xaxis=axis(ticksuffix="%", title=title_font("Investor Share of Purchases (%)")),
        yaxis=axis(**dt, title=title_font("Median Sale Price")),
        showlegend=False,
    ))
    return export(fig)


def fig8_flip_yr(d):
    fr = d["q2"]["annual_flip_rate"]

    fig = go.Figure([
        go.Bar(
            x=fr["years"], y=fr["flips"], name="Flip Count", yaxis="y2",
            marker=dict(color="rgba(251,113,133,0.2)",
                        line=dict(color="rgba(251,113,133,0.55)", width=1)),
            hovertemplate="<b>%{x}</b> — %{y} flips<extra></extra>",
        ),
        go.Scatter(
            x=fr["years"], y=fr["rate"],
            mode="lines+markers", name="Flip Rate %",
            line=dict(color=C["rose"], width=3),
            marker=dict(color=C["rose"], size=7),
            hovertemplate="<b>%{x}</b> — %{y:.2f}% flip rate<extra></extra>",
        ),
    ])
    fig.update_layout(**base_layout(
        margin=dict(t=20, b=52, l=64, r=64),
        xaxis =axis(dtick=2, tickfont=dict(color=C["text"], size=12)),
        yaxis =axis(ticksuffix="%", title=title_font("Flip Rate (%)")),
        yaxis2=dict(overlaying="y", side="right", gridcolor="rgba(0,0,0,0)",
                    showgrid=False, tickfont=dict(color=C["text"], size=12),
                    title=title_font("Annual Flip Count")),
        legend={**BASE["legend"], "y": -0.14},
    ))
    return export(fig)


def fig9_flip_profit(d):
    dist = d["q2"]["profit_distribution"]
    labels, lo, counts = dist["labels"], dist["bucket_lo"], dist["counts"]
    colors = [
        "rgba(251,113,133,0.65)" if b < 0 else
        C["amber"] if b < 20 else
        "rgba(74,222,128,0.7)"
        for b in lo
    ]
    max_idx  = counts.index(max(counts))
    tick_vals = [labels[i] for i in range(0, len(labels), 3)]

    fig = go.Figure(go.Bar(
        x=labels, y=counts,
        marker=dict(color=colors, line=dict(color="rgba(0,0,0,0)")),
        hovertemplate="<b>%{x}</b><br>%{y} flips<extra></extra>",
        name="",
    ))
    fig.update_layout(**base_layout(
        margin=dict(t=32, b=80, l=64, r=24),
        xaxis=axis(tickangle=-35, tickfont=dict(color=C["muted"], size=11),
                   tickvals=tick_vals, ticktext=tick_vals),
        yaxis=axis(title=title_font("Number of Flips")),
        showlegend=False,
        annotations=[dict(
            x=labels[max_idx], y=counts[max_idx],
            text="Peak: 0–10% gain",
            showarrow=True, ax=70, ay=-44,
            font=dict(color=C["amber"], size=12),
            arrowcolor=C["amber"], arrowsize=0.9,
        )],
    ))
    return export(fig)


def fig10_flip_zip(d):
    raw  = d["q2"]["flip_stats_by_zip"]
    data = sorted(
        [dict(name=ZIP_NAMES.get(r["zip"], r["zip"]), rate=r["flip_rate"],
              profit=r["median_profit"], n=r["total"], flips=r["flips"])
         for r in raw],
        key=lambda x: x["rate"],
    )

    fig = go.Figure([
        go.Bar(
            x=[p["rate"] for p in data],
            y=[p["name"] for p in data],
            orientation="h", name="Flip Rate (bars, bottom axis)",
            marker=dict(
                color=[C["rose"] if p["profit"] < 0 else "rgba(245,166,35,0.75)" for p in data],
                line=dict(color="rgba(0,0,0,0)"),
            ),
            customdata=[[p["flips"], p["n"]] for p in data],
            hovertemplate=(
                "<b>%{y}</b><br>Flip rate: %{x:.2f}%<br>"
                "%{customdata[0]} flips of %{customdata[1]:,} sales<extra></extra>"
            ),
        ),
        go.Scatter(
            x=[p["profit"] for p in data],
            y=[p["name"] for p in data],
            mode="markers", name="Median Profit % (dots, top axis)",
            xaxis="x2",
            marker=dict(
                color=[C["rose"] if p["profit"] < 0 else C["green"] for p in data],
                size=13, symbol="diamond",
                line=dict(color=C["bg"], width=2),
            ),
            hovertemplate="<b>%{y}</b><br>Median profit: %{x:.2f}%<extra></extra>",
        ),
    ])
    fig.update_layout(**base_layout(
        margin=dict(t=44, b=60, l=180, r=60),
        xaxis =axis(ticksuffix="%", title=title_font("← Flip Rate (%)"), range=[0, 7]),
        xaxis2=dict(overlaying="x", side="top", ticksuffix="%",
                    tickfont=dict(color=C["text"], size=12),
                    gridcolor="rgba(0,0,0,0)", showgrid=False,
                    title=title_font("Median Flip Profit (%) →"),
                    range=[-5, 20]),
        yaxis =axis(tickfont=dict(color=C["text"], size=12)),
        legend={**BASE["legend"], "y": -0.16},
        bargap=0.25,
    ))
    return export(fig)


def fig11_cash_yr(d):
    ac = d["q3"]["annual_cash_rate"]

    fig = go.Figure([
        go.Bar(
            x=ac["years"], y=ac["cash"], name="Cash Sales (count)", yaxis="y2",
            marker=dict(color="rgba(167,139,250,0.2)",
                        line=dict(color="rgba(167,139,250,0.55)", width=1)),
            hovertemplate="<b>%{x}</b> — %{y:,} cash sales<extra></extra>",
        ),
        go.Scatter(
            x=ac["years"], y=ac["rate"],
            mode="lines+markers", name="Cash Rate (%)",
            line=dict(color=C["purple"], width=3),
            marker=dict(color=C["purple"], size=7),
            hovertemplate="<b>%{x}</b> — %{y:.1f}% cash<extra></extra>",
        ),
    ])
    fig.update_layout(**base_layout(
        margin=dict(t=36, b=52, l=68, r=72),
        xaxis =axis(dtick=2, tickfont=dict(color=C["text"], size=12)),
        yaxis =axis(ticksuffix="%", range=[0, 55],
                    title=title_font("Cash Sale Rate (%)"), dtick=10),
        yaxis2=dict(overlaying="y", side="right", gridcolor="rgba(0,0,0,0)",
                    showgrid=False, tickfont=dict(color=C["text"], size=12),
                    title=title_font("Cash Count")),
        shapes=[dict(type="rect", x0=2008, x1=2014, yref="paper", y0=0, y1=1,
                     fillcolor="rgba(167,139,250,0.05)", line=dict(width=0))],
        annotations=[dict(x=2011, text="Post-crisis surge: 2008–2014",
                          yref="paper", y=0.97, showarrow=False,
                          font=dict(color=C["purple"], size=11), xanchor="center")],
        legend={**BASE["legend"], "y": -0.14},
    ))
    return export(fig)


def fig12_cash_inv(d):
    rows = sorted(d["q3"]["cash_rate_by_investor_type"], key=lambda r: r["rate"])
    non_inv_rate = next((r["rate"] for r in rows if r["type"] == "Non-investor"), 0)

    fig = go.Figure(go.Bar(
        y=[r["type"] for r in rows],
        x=[r["rate"] for r in rows],
        orientation="h",
        marker=dict(color=PAL5[:len(rows)], line=dict(color="rgba(0,0,0,0)")),
        customdata=[r["total"] for r in rows],
        text=[f'{r["rate"]:.1f}%' for r in rows],
        textposition="outside",
        textfont=dict(color=C["text"], size=13),
        hovertemplate="<b>%{y}</b><br>%{x:.1f}% cash<br>n=%{customdata:,}<extra></extra>",
        name="",
    ))
    fig.update_layout(**base_layout(
        margin=dict(t=32, b=52, l=130, r=80),
        xaxis=axis(ticksuffix="%", range=[0, 70],
                   title=title_font("Cash Purchase Rate (%)"), dtick=10),
        yaxis=axis(tickfont=dict(color=C["text"], size=13)),
        showlegend=False,
        bargap=0.3,
        shapes=[dict(type="line", x0=non_inv_rate, x1=non_inv_rate,
                     yref="paper", y0=0, y1=1,
                     line=dict(color=C["sky"], width=1.5, dash="dot"))],
        annotations=[dict(x=non_inv_rate, text="Non-investor baseline",
                          yref="paper", y=1.06, showarrow=False,
                          font=dict(color=C["sky"], size=11),
                          xanchor="left", xshift=5)],
    ))
    return export(fig)


def fig13_cash_zip(d):
    raw  = sorted(d["q3"]["cash_rate_by_zip"], key=lambda r: r["rate"])
    names = [ZIP_NAMES.get(r["zip"], r["zip"]) for r in raw]
    rates = [r["rate"] for r in raw]

    def grad_color(v):
        t = min(v / 70, 1.0)
        r = min(round(167 + t * 84), 255)
        g = max(round(139 - t * 26), 0)
        b = max(round(250 - t * 117), 0)
        return f"rgba({r},{g},{b},0.82)"

    fig = go.Figure(go.Bar(
        x=rates, y=names,
        orientation="h",
        marker=dict(color=[grad_color(v) for v in rates], line=dict(color="rgba(0,0,0,0)")),
        customdata=[r["total"] for r in raw],
        text=[f"{v:.1f}%" for v in rates],
        textposition="outside",
        textfont=dict(color=C["text"], size=13),
        hovertemplate=(
            "<b>%{y}</b><br>%{x:.1f}% cash purchases<br>"
            "%{customdata:,} total sales<extra></extra>"
        ),
        name="",
    ))
    fig.update_layout(**base_layout(
        margin=dict(t=20, b=52, l=190, r=72),
        xaxis=axis(ticksuffix="%", range=[0, 80],
                   title=title_font("Cash Purchase Rate (%)"), dtick=10),
        yaxis=axis(tickfont=dict(color=C["text"], size=13)),
        showlegend=False,
        bargap=0.22,
    ))
    return export(fig)


# ── Main ─────────────────────────────────────────────────────────────────────
GENERATORS = [
    ("fig1",  fig1_price_hist),
    ("fig2",  fig2_yr_overview),
    ("fig3",  fig3_style_psf),
    ("fig4",  fig4_era),
    ("fig5",  fig5_investor_area),
    ("fig6",  fig6_inv_price),
    ("fig7",  fig7_inv_corr),
    ("fig8",  fig8_flip_yr),
    ("fig9",  fig9_flip_profit),
    ("fig10", fig10_flip_zip),
    ("fig11", fig11_cash_yr),
    ("fig12", fig12_cash_inv),
    ("fig13", fig13_cash_zip),
]


def main():
    print("Loading analysis data…")
    d = load_data()

    figures = {}
    for key, fn in GENERATORS:
        print(f"  Building {key} ({fn.__name__})…")
        figures[key] = fn(d)

    js  = "// AUTO-GENERATED by generate_figures.py — do not edit by hand\n"
    js += "// Re-generate with: python scripts/generate_figures.py\n"
    js += "const FIGURES = " + json.dumps(figures, separators=(",", ":")) + ";\n"

    RESULTS_DIR.mkdir(exist_ok=True)
    with open(OUT_PATH, "w") as f:
        f.write(js)

    size_kb = OUT_PATH.stat().st_size // 1024
    print(f"\nSaved → {OUT_PATH}  ({size_kb} KB)")
    print("Open report.html in a browser.")


if __name__ == "__main__":
    main()
