import matplotlib.pyplot as plt

from ibcs_mpl.charts import ChartRegistry, GroupedColumnChart, SingleColumnChart
from ibcs_mpl.plugins import register_plugin


def register(registry: ChartRegistry) -> None:
    registry.register("my_single_column", SingleColumnChart)
    registry.register("my_grouped_column", GroupedColumnChart)


local_registry = ChartRegistry()
register_plugin(register, registry=local_registry)

chart = local_registry.build(
    "my_single_column",
    title="Plugin chart",
    categories=["Jan", "Feb", "Mar"],
    values=[10, 11, 13],
)

fig, ax = plt.subplots(figsize=(8, 3.2))
chart.draw(ax)
plt.tight_layout()
plt.show()
