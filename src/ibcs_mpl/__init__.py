from ibcs_mpl.charts import (
    BubbleChart,
    GroupedBarChart,
    GroupedColumnChart,
    HorizontalWaterfallChart,
    LineChart,
    RelativeVariancePinChart,
    ScatterChart,
    ScenarioLineSeries,
    SingleBarChart,
    SingleColumnChart,
    StackedColumnChart,
    StackedBarChart,
    VerticalPinChart,
    VerticalWaterfallChart,
    registry,
    single_column_from_data,
)
from ibcs_mpl.catalog import available_chart_types, assert_required_charts
from ibcs_mpl.compliance import ComplianceEngine, ComplianceIssue, format_report
from ibcs_mpl.composites.multi_tier import draw_multi_tier
from ibcs_mpl.composites.overlay import ExtendedLayout, draw_extended, draw_overlay
from ibcs_mpl.composites.small_multiples import compute_shared_ylim, draw_small_multiples
from ibcs_mpl.data import ScenarioSeriesData, from_pandas, from_records
from ibcs_mpl.indicators import (
    DifferenceMarker,
    OutlierIndicator,
    ReferenceArrowhead,
    ScalingArea,
    ScalingLine,
    TrendArrow,
)
from ibcs_mpl.plugins import load_entrypoint_plugins, load_plugins_from_modules, register_plugin
from ibcs_mpl.reports import build_plain_report_table, build_variance_table
from ibcs_mpl.theme_profiles import get_theme_profile
from ibcs_mpl.annotations import find_legend_position
from ibcs_mpl.titles import MessageBlock, PageTitle
from ibcs_mpl.validation import (
    validate_ratio_widths,
    validate_scenario_order,
    validate_stacked_sign_consistency,
)


__all__ = [
    # Charts
    "SingleColumnChart",
    "SingleBarChart",
    "GroupedColumnChart",
    "GroupedBarChart",
    "StackedBarChart",
    "VerticalWaterfallChart",
    "HorizontalWaterfallChart",
    "StackedColumnChart",
    "LineChart",
    "ScenarioLineSeries",
    "RelativeVariancePinChart",
    "VerticalPinChart",
    "ScatterChart",
    "BubbleChart",
    # Data
    "ScenarioSeriesData",
    "from_records",
    "from_pandas",
    # Composites
    "draw_small_multiples",
    "compute_shared_ylim",
    "draw_multi_tier",
    "draw_overlay",
    "ExtendedLayout",
    "draw_extended",
    # Indicators
    "DifferenceMarker",
    "TrendArrow",
    "ScalingLine",
    "ScalingArea",
    "OutlierIndicator",
    "ReferenceArrowhead",
    # Compliance
    "ComplianceEngine",
    "ComplianceIssue",
    "format_report",
    # Utilities
    "find_legend_position",
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
