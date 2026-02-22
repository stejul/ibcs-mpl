import matplotlib.pyplot as plt
from ibcs_mpl.charts.columns import SingleColumnChart
from ibcs_mpl.types import ScenarioCode

chart = SingleColumnChart(
    title="Accounts receivable",
    subtitle="Aug..Apr (mUSD)",
    categories=["Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr"],
    values=[653, 1040, 943, 737, 898, 985, 1150, 984, 943],
    scenario=ScenarioCode.AC,
)

fig, ax = plt.subplots(figsize=(8.6, 3.6))
chart.draw(ax)
plt.subplots_adjust(top=0.78)
plt.show()
