"""
ex_16 — Scale governance and compliance engine

Demonstrates:
- compute_shared_ylim: compute a common y-range across small multiples
- shared_ylim in draw_small_multiples: enforce that range
- find_legend_position: collision-aware legend placement
- ComplianceEngine: IBCS rule checker
- format_report: human-readable compliance output
"""

import matplotlib.pyplot as plt

from ibcs_mpl.annotations import draw_inline_legend, find_legend_position, LegendItem
from ibcs_mpl.charts import GroupedColumnChart, SingleColumnChart
from ibcs_mpl.compliance import ComplianceEngine, format_report
from ibcs_mpl.composites import SmallMultiplesLayout, compute_shared_ylim, draw_small_multiples
from ibcs_mpl.theme import DEFAULT_THEME, scenario_style
from ibcs_mpl.types import ScenarioCode

# ── Scale governance ────────────────────────────────────────────────────────
# Without shared scale, each small multiple auto-scales independently.
# With shared_ylim, they all share the same axis — making cross-chart comparison honest.

COUNTRIES = ["DE", "AT", "CH", "NL", "BE", "PL"]
VALUES_BY_COUNTRY = [
    [42, 48, 51, 55],  # DE — large
    [12, 14, 13, 15],  # AT — small
    [28, 31, 30, 33],  # CH — medium
    [19, 22, 21, 24],  # NL — small-medium
    [8, 9, 11, 10],  # BE — small
    [35, 38, 40, 44],  # PL — medium-large
]

charts = [
    SingleColumnChart(
        title=country,
        subtitle="AC (mEUR)",
        categories=["Q1", "Q2", "Q3", "Q4"],
        values=vals,
    )
    for country, vals in zip(COUNTRIES, VALUES_BY_COUNTRY)
]

# Without shared scale
fig1 = plt.figure(figsize=(14, 5))
draw_small_multiples(fig1, charts, layout=SmallMultiplesLayout(columns=3, top=0.90))
fig1.suptitle("Small multiples — WITHOUT shared scale (misleading!)", fontsize=10, y=0.97)

# With shared scale
fig2 = plt.figure(figsize=(14, 5))
# First draw to collect axes, then compute shared range
temp_fig = plt.figure(figsize=(1, 1))  # throwaway
temp_axes = [temp_fig.add_subplot(1, 1, 1) for _ in charts]
for c, ax in zip(charts, temp_axes):
    c.draw(ax)
ylim = compute_shared_ylim(temp_axes)
plt.close(temp_fig)

draw_small_multiples(
    fig2, charts, layout=SmallMultiplesLayout(columns=3, top=0.90), shared_ylim=ylim
)
fig2.suptitle(
    f"Small multiples — WITH shared scale ylim={ylim[0]:.0f}–{ylim[1]:.0f} (honest!)",
    fontsize=10,
    y=0.97,
)

# ── Legend collision detection ──────────────────────────────────────────────
fig3, ax = plt.subplots(figsize=(8, 4.5))
gc = GroupedColumnChart(
    title="Legend placement — collision-aware",
    subtitle="legend auto-positioned away from data",
    categories=["Q1", "Q2", "Q3", "Q4"],
    primary_values=[44, 52, 49, 56],
    reference_values=[41, 50, 47, 54],
)
gc.draw(ax)

legend_items = [
    LegendItem("AC", scenario_style(DEFAULT_THEME, ScenarioCode.AC)),
    LegendItem("PY", scenario_style(DEFAULT_THEME, ScenarioCode.PY)),
]
lx, ly = find_legend_position(ax, width=0.14, height=0.18)
draw_inline_legend(ax, items=legend_items, x=lx, y=ly)

# ── Compliance engine ───────────────────────────────────────────────────────
engine = ComplianceEngine()

good_chart = SingleColumnChart(
    title="Revenue",
    subtitle="AC (mEUR)",
    categories=["Q1", "Q2"],
    values=[100, 120],
)
bad_chart_no_title = SingleColumnChart(
    title="",
    categories=["Q1", "Q2"],
    values=[100, 120],
)
bad_chart_empty = SingleColumnChart(
    title="Empty chart",
    categories=[],
    values=[],
)

all_charts = [good_chart, bad_chart_no_title, bad_chart_empty]
results = engine.check_all(all_charts)
report = format_report(results)

print("\n" + "=" * 60)
print("IBCS Compliance Report")
print("=" * 60)
print(report)

plt.show()
