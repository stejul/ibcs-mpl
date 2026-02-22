import pytest

from ibcs_mpl.charts.specs import CategorySeries, RelativeVarianceSeries


def test_category_series_validate_ok() -> None:
    spec = CategorySeries(categories=["Jan", "Feb"], values=[1.0, 2.0])
    spec.validate()


def test_category_series_validate_mismatch() -> None:
    spec = CategorySeries(categories=["Jan"], values=[1.0, 2.0])
    with pytest.raises(ValueError):
        spec.validate()


def test_relative_variance_validate_empty() -> None:
    spec = RelativeVarianceSeries(categories=[], rel_variance_pct=[])
    with pytest.raises(ValueError):
        spec.validate()
