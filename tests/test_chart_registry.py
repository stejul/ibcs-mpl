import pytest

from ibcs_mpl.charts import registry
from ibcs_mpl.charts.columns import SingleColumnChart


def test_default_registry_can_build_single_column() -> None:
    chart = registry.build(
        "single_column",
        title="Test",
        categories=["A"],
        values=[1.0],
    )
    assert isinstance(chart, SingleColumnChart)


def test_default_registry_unknown_key() -> None:
    with pytest.raises(KeyError):
        registry.build("does_not_exist")


def test_default_registry_contains_extended_chart_types() -> None:
    keys = set(registry.keys())
    assert "grouped_bar" in keys
    assert "stacked_bar" in keys
    assert "stacked_column" in keys
    assert "line" in keys
    assert "vertical_waterfall" in keys
    assert "horizontal_waterfall" in keys
