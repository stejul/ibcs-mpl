import matplotlib.pyplot as plt

from ibcs_mpl.charts import registry


chart = registry.build(
    "grouped_column",
    title="Sales",
    subtitle="AC vs PY (mEUR)",
    categories=["Jan", "Feb", "Mar", "Apr"],
    primary_values=[44, 52, 49, 56],
    reference_values=[41, 50, 47, 54],
)


fig, ax = plt.subplots(figsize=(8.4, 3.2))
chart.draw(ax)
plt.tight_layout()
plt.show()
