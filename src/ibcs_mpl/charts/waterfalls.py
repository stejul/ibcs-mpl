from dataclasses import dataclass
from typing import Sequence

import matplotlib.axes
import numpy as np

from ibcs_mpl.charts.base import ChartBase
from ibcs_mpl.charts.specs import WaterfallSeries
from ibcs_mpl.semantic import impact_from_value
from ibcs_mpl.theme import impact_color, scenario_style
from ibcs_mpl.types import ScenarioCode


def _waterfall_geometry(
    values: Sequence[float], is_total: Sequence[bool]
) -> tuple[list[float], list[float], list[float], list[float]]:
    running = 0.0
    bottoms: list[float] = []
    heights: list[float] = []
    starts: list[float] = []
    ends: list[float] = []

    for value, total in zip(values, is_total, strict=True):
        if total:
            start = 0.0
            end = value
            running = value
        else:
            start = running
            end = running + value
            running = end

        bottoms.append(min(start, end))
        heights.append(abs(end - start))
        starts.append(start)
        ends.append(end)

    return bottoms, heights, starts, ends


@dataclass(frozen=True, slots=True, kw_only=True)
class VerticalWaterfallChart(ChartBase):
    categories: Sequence[str] = ()
    values: Sequence[float] = ()
    is_total: Sequence[bool] = ()
    total_scenario: ScenarioCode = ScenarioCode.AC

    show_value_labels: bool = True
    delta_label_fmt: str = "{:+,.1f}"
    total_label_fmt: str = "{:,.1f}"

    def draw(self, ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        WaterfallSeries(
            categories=self.categories,
            values=self.values,
            is_total=self.is_total,
        ).validate()

        self._prep(ax)

        x = np.arange(len(self.categories), dtype=float)
        bottoms, heights, _starts, ends = _waterfall_geometry(self.values, self.is_total)
        total_style = scenario_style(self.theme, self.total_scenario)

        for idx, value in enumerate(self.values):
            if self.is_total[idx]:
                facecolor = total_style.facecolor
                edgecolor = total_style.edgecolor
                hatch = total_style.hatch
                linewidth = total_style.linewidth
            else:
                variance_color = impact_color(self.theme, impact_from_value(float(value)))
                facecolor = variance_color
                edgecolor = variance_color
                hatch = None
                linewidth = 0.8

            ax.bar(
                [x[idx]],
                [heights[idx]],
                width=self.theme.width_basic,
                bottom=[bottoms[idx]],
                color=facecolor,
                edgecolor=edgecolor,
                hatch=hatch,
                linewidth=linewidth,
            )

            if idx < len(self.values) - 1:
                y_connector = ends[idx]
                x0 = x[idx] + self.theme.width_basic / 2.0
                x1 = x[idx + 1] - self.theme.width_basic / 2.0
                ax.plot(
                    [x0, x1],
                    [y_connector, y_connector],
                    color=self.theme.variance_neu,
                    linewidth=0.8,
                )

            if self.show_value_labels:
                label = (
                    self.total_label_fmt.format(ends[idx])
                    if self.is_total[idx]
                    else self.delta_label_fmt.format(value)
                )
                y_anchor = ends[idx]
                dy = 4 if value >= 0 else -6
                va = "bottom" if value >= 0 else "top"
                ax.annotate(
                    label,
                    (x[idx], y_anchor),
                    xytext=(0, dy),
                    textcoords="offset points",
                    ha="center",
                    va=va,
                    fontsize=self.theme.label_size,
                )

        ax.set_xticks(x, self.categories)
        return ax


@dataclass(frozen=True, slots=True, kw_only=True)
class HorizontalWaterfallChart(ChartBase):
    categories: Sequence[str] = ()
    values: Sequence[float] = ()
    is_total: Sequence[bool] = ()
    total_scenario: ScenarioCode = ScenarioCode.AC

    show_value_labels: bool = True
    delta_label_fmt: str = "{:+,.1f}"
    total_label_fmt: str = "{:,.1f}"

    def draw(self, ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        WaterfallSeries(
            categories=self.categories,
            values=self.values,
            is_total=self.is_total,
        ).validate()

        self._prep(ax)

        y = np.arange(len(self.categories), dtype=float)
        lefts, widths, _starts, ends = _waterfall_geometry(self.values, self.is_total)
        total_style = scenario_style(self.theme, self.total_scenario)

        for idx, value in enumerate(self.values):
            if self.is_total[idx]:
                facecolor = total_style.facecolor
                edgecolor = total_style.edgecolor
                hatch = total_style.hatch
                linewidth = total_style.linewidth
            else:
                variance_color = impact_color(self.theme, impact_from_value(float(value)))
                facecolor = variance_color
                edgecolor = variance_color
                hatch = None
                linewidth = 0.8

            ax.barh(
                [y[idx]],
                [widths[idx]],
                height=self.theme.width_basic,
                left=[lefts[idx]],
                color=facecolor,
                edgecolor=edgecolor,
                hatch=hatch,
                linewidth=linewidth,
            )

            if idx < len(self.values) - 1:
                x_connector = ends[idx]
                y0 = y[idx] + self.theme.width_basic / 2.0
                y1 = y[idx + 1] - self.theme.width_basic / 2.0
                ax.plot(
                    [x_connector, x_connector],
                    [y0, y1],
                    color=self.theme.variance_neu,
                    linewidth=0.8,
                )

            if self.show_value_labels:
                label = (
                    self.total_label_fmt.format(ends[idx])
                    if self.is_total[idx]
                    else self.delta_label_fmt.format(value)
                )
                x_anchor = ends[idx]
                dx = 4 if value >= 0 else -4
                ha = "left" if value >= 0 else "right"
                ax.annotate(
                    label,
                    (x_anchor, y[idx]),
                    xytext=(dx, 0),
                    textcoords="offset points",
                    ha=ha,
                    va="center",
                    fontsize=self.theme.label_size,
                )

        ax.set_yticks(y, self.categories)
        ax.invert_yaxis()
        return ax
