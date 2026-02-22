from ibcs_mpl.semantic import impact_from_value
from ibcs_mpl.theme import DEFAULT_THEME, scenario_style
from ibcs_mpl.types import Impact, ScenarioCode


def test_impact_from_value() -> None:
    assert impact_from_value(2.0) is Impact.POSITIVE
    assert impact_from_value(-0.1) is Impact.NEGATIVE
    assert impact_from_value(0.0) is Impact.NEUTRAL


def test_scenario_style_mapping() -> None:
    ac = scenario_style(DEFAULT_THEME, ScenarioCode.AC)
    fc = scenario_style(DEFAULT_THEME, ScenarioCode.FC)

    assert ac.facecolor == DEFAULT_THEME.actual_dark
    assert ac.edgecolor == DEFAULT_THEME.actual_dark
    assert fc.hatch == "///"
    assert fc.facecolor is None
