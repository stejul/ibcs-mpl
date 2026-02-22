from ibcs_mpl.charts import (
    GroupedBarChart,
    GroupedColumnChart,
    HorizontalWaterfallChart,
    LineChart,
    RelativeVariancePinChart,
    ScenarioLineSeries,
    SingleColumnChart,
    StackedColumnChart,
    StackedBarChart,
    VerticalWaterfallChart,
    registry,
    single_column_from_data,
)
from ibcs_mpl.catalog import available_chart_types, assert_required_charts
from ibcs_mpl.composites.multi_tier import draw_multi_tier
from ibcs_mpl.composites.small_multiples import draw_small_multiples
from ibcs_mpl.data import ScenarioSeriesData, from_pandas, from_records
from ibcs_mpl.plugins import load_entrypoint_plugins, load_plugins_from_modules, register_plugin
from ibcs_mpl.reports import build_plain_report_table, build_variance_table
from ibcs_mpl.theme_profiles import get_theme_profile
from ibcs_mpl.titles import MessageBlock, PageTitle
from ibcs_mpl.validation import (
    validate_ratio_widths,
    validate_scenario_order,
    validate_stacked_sign_consistency,
)


__all__ = [
    "GroupedColumnChart",
    "GroupedBarChart",
    "StackedBarChart",
    "VerticalWaterfallChart",
    "HorizontalWaterfallChart",
    "StackedColumnChart",
    "LineChart",
    "ScenarioLineSeries",
    "RelativeVariancePinChart",
    "SingleColumnChart",
    "ScenarioSeriesData",
    "from_records",
    "from_pandas",
    "draw_small_multiples",
    "draw_multi_tier",
    "PageTitle",
    "MessageBlock",
    "get_theme_profile",
    "validate_ratio_widths",
    "validate_scenario_order",
    "validate_stacked_sign_consistency",
    "registry",
    "single_column_from_data",
    "available_chart_types",
    "assert_required_charts",
    "register_plugin",
    "load_entrypoint_plugins",
    "load_plugins_from_modules",
    "build_plain_report_table",
    "build_variance_table",
    "main",
]


def main() -> None:
    print("ibcs-mpl: use charts and reports modules to render IBCS-styled visuals")
