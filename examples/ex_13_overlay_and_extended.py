"""
ex_13 — Overlay and Extended chart composition

Demonstrates:
- draw_overlay: two charts sharing a primary axis (with twin y-axis)
- draw_extended: multi-panel continuation with break markers
- shared_ylim: scale governance across extended panels
"""
import matplotlib.pyplot as plt

from ibcs_mpl.charts import LineChart, SingleColumnChart
from ibcs_mpl.charts.lines import ScenarioLineSeries
from ibcs_mpl.composites.overlay import ExtendedLayout, draw_extended, draw_overlay
from ibcs_mpl.types import ScenarioCode

# ── Overlay: columns + line on twin y-axis ─────────────────────────────────
CATS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
col_chart = SingleColumnChart(
    title="Revenue + Margin overlay",
    subtitle="Revenue (mEUR) | Margin % (right axis)",
    categories=CATS,
    values=[420, 380, 510, 490, 560, 530],
    scenario=ScenarioCode.AC,
)
line_chart = LineChart(
    title="",
    categories=CATS,
    series=[
        ScenarioLineSeries(
            label="Margin %",
            values=[18.2, 15.1, 21.3, 20.5, 23.4, 22.1],
            scenario=ScenarioCode.AC,
        )
    ],
)

fig1, ax1 = plt.subplots(figsize=(9, 4.5))
ax1, ax2 = draw_overlay(ax1, col_chart, line_chart, twin_axis="x")
ax2.set_ylabel("Margin %", fontsize=9)
ax2.tick_params(axis="y", labelsize=8)
fig1.suptitle("draw_overlay — columns + line on twin axis", fontsize=10, y=1.01)
plt.tight_layout()

# ── Extended: three time-slice panels with shared y-axis ───────────────────
panels = [
    SingleColumnChart(
        title=f"H{i + 1} {2022 + i}",
        subtitle="Revenue (mEUR)",
        categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        values=[420 + i * 30, 380 + i * 25, 510 + i * 20, 490 + i * 35, 560 + i * 15, 530 + i * 28],
    )
    for i in range(3)
]

fig2 = plt.figure(figsize=(14, 4.5))
axes = draw_extended(
    fig2,
    panels,
    layout=ExtendedLayout(left=0.04, right=0.97, top=0.82, bottom=0.12, gap=0.02, break_marker=True),
    shared_ylim=(300, 700),
)
fig2.suptitle("draw_extended — three panels with shared y-scale and break markers", fontsize=10)

plt.show()
