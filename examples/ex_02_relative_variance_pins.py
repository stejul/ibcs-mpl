import matplotlib.pyplot as plt
from ibcs_mpl.charts.pins import RelativeVariancePinChart
from ibcs_mpl.types import ScenarioCode, ReferenceScenario

chart = RelativeVariancePinChart(
    title="Sales variance",
    subtitle="ΔPY% (monthly)",
    categories=["Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"],
    rel_variance_pct=[-8.0, 5.0, 2.5, -3.0, 0.0, 7.2, -1.1, 4.0],
    minuend_scenario=ScenarioCode.AC,
    reference_scenario=ReferenceScenario.PY,
    title_top_pad=0.06,
    title_subtitle_gap=0.05
)

fig, ax = plt.subplots(figsize=(8.6, 3.2))
chart.draw(ax)
plt.tight_layout()
plt.show()
