"""
ex_12 — Indicator framework

Demonstrates all six indicator types:
- DifferenceMarker: Δ bracket between two data points
- TrendArrow: directional arrow between two points
- ScalingLine: horizontal reference line for shared scale
- ScalingArea: shaded scale band
- OutlierIndicator: break mark at clipped axis edge
- ReferenceArrowhead: arrowhead marker at reference values
"""
import matplotlib.pyplot as plt

from ibcs_mpl.charts import SingleColumnChart, GroupedColumnChart
from ibcs_mpl.indicators import (
    DifferenceMarker,
    OutlierIndicator,
    ReferenceArrowhead,
    ScalingArea,
    ScalingLine,
    TrendArrow,
)
from ibcs_mpl.types import ScenarioCode

CATS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
VALUES = [420, 380, 510, 490, 560, 530]

fig, axes = plt.subplots(2, 3, figsize=(15, 8))
fig.suptitle("Indicator framework", fontsize=11, y=0.99)

# --- DifferenceMarker ---
ax = axes[0, 0]
chart = SingleColumnChart(title="DifferenceMarker", subtitle="Δ between Jan and Jun",
                           categories=CATS, values=VALUES)
chart.draw(ax)
DifferenceMarker(x=5.6, y1=VALUES[0], y2=VALUES[-1], bracket_width=0.12).draw(ax)

# --- TrendArrow ---
ax = axes[0, 1]
chart = SingleColumnChart(title="TrendArrow", subtitle="upward trend annotation",
                           categories=CATS, values=VALUES)
chart.draw(ax)
TrendArrow(x1=0, y1=VALUES[0] + 30, x2=5, y2=VALUES[-1] + 30,
           scenario=ScenarioCode.AC, linewidth=1.8).draw(ax)

# --- ScalingLine + ScalingArea ---
ax = axes[0, 2]
chart = SingleColumnChart(title="ScalingLine + ScalingArea", subtitle="scale reference band",
                           categories=CATS, values=VALUES)
chart.draw(ax)
ScalingArea(y_low=400, y_high=550).draw(ax)
ScalingLine(y=500, label="target").draw(ax)

# --- OutlierIndicator ---
ax = axes[1, 0]
clipped = [420, 380, 510, 490, 750, 530]  # 750 will be clipped
chart = SingleColumnChart(title="OutlierIndicator", subtitle="bar 5 clipped at 650",
                           categories=CATS, values=clipped)
chart.draw(ax)
ax.set_ylim(top=650)
OutlierIndicator(positions=[4], direction="top").draw(ax)

# --- ReferenceArrowhead ---
ax = axes[1, 1]
ref_values = [410, 375, 495, 480, 545, 515]
chart = GroupedColumnChart(
    title="ReferenceArrowhead",
    subtitle="arrowhead at PY values",
    categories=CATS,
    primary_values=VALUES,
    reference_values=ref_values,
)
chart.draw(ax)
ReferenceArrowhead(
    positions=list(range(len(CATS))),
    values=ref_values,
    scenario=ScenarioCode.PY,
).draw(ax)

# --- Combined: ScalingLine + DifferenceMarker ---
ax = axes[1, 2]
chart = SingleColumnChart(title="Combined indicators", subtitle="target line + Δ marker",
                           categories=CATS, values=VALUES)
chart.draw(ax)
ScalingLine(y=480, label="budget").draw(ax)
DifferenceMarker(x=1.6, y1=480, y2=VALUES[1], bracket_width=0.1).draw(ax)

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()
