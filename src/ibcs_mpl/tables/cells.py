from dataclasses import dataclass
from typing import Any, Callable

import matplotlib.axes
import matplotlib.patches as mpatches

from ibcs_mpl.tables.types import Rect
from ibcs_mpl.theme import DEFAULT_THEME, IBCSTheme, impact_color, scenario_style
from ibcs_mpl.types import Impact, ScenarioCode, ReferenceScenario
from ibcs_mpl.semantic import impact_from_value


def _impact(v: float) -> Impact:
    return impact_from_value(v)

@dataclass(frozen=True)
class VariancePercentCell:
    """Δ…% in tables: + sign, colored like variance pins/bars."""
    decimals: int = 1
    theme: IBCSTheme = DEFAULT_THEME
    pad_x: float = 0.01
    na_text: str = "n.a."

    def draw(self, ax: matplotlib.axes.Axes, rect: Rect, value: Any) -> None:
        if value is None:
            s = self.na_text
            c = self.theme.variance_neu
        else:
            v = float(value)
            s = f"{v:+.{self.decimals}f}%"
            c = impact_color(self.theme, _impact(v))

        ax.text(
            rect.x + rect.w - self.pad_x,
            rect.y + rect.h / 2,
            s,
            ha="right",
            va="center",
            fontsize=9,
            color=c,
        )


@dataclass(frozen=True)
class RelativeVariancePinCell:
    """
    In-cell horizontal pin for Δ…%:
      - pin colored green/red/gray
      - head marker uses scenario notation (AC solid, FC hatched)
      - axis style encodes reference scenario (PY solid light, PL/BU outline)
    """
    max_abs_pct: float
    minuend: ScenarioCode = ScenarioCode.AC
    reference: ReferenceScenario = ReferenceScenario.PY
    theme: IBCSTheme = DEFAULT_THEME

    pad_x: float = 0.02
    axis_y_frac: float = 0.50
    pin_thickness_pt: float = 4.0

    head_w_frac: float = 0.06
    head_h_frac: float = 0.35
    na_draw_axis_only: bool = True  # if None: show only axis

    def _draw_reference_axis(self, ax: matplotlib.axes.Axes, rect: Rect) -> None:
        y = rect.y + rect.h * self.axis_y_frac
        x0 = rect.x + rect.w * self.pad_x
        x1 = rect.x + rect.w * (1.0 - self.pad_x)

        if self.reference == ReferenceScenario.PY:
            # solid light axis
            ax.plot([x0, x1], [y, y], linewidth=2.0, color=self.theme.measured_light, solid_capstyle="butt")
        else:
            # outline axis (two parallel lines) for PL/BU
            dy = rect.h * 0.06
            ax.plot([x0, x1], [y - dy, y - dy], linewidth=1.0, color=self.theme.actual_dark)
            ax.plot([x0, x1], [y + dy, y + dy], linewidth=1.0, color=self.theme.actual_dark)

    def draw(self, ax: matplotlib.axes.Axes, rect: Rect, value: Any) -> None:
        self._draw_reference_axis(ax, rect)

        if value is None:
            return

        v = float(value)
        if self.max_abs_pct <= 0:
            return

        # clamp
        v = max(-self.max_abs_pct, min(self.max_abs_pct, v))

        imp = _impact(v)
        c = impact_color(self.theme, imp)
        head = scenario_style(self.theme, self.minuend)

        # geometry
        x_left = rect.x + rect.w * self.pad_x
        x_right = rect.x + rect.w * (1.0 - self.pad_x)
        x_mid = (x_left + x_right) / 2.0
        y = rect.y + rect.h * self.axis_y_frac

        # pin length proportional to max_abs_pct
        half = (x_right - x_left) * 0.48
        x_end = x_mid + half * (v / self.max_abs_pct)

        # pin (thin bar)
        ax.plot([x_mid, x_end], [y, y], linewidth=self.pin_thickness_pt, color=c, solid_capstyle="butt")

        # head marker at end
        hw = rect.w * self.head_w_frac
        hh = rect.h * self.head_h_frac
        hx = x_end - hw / 2.0
        hy = y - hh / 2.0

        ax.add_patch(
            mpatches.Rectangle(
                (hx, hy),
                hw,
                hh,
                facecolor=head.facecolor if head.facecolor else "none",
                edgecolor=head.edgecolor,
                hatch=head.hatch,
                linewidth=head.linewidth,
            )
        )


@dataclass(frozen=True)
class TextCell:
    fmt: Callable[[Any], str] = lambda v: "" if v is None else str(v)
    ha: str = "left"
    fontsize: int = 9
    color: str = "black"
    pad_x: float = 0.01

    def draw(self, ax: matplotlib.axes.Axes, rect: Rect, value: Any) -> None:
        if self.ha == "left":
            x = rect.x + self.pad_x
        elif self.ha == "right":
            x = rect.x + rect.w - self.pad_x
        else:
            x = rect.x + rect.w / 2
        ax.text(x, rect.y + rect.h / 2, self.fmt(value),
                ha=self.ha, va="center", fontsize=self.fontsize, color=self.color)


@dataclass(frozen=True)
class NumberCell:
    fmt: str = "{:,.0f}"
    fontsize: int = 9
    color: str = "black"
    pad_x: float = 0.01

    def draw(self, ax: matplotlib.axes.Axes, rect: Rect, value: Any) -> None:
        s = "" if value is None else self.fmt.format(float(value))
        ax.text(rect.x + rect.w - self.pad_x, rect.y + rect.h / 2, s,
                ha="right", va="center", fontsize=self.fontsize, color=self.color)


@dataclass(frozen=True)
class PercentCell:
    decimals: int = 1
    fontsize: int = 9
    color: str = "black"
    pad_x: float = 0.01

    def draw(self, ax: matplotlib.axes.Axes, rect: Rect, value: Any) -> None:
        s = "" if value is None else f"{float(value):,.{self.decimals}f}%"
        ax.text(rect.x + rect.w - self.pad_x, rect.y + rect.h / 2, s,
                ha="right", va="center", fontsize=self.fontsize, color=self.color)


@dataclass(frozen=True)
class VarianceNumberCell:
    fmt: str = "{:+,.0f}"
    fontsize: int = 9
    theme: IBCSTheme = DEFAULT_THEME
    pad_x: float = 0.01

    def draw(self, ax: matplotlib.axes.Axes, rect: Rect, value: Any) -> None:
        if value is None:
            return
        v = float(value)
        c = impact_color(self.theme, _impact(v))
        ax.text(rect.x + rect.w - self.pad_x, rect.y + rect.h / 2, self.fmt.format(v),
                ha="right", va="center", fontsize=self.fontsize, color=c)


@dataclass(frozen=True)
class VarianceBarCell:
    max_abs: float
    theme: IBCSTheme = DEFAULT_THEME

    def draw(self, ax: matplotlib.axes.Axes, rect: Rect, value: Any) -> None:
        if value is None or self.max_abs <= 0:
            return
        v = float(value)
        v = max(-self.max_abs, min(self.max_abs, v))

        mid_x = rect.x + rect.w * 0.5
        y = rect.y + rect.h * 0.5
        half_w = rect.w * 0.48

        # center baseline
        ax.plot([mid_x, mid_x], [rect.y + rect.h * 0.2, rect.y + rect.h * 0.8], linewidth=0.8)

        frac = v / self.max_abs
        x1 = mid_x + half_w * frac
        c = impact_color(self.theme, _impact(v))

        ax.plot([mid_x, x1], [y, y], linewidth=6.0, solid_capstyle="butt", color=c)
