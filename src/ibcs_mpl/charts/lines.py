"""IBCS-styled line charts with scenario-coded series."""

from dataclasses import dataclass
from typing import Sequence

import matplotlib.axes
import numpy as np

from ibcs_mpl.annotations import LegendItem, draw_inline_legend
from ibcs_mpl.charts.base import ChartBase
from ibcs_mpl.theme import scenario_style
from ibcs_mpl.types import ScenarioCode


__all__ = [
    "ScenarioLineSeries",
    "LineChart",
]


@dataclass(frozen=True, slots=True, kw_only=True)
class ScenarioLineSeries:
    label: str
    values: Sequence[float]
    scenario: ScenarioCode = ScenarioCode.AC


@dataclass(frozen=True, slots=True, kw_only=True)
class LineChart(ChartBase):
    categories: Sequence[str] = ()
    series: Sequence[ScenarioLineSeries] = ()
    show_legend: bool = True

    def draw(self, ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        if len(self.categories) == 0:
            raise ValueError("categories must not be empty")
        if len(self.series) == 0:
            raise ValueError("series must not be empty")

        self._prep(ax)
        x = np.arange(len(self.categories), dtype=float)
        legend_items: list[LegendItem] = []

        for s in self.series:
            if len(s.values) != len(self.categories):
                raise ValueError(f"series '{s.label}' length must match categories")
            st = scenario_style(self.theme, s.scenario)
            line_width = 2.0 if s.scenario in {ScenarioCode.AC, ScenarioCode.PY} else 1.4
            marker = "o"
            marker_face = st.facecolor if st.facecolor else "white"
            ax.plot(
                x,
                s.values,
                linewidth=line_width,
                color=st.edgecolor,
                marker=marker,
                markersize=4,
                markerfacecolor=marker_face,
                markeredgecolor=st.edgecolor,
            )
            legend_items.append(LegendItem(label=s.label, style=st))

        ax.set_xticks(x, self.categories)
        if self.show_legend:
            draw_inline_legend(ax, items=legend_items, x=1.01, y=0.85, dy=0.10)

        return ax
