"""
ex_15 — ScatterChart and BubbleChart

Demonstrates:
- ScatterChart: IBCS-styled scatter with scenario notation
- BubbleChart: scatter with a third dimension encoded as bubble size
Both with optional quadrant reference lines and point labels.
"""
import matplotlib.pyplot as plt

from ibcs_mpl.charts.scatter import BubbleChart, ScatterChart
from ibcs_mpl.types import ScenarioCode

PRODUCTS = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta"]

# Scatter: revenue vs. margin for AC and PY
scatter_ac = ScatterChart(
    title="Revenue vs Margin — AC",
    subtitle="by product (mEUR / %)",
    x_values=[420, 310, 580, 195, 740, 280],
    y_values=[18.2, 12.5, 22.1, 9.8, 25.4, 11.3],
    labels=PRODUCTS,
    scenario=ScenarioCode.AC,
    x_label="Revenue (mEUR)",
    y_label="Margin %",
    show_quadrants=True,
)

scatter_py = ScatterChart(
    title="Revenue vs Margin — PY",
    subtitle="by product (mEUR / %)",
    x_values=[390, 335, 555, 210, 700, 260],
    y_values=[16.8, 13.2, 20.5, 11.1, 23.8, 12.0],
    labels=PRODUCTS,
    scenario=ScenarioCode.PY,
    x_label="Revenue (mEUR)",
    y_label="Margin %",
    show_quadrants=True,
)

# Bubble: revenue vs. margin, sized by headcount
bubble = BubbleChart(
    title="Revenue · Margin · Headcount",
    subtitle="bubble size = headcount",
    x_values=[420, 310, 580, 195, 740, 280],
    y_values=[18.2, 12.5, 22.1, 9.8, 25.4, 11.3],
    size_values=[520, 310, 840, 180, 1200, 290],
    labels=PRODUCTS,
    scenario=ScenarioCode.AC,
    x_label="Revenue (mEUR)",
    y_label="Margin %",
    size_label="Headcount",
    show_quadrants=True,
    size_scale=600,
)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5.5))
scatter_ac.draw(ax1)
scatter_py.draw(ax2)
bubble.draw(ax3)

fig.suptitle("ScatterChart (AC, PY) · BubbleChart — portfolio family", fontsize=10, y=1.01)
plt.tight_layout()
plt.show()
