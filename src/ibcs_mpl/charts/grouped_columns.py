from dataclasses import dataclass
from typing import Sequence

import matplotlib.axes
import numpy as np

from ibcs_mpl.charts.base import ChartBase
from ibcs_mpl.charts.specs import CategorySeries
from ibcs_mpl.primitives import DataLabels
from ibcs_mpl.theme import scenario_style
from ibcs_mpl.types import ScenarioCode


@dataclass(frozen=True, slots=True, kw_only=True)
class GroupedColumnChart(ChartBase):
    categories: Sequence[str] = ()

    primary_values: Sequence[float] = ()
    primary_scenario: ScenarioCode = ScenarioCode.AC

    reference_values: Sequence[float] = ()
    reference_scenario: ScenarioCode = ScenarioCode.PY

    labels: DataLabels = DataLabels("{:,.0f}")
    overlap_shift_ratio: float = 0.22

    def draw(self, ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        CategorySeries(categories=self.categories, values=self.primary_values).validate()
        CategorySeries(categories=self.categories, values=self.reference_values).validate()

        self._prep(ax)

        x = np.arange(len(self.categories), dtype=float)
        bar_width = self.theme.width_basic
        shift = bar_width * self.overlap_shift_ratio

        st_primary = scenario_style(self.theme, self.primary_scenario)
        st_reference = scenario_style(self.theme, self.reference_scenario)

        ax.bar(
            x - shift,
            self.reference_values,
            width=bar_width,
            color=st_reference.facecolor,
            edgecolor=st_reference.edgecolor,
            linewidth=st_reference.linewidth,
            hatch=st_reference.hatch,
            zorder=1,
        )
        ax.bar(
            x,
            self.primary_values,
            width=bar_width,
            color=st_primary.facecolor,
            edgecolor=st_primary.edgecolor,
            linewidth=st_primary.linewidth,
            hatch=st_primary.hatch,
            zorder=2,
        )

        ax.set_xticks(x, self.categories)
        self.labels.draw_above_bars(ax, x.tolist(), list(self.primary_values))

        return ax
