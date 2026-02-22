from ibcs_mpl.validation import (
    validate_ratio_widths,
    validate_scenario_order,
    validate_stacked_sign_consistency,
)


def test_validate_ratio_widths_flags_bad_ratio() -> None:
    issues = validate_ratio_widths(2 / 3, 0.4)
    assert any(i.code == "RATIO_WIDTH_NOT_HALF" for i in issues)


def test_validate_scenario_order_flags_reference_first() -> None:
    issues = validate_scenario_order(["PY", "AC"])
    assert any(i.code == "SCENARIO_ORDER_REFERENCE_FIRST" for i in issues)


def test_validate_stacked_sign_consistency_flags_mixed_signs() -> None:
    issues = validate_stacked_sign_consistency([[1, -2, 3]])
    assert any(i.code == "STACKED_MIXED_SIGN" for i in issues)
