import matplotlib.pyplot as plt

from ibcs_mpl.charts import GroupedBarChart, VerticalWaterfallChart


grouped_bar = GroupedBarChart(
    title="Contribution",
    subtitle="AC vs PY (kEUR)",
    categories=["Berlin", "Paris", "Rome", "Vienna"],
    primary_values=[620, 795, 618, 720],
    reference_values=[592, 759, 575, 690],
)

waterfall = VerticalWaterfallChart(
    title="EBIT Bridge",
    subtitle="AC variance walk (mEUR)",
    categories=["PY", "Volume", "Price", "Cost", "AC"],
    values=[42.0, 6.5, 3.0, -4.0, 47.5],
    is_total=[True, False, False, False, True],
)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.0, 5.2))
grouped_bar.draw(ax1)
waterfall.draw(ax2)
plt.subplots_adjust(top=0.76, wspace=0.26)
plt.show()
