from ibcs_mpl.charts.adapters import single_column_from_data
from ibcs_mpl.charts.base import Chart, ChartBase
from ibcs_mpl.charts.bars import GroupedBarChart, SingleBarChart, StackedBarChart
from ibcs_mpl.charts.columns import SingleColumnChart
from ibcs_mpl.charts.grouped_columns import GroupedColumnChart
from ibcs_mpl.charts.lines import LineChart, ScenarioLineSeries
from ibcs_mpl.charts.pins import RelativeVariancePinChart, VerticalPinChart
from ibcs_mpl.charts.registry import ChartRegistry
from ibcs_mpl.charts.scatter import BubbleChart, ScatterChart
from ibcs_mpl.charts.stacked_columns import StackedColumnChart
from ibcs_mpl.charts.waterfalls import HorizontalWaterfallChart, VerticalWaterfallChart


registry = ChartRegistry()
registry.register("single_column", SingleColumnChart)
registry.register("single_bar", SingleBarChart)
registry.register("grouped_column", GroupedColumnChart)
registry.register("grouped_bar", GroupedBarChart)
registry.register("stacked_bar", StackedBarChart)
registry.register("stacked_column", StackedColumnChart)
registry.register("line", LineChart)
registry.register("relative_variance_pin", RelativeVariancePinChart)
registry.register("vertical_pin", VerticalPinChart)
registry.register("vertical_waterfall", VerticalWaterfallChart)
registry.register("horizontal_waterfall", HorizontalWaterfallChart)
registry.register("scatter", ScatterChart)
registry.register("bubble", BubbleChart)


__all__ = [
    "Chart",
    "ChartBase",
    "SingleColumnChart",
    "SingleBarChart",
    "GroupedColumnChart",
    "GroupedBarChart",
    "StackedBarChart",
    "StackedColumnChart",
    "LineChart",
    "ScenarioLineSeries",
    "RelativeVariancePinChart",
    "VerticalPinChart",
    "VerticalWaterfallChart",
    "HorizontalWaterfallChart",
    "ScatterChart",
    "BubbleChart",
    "ChartRegistry",
    "registry",
    "single_column_from_data",
]
