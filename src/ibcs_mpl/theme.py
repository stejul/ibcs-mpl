"""IBCS theme definitions: colors, widths, fonts."""

from dataclasses import dataclass
from typing import Final

from ibcs_mpl.types import Impact, ScenarioCode


__all__ = [
    "FillStyle",
    "IBCSTheme",
    "DEFAULT_THEME",
    "scenario_style",
    "impact_color",
]


@dataclass(frozen=True, slots=True, kw_only=True)
class FillStyle:
    facecolor: str | None = None
    edgecolor: str = "black"
    hatch: str | None = None
    linewidth: float = 1.2
    alpha: float = 1.0


@dataclass(frozen=True, slots=True, kw_only=True)
class IBCSTheme:
    actual_dark: str = "#3A3A3A"
    measured_light: str = "#BDBDBD"

    variance_pos: str = "#2E7D32"  # green
    variance_neg: str = "#C62828"  # red
    variance_neu: str = "#7A7A7A"  # medium gray

    font_size: int = 10
    title_size: int = 12
    label_size: int = 9

    width_basic: float = 2.0 / 3.0
    width_ratio: float = 1.0 / 3.0


DEFAULT_THEME: Final[IBCSTheme] = IBCSTheme()


def scenario_style(theme: IBCSTheme, scenario: ScenarioCode) -> FillStyle:
    mapping: dict[ScenarioCode, FillStyle] = {
        ScenarioCode.AC: FillStyle(
            facecolor=theme.actual_dark, edgecolor=theme.actual_dark, linewidth=0.8
        ),
        ScenarioCode.PY: FillStyle(
            facecolor=theme.measured_light, edgecolor=theme.measured_light, linewidth=0.8
        ),
        ScenarioCode.PL: FillStyle(facecolor=None, edgecolor=theme.actual_dark, linewidth=1.4),
        ScenarioCode.BU: FillStyle(facecolor=None, edgecolor=theme.actual_dark, linewidth=1.4),
        ScenarioCode.FC: FillStyle(
            facecolor=None, edgecolor=theme.actual_dark, hatch="///", linewidth=1.4
        ),
    }
    style = mapping.get(scenario)
    if style is not None:
        return style

    raise ValueError(f"Unknown scenario: {scenario}")


def impact_color(theme: IBCSTheme, impact: Impact) -> str:
    if impact == Impact.POSITIVE:
        return theme.variance_pos
    if impact == Impact.NEGATIVE:
        return theme.variance_neg
    return theme.variance_neu
