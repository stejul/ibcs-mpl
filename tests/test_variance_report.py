from ibcs_mpl.reports.variance import _relative_variance_pct


def test_relative_variance_pct_regular_case() -> None:
    assert _relative_variance_pct(120.0, 100.0) == 20.0


def test_relative_variance_pct_not_available_for_opposite_sign() -> None:
    assert _relative_variance_pct(30.0, -30.0) is None
