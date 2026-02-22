from dataclasses import dataclass
from typing import Sequence

import numpy as np
import matplotlib.axes

from ibcs_mpl.theme import scenario_style
from ibcs_mpl.types import ScenarioCode
from ibcs_mpl.primitives import DataLabels
from ibcs_mpl.charts.base import ChartBase
from ibcs_mpl.charts.specs import ScenarioSeries


def _draw_single_columns(
    *,
    ax: matplotlib.axes.Axes,
    categories: Sequence[str],
    values: Sequence[float],
    scenario: ScenarioCode,
    labels: DataLabels | None,
    width: float,
    theme,
) -> None:
    x = np.arange(len(categories))
    st = scenario_style(theme, scenario)

    ax.bar(
        x,
        values,
        width=width,
        align="center",
        color=st.facecolor,
        edgecolor=st.edgecolor,
        linewidth=st.linewidth,
        hatch=st.hatch,
    )

    ax.set_xticks(x, categories)
    if labels is not None:
        labels.draw_above_bars(ax, x.tolist(), list(values))


@dataclass(frozen=True, slots=True, kw_only=True)
class SingleColumnChart(ChartBase):
    categories: Sequence[str] = ()
    values: Sequence[float] = ()
    scenario: ScenarioCode = ScenarioCode.AC
    labels: DataLabels | None = DataLabels("{:,.0f}")

    @classmethod
    def from_series(
        cls,
        *,
        title: str,
        series: ScenarioSeries,
        subtitle: str | None = None,
        labels: DataLabels | None = DataLabels("{:,.0f}"),
    ) -> "SingleColumnChart":
        series.validate()
        return cls(
            title=title,
            subtitle=subtitle,
            categories=series.categories,
            values=series.values,
            scenario=series.scenario,
            labels=labels,
        )

    def draw(self, ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        ScenarioSeries(
            categories=self.categories,
            values=self.values,
            scenario=self.scenario,
        ).validate()

        self._prep(ax)

        _draw_single_columns(
            ax=ax,
            categories=self.categories,
            values=self.values,
            scenario=self.scenario,
            labels=self.labels,
            width=self.theme.width_basic,
            theme=self.theme,
        )

        return ax
