import matplotlib.pyplot as plt

from ibcs_mpl.annotations import CommentRef
from ibcs_mpl.charts import LineChart, ScenarioLineSeries, StackedColumnChart
from ibcs_mpl.titles import MessageBlock, PageTitle


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))

line = LineChart(
    title=PageTitle(
        line1_reporting_unit="Sample Company",
        line2_measure="Share price index",
        line3_context="2026 AC and PY",
    ),
    message=MessageBlock(text="AC trend outperforms PY."),
    categories=["Jan", "Feb", "Mar", "Apr", "May"],
    series=[
        ScenarioLineSeries(label="AC", values=[100, 103, 107, 109, 112]),
        ScenarioLineSeries(label="PY", values=[100, 101, 102, 103, 104]),
    ],
)
line.draw(ax1)

stacked = StackedColumnChart(
    title="Sales mix",
    subtitle="Product split",
    categories=["Jan", "Feb", "Mar", "Apr"],
    stack_labels=["Core", "Growth", "Services"],
    stack_values=[[20, 21, 22, 23], [8, 9, 10, 11], [5, 6, 6, 7]],
    comments=[CommentRef(index=1, x=3, y=41, text="Growth share increases")],
)
stacked.draw(ax2)

plt.tight_layout()
plt.show()
