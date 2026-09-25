"""Convenience adapters to build charts from plain data structures."""

from ibcs_mpl.charts.columns import SingleColumnChart
from ibcs_mpl.data import ScenarioSeriesData

__all__ = [
    "single_column_from_data",
]


def single_column_from_data(
    *, title: str, data: ScenarioSeriesData, subtitle: str | None = None
) -> SingleColumnChart:
    data.validate()
    return SingleColumnChart(
        title=title,
        subtitle=subtitle,
        categories=data.categories,
        values=data.values,
        scenario=data.scenario,
    )
