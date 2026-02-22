from dataclasses import dataclass
from typing import Sequence

import numpy as np
import matplotlib.axes
import matplotlib.patches as mpatches

from ibcs_mpl.theme import impact_color, scenario_style
from ibcs_mpl.types import Impact, ScenarioCode, ReferenceScenario
from ibcs_mpl.charts.base import ChartBase
from ibcs_mpl.charts.specs import RelativeVarianceSeries
from ibcs_mpl.semantic import impact_from_value


def _impact_from_value(v: float) -> Impact:
    return impact_from_value(v)


def _draw_reference_axis(
    ax: matplotlib.axes.Axes,
    *,
    reference_scenario: ReferenceScenario,
    theme,
) -> None:
    if reference_scenario == ReferenceScenario.PY:
        ax.axhline(0.0, linewidth=2.0, color=theme.measured_light)
        return

    y_delta = 0.3
    ax.axhline(-y_delta, linewidth=1.0, color=theme.actual_dark)
    ax.axhline(+y_delta, linewidth=1.0, color=theme.actual_dark)


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

        _draw_reference_axis(
            ax,
            reference_scenario=self.reference_scenario,
            theme=self.theme,
        )

        head_style = scenario_style(self.theme, self.minuend_scenario)

        for xi, yi in zip(x, y, strict=True):
            imp = _impact_from_value(float(yi))
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
