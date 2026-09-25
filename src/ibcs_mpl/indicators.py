"""Visual indicators: difference markers, scaling lines, outliers."""

from dataclasses import dataclass, field
from typing import Sequence

import matplotlib.axes

from ibcs_mpl.theme import IBCSTheme, DEFAULT_THEME, impact_color, scenario_style
from ibcs_mpl.types import ScenarioCode
from ibcs_mpl.semantic import impact_from_value


__all__ = [
    "DifferenceMarker",
    "TrendArrow",
    "ScalingLine",
    "ScalingArea",
    "OutlierIndicator",
    "ReferenceArrowhead",
]


@dataclass(frozen=True, slots=True, kw_only=True)
class DifferenceMarker:
    """Shows absolute difference (Δ) between two data points on a chart."""

    x: float
    y1: float
    y2: float
    label: str | None = None
    bracket_width: float = 0.15
    theme: IBCSTheme = field(default_factory=lambda: DEFAULT_THEME)

    def draw(self, ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        delta = self.y2 - self.y1
        impact = impact_from_value(delta)
        c = impact_color(self.theme, impact)

        label_text = self.label if self.label is not None else f"{delta:+,.0f}"

        # Vertical spine of bracket
        ax.plot(
            [self.x, self.x],
            [self.y1, self.y2],
            color=c,
            linewidth=1.0,
            solid_capstyle="butt",
        )
        # Horizontal tick at y1
        ax.plot(
            [self.x - self.bracket_width, self.x + self.bracket_width],
            [self.y1, self.y1],
            color=c,
            linewidth=1.0,
        )
        # Horizontal tick at y2
        ax.plot(
            [self.x - self.bracket_width, self.x + self.bracket_width],
            [self.y2, self.y2],
            color=c,
            linewidth=1.0,
        )

        mid_y = (self.y1 + self.y2) / 2
        ax.text(
            self.x + self.bracket_width + 0.05,
            mid_y,
            label_text,
            ha="left",
            va="center",
            fontsize=self.theme.label_size,
            color=c,
        )

        return ax


@dataclass(frozen=True, slots=True, kw_only=True)
class TrendArrow:
    """Draws a directional trend arrow between two points."""

    x1: float
    y1: float
    x2: float
    y2: float
    scenario: ScenarioCode = ScenarioCode.AC
    arrowstyle: str = "->"
    linewidth: float = 1.5
    theme: IBCSTheme = field(default_factory=lambda: DEFAULT_THEME)

    def draw(self, ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        color = scenario_style(self.theme, self.scenario).edgecolor
        ax.annotate(
            "",
            xy=(self.x2, self.y2),
            xytext=(self.x1, self.y1),
            arrowprops=dict(
                arrowstyle=self.arrowstyle,
                color=color,
                lw=self.linewidth,
            ),
        )
        return ax


@dataclass(frozen=True, slots=True, kw_only=True)
class ScalingLine:
    """A horizontal reference line indicating a shared scale value across charts."""

    y: float
    label: str | None = None
    color: str = "#888888"
    linewidth: float = 0.8
    linestyle: str = "--"
    theme: IBCSTheme = field(default_factory=lambda: DEFAULT_THEME)

    def draw(self, ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        ax.axhline(
            self.y,
            linewidth=self.linewidth,
            color=self.color,
            linestyle=self.linestyle,
            zorder=0,
        )
        if self.label is not None:
            xlim = ax.get_xlim()
            ax.text(
                xlim[1],
                self.y,
                self.label,
                va="bottom",
                ha="right",
                fontsize=self.theme.label_size,
                color=self.color,
                transform=ax.transData,
            )
        return ax


@dataclass(frozen=True, slots=True, kw_only=True)
class ScalingArea:
    """A shaded horizontal band indicating acceptable scale range."""

    y_low: float
    y_high: float
    color: str = "#EEEEEE"
    alpha: float = 0.4
    theme: IBCSTheme = field(default_factory=lambda: DEFAULT_THEME)

    def draw(self, ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        ax.axhspan(
            self.y_low,
            self.y_high,
            facecolor=self.color,
            alpha=self.alpha,
            zorder=0,
        )
        return ax


@dataclass(frozen=True, slots=True, kw_only=True)
class OutlierIndicator:
    """Marks that a data value has been clipped/truncated at the axis limit."""

    positions: Sequence[float]
    direction: str = "top"  # "top" or "bottom"
    color: str = "#3A3A3A"
    size: float = 0.08
    theme: IBCSTheme = field(default_factory=lambda: DEFAULT_THEME)

    def draw(self, ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        ylim = ax.get_ylim()

        if self.direction == "top":
            y_center = ylim[1] * 0.98
        else:
            y_center = ylim[0] * 1.02

        y_span = (ylim[1] - ylim[0]) * 0.02

        for pos in self.positions:
            # 5-point zigzag wave: W-shape centered at (pos, y_center)
            half = self.size / 2
            xs = [
                pos - half,
                pos - half / 2,
                pos,
                pos + half / 2,
                pos + half,
            ]
            ys = [
                y_center,
                y_center + y_span,
                y_center,
                y_center + y_span,
                y_center,
            ]
            ax.plot(xs, ys, color=self.color, linewidth=1.0, solid_capstyle="round")

        return ax


@dataclass(frozen=True, slots=True, kw_only=True)
class ReferenceArrowhead:
    """Draws a small arrowhead marker at a reference value (like the tip of a reference bar)."""

    positions: Sequence[float]
    values: Sequence[float]
    scenario: ScenarioCode = ScenarioCode.PY
    marker_size: float = 7.0
    theme: IBCSTheme = field(default_factory=lambda: DEFAULT_THEME)

    def draw(self, ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        style = scenario_style(self.theme, self.scenario)
        ax.plot(
            list(self.positions),
            list(self.values),
            marker="^",
            markersize=self.marker_size,
            linestyle="none",
            color=style.edgecolor,
            markerfacecolor=style.facecolor if style.facecolor is not None else style.edgecolor,
            zorder=5,
        )
        return ax
