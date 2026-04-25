from dataclasses import dataclass
from typing import Sequence

import numpy as np
import matplotlib.axes
import matplotlib.patches as mpatches

from ibcs_mpl.theme import impact_color, scenario_style
from ibcs_mpl.types import ScenarioCode, ReferenceScenario
from ibcs_mpl.charts.base import ChartBase
from ibcs_mpl.charts.specs import RelativeVarianceSeries
from ibcs_mpl.semantic import impact_from_value


def _draw_reference_axis(
    ax: matplotlib.axes.Axes,
    *,
    reference_scenario: ReferenceScenario,
    theme,
    orient: str = "h",
) -> None:
    """Draw the zero-reference line(s). orient='h' → axhline, orient='v' → axvline."""
    line = ax.axvline if orient == "v" else ax.axhline
    delta = 0.3

    if reference_scenario == ReferenceScenario.PY:
        line(0.0, linewidth=2.0, color=theme.measured_light)
        return

    line(-delta, linewidth=1.0, color=theme.actual_dark)
    line(+delta, linewidth=1.0, color=theme.actual_dark)


@dataclass(frozen=True, slots=True, kw_only=True)
class RelativeVariancePinChart(ChartBase):
    categories: Sequence[str] = ()
    rel_variance_pct: Sequence[float] = ()   # e.g. +12.5 means +12.5%
    minuend_scenario: ScenarioCode = ScenarioCode.AC
    reference_scenario: ReferenceScenario = ReferenceScenario.PY

    pin_width: float = 0.10
    head_height_pct: float = 1.0  # head marker size in "percentage points"
    label_offset_pos: int = 5
    label_offset_neg: int = -10       # points
    ylim_pad_top: float = 4.0
    ylim_pad_bottom: float = 12.0    # percentage points

    def draw(self, ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        RelativeVarianceSeries(
            categories=self.categories,
            rel_variance_pct=self.rel_variance_pct,
            minuend_scenario=self.minuend_scenario,
            reference_scenario=self.reference_scenario,
        ).validate()

        self._prep(ax)

        x = np.arange(len(self.categories))
        y = np.array(self.rel_variance_pct, dtype=float)

        bbox = dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8)

        _draw_reference_axis(ax, reference_scenario=self.reference_scenario, theme=self.theme)

        head_style = scenario_style(self.theme, self.minuend_scenario)

        for xi, yi in zip(x, y, strict=True):
            imp = impact_from_value(float(yi))
            c = impact_color(self.theme, imp)

            # Pin body (thin column)
            ax.bar([xi], [yi], width=self.pin_width, color=c, edgecolor=c, linewidth=0.8)

            # Head marker: small rectangle at end of the pin
            if yi >= 0:
                head_y = yi
                rect_y = head_y
                va = "bottom"
                dy = self.label_offset_pos
            else:
                head_y = yi
                rect_y = head_y - self.head_height_pct
                va = "top"
                dy = self.label_offset_neg

            head = mpatches.Rectangle(
                (xi - self.pin_width / 2.0, rect_y),
                self.pin_width,
                self.head_height_pct,
                facecolor=head_style.facecolor,
                edgecolor=head_style.edgecolor,
                hatch=head_style.hatch,
                linewidth=head_style.linewidth,
            )
            ax.add_patch(head)

            # Label outside in direction of change :contentReference[oaicite:15]{index=15}
            ax.annotate(
                f"{yi:+.1f}%",
                (xi, yi),
                xytext=(0, dy),
                textcoords="offset points",
                ha="center",
                va=va,
                fontsize=self.theme.label_size,
                color=c,
                bbox=bbox
            )

        low = min(-30.0, float(y.min()) - self.ylim_pad_bottom)
        high = max(30.0, float(y.max()) + self.ylim_pad_top)

        ax.set_xticks(x, self.categories)
        ax.set_ylim(low, high)

        return ax


@dataclass(frozen=True, slots=True, kw_only=True)
class VerticalPinChart(ChartBase):
    categories: Sequence[str] = ()
    rel_variance_pct: Sequence[float] = ()   # e.g. +12.5 means +12.5%
    minuend_scenario: ScenarioCode = ScenarioCode.AC
    reference_scenario: ReferenceScenario = ReferenceScenario.PY

    pin_height: float = 0.10
    head_width_pct: float = 1.0   # head marker width in "percentage points"
    label_offset_pos: int = 5
    label_offset_neg: int = -10
    xlim_pad_right: float = 4.0
    xlim_pad_left: float = 12.0

    def draw(self, ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        RelativeVarianceSeries(
            categories=self.categories,
            rel_variance_pct=self.rel_variance_pct,
            minuend_scenario=self.minuend_scenario,
            reference_scenario=self.reference_scenario,
        ).validate()

        self._prep(ax)

        y = np.arange(len(self.categories))
        x = np.array(self.rel_variance_pct, dtype=float)

        bbox = dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8)

        _draw_reference_axis(ax, reference_scenario=self.reference_scenario, theme=self.theme, orient="v")

        head_style = scenario_style(self.theme, self.minuend_scenario)

        for yi, xi in zip(y, x, strict=True):
            imp = impact_from_value(float(xi))
            c = impact_color(self.theme, imp)

            # Pin body (thin horizontal bar)
            ax.barh([yi], [xi], height=self.pin_height, color=c, edgecolor=c, linewidth=0.8)

            # Head marker: small rectangle at end of the pin
            if xi >= 0:
                rect_x = xi
                ha = "left"
                dx = self.label_offset_pos
            else:
                rect_x = xi - self.head_width_pct
                ha = "right"
                dx = self.label_offset_neg

            head = mpatches.Rectangle(
                (rect_x, yi - self.pin_height / 2.0),
                self.head_width_pct,
                self.pin_height,
                facecolor=head_style.facecolor,
                edgecolor=head_style.edgecolor,
                hatch=head_style.hatch,
                linewidth=head_style.linewidth,
            )
            ax.add_patch(head)

            # Label outside in direction of change
            ax.annotate(
                f"{xi:+.1f}%",
                (xi, yi),
                xytext=(dx, 0),
                textcoords="offset points",
                ha=ha,
                va="center",
                fontsize=self.theme.label_size,
                color=c,
                bbox=bbox,
            )

        left = min(-30.0, float(x.min()) - self.xlim_pad_left)
        right = max(30.0, float(x.max()) + self.xlim_pad_right)

        ax.set_yticks(y, self.categories)
        ax.invert_yaxis()
        ax.set_xlim(left, right)

        return ax
