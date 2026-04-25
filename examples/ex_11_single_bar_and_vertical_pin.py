"""
ex_11 — SingleBarChart, VerticalPinChart, scenario triangles

Demonstrates:
- SingleBarChart: structure-axis single series (horizontal)
- VerticalPinChart: structure-axis relative variance pins (horizontal)
- show_reference_triangles=True on GroupedBarChart and GroupedColumnChart
"""
import matplotlib.pyplot as plt

from ibcs_mpl.charts import (
    GroupedBarChart,
    GroupedColumnChart,
    SingleBarChart,
    VerticalPinChart,
)
from ibcs_mpl.types import ReferenceScenario, ScenarioCode

REGIONS = ["North", "South", "East", "West", "Central"]
AC = [820, 650, 740, 910, 580]
PY = [780, 710, 720, 870, 610]
DELTA_PCT = [(a / p - 1) * 100 for a, p in zip(AC, PY)]

single_bar = SingleBarChart(
    title="Revenue by region",
    subtitle="AC (mEUR)",
    categories=REGIONS,
    values=AC,
    scenario=ScenarioCode.AC,
)

vertical_pin = VerticalPinChart(
    title="Revenue variance",
    subtitle="ΔPY%",
    categories=REGIONS,
    rel_variance_pct=DELTA_PCT,
    minuend_scenario=ScenarioCode.AC,
    reference_scenario=ReferenceScenario.PY,
)

grouped_bar_triangles = GroupedBarChart(
    title="Revenue AC vs PY",
    subtitle="with scenario triangles",
    categories=REGIONS,
    primary_values=AC,
    reference_values=PY,
    show_reference_triangles=True,
)

grouped_col_triangles = GroupedColumnChart(
    title="Revenue AC vs PY",
    subtitle="with scenario triangles",
    categories=["Q1", "Q2", "Q3", "Q4"],
    primary_values=[210, 240, 195, 270],
    reference_values=[195, 220, 205, 255],
    show_reference_triangles=True,
)

fig, axes = plt.subplots(2, 2, figsize=(14, 9))
single_bar.draw(axes[0, 0])
vertical_pin.draw(axes[0, 1])
grouped_bar_triangles.draw(axes[1, 0])
grouped_col_triangles.draw(axes[1, 1])

fig.suptitle("SingleBarChart · VerticalPinChart · Scenario triangles", fontsize=11, y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
