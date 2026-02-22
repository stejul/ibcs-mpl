from dataclasses import dataclass
from typing import Sequence

import matplotlib.axes
import numpy as np

from ibcs_mpl.charts.base import ChartBase
from ibcs_mpl.charts.specs import GroupedScenarioSeries, StackedSeries
from ibcs_mpl.primitives import DataLabels
from ibcs_mpl.theme import scenario_style
from ibcs_mpl.types import ScenarioCode
from ibcs_mpl.validation import validate_stacked_sign_consistency


def _stack_colors(n: int) -> list[str]:
    shades = ["#2E2E2E", "#575757", "#808080", "#A5A5A5", "#C8C8C8", "#E1E1E1"]
    return [shades[idx % len(shades)] for idx in range(n)]


@dataclass(frozen=True, slots=True, kw_only=True)
class GroupedBarChart(ChartBase):
    categories: Sequence[str] = ()

    primary_values: Sequence[float] = ()
    primary_scenario: ScenarioCode = ScenarioCode.AC

    reference_values: Sequence[float] = ()
    reference_scenario: ScenarioCode = ScenarioCode.PY

    labels: DataLabels = DataLabels("{:,.0f}")
    overlap_shift_ratio: float = 0.22

    def draw(self, ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        GroupedScenarioSeries(
            categories=self.categories,
            primary_values=self.primary_values,
            reference_values=self.reference_values,
            primary_scenario=self.primary_scenario,
            reference_scenario=self.reference_scenario,
        ).validate()

        self._prep(ax)

        y = np.arange(len(self.categories), dtype=float)
        bar_h = self.theme.width_basic
        shift = bar_h * self.overlap_shift_ratio

        st_primary = scenario_style(self.theme, self.primary_scenario)
        st_reference = scenario_style(self.theme, self.reference_scenario)

        ax.barh(
            y - shift,
            self.reference_values,
            height=bar_h,
            color=st_reference.facecolor,
            edgecolor=st_reference.edgecolor,
            linewidth=st_reference.linewidth,
            hatch=st_reference.hatch,
            zorder=1,
        )
        ax.barh(
            y,
            self.primary_values,
            height=bar_h,
            color=st_primary.facecolor,
            edgecolor=st_primary.edgecolor,
            linewidth=st_primary.linewidth,
            hatch=st_primary.hatch,
            zorder=2,
        )

        ax.set_yticks(y, self.categories)
        ax.invert_yaxis()
        return ax


@dataclass(frozen=True, slots=True, kw_only=True)
class StackedBarChart(ChartBase):
    categories: Sequence[str] = ()
    stack_labels: Sequence[str] = ()
    stack_values: Sequence[Sequence[float]] = ()
    enforce_semantic_rules: bool = True

    def draw(self, ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        spec = StackedSeries(
            categories=self.categories,
            stack_labels=self.stack_labels,
            stack_values=self.stack_values,
        )
        spec.validate()
        if self.enforce_semantic_rules:
            issues = validate_stacked_sign_consistency(self.stack_values)
            if issues:
                raise ValueError(issues[0].message)

        self._prep(ax)

        y = np.arange(len(self.categories), dtype=float)
        left = np.zeros(len(self.categories), dtype=float)
        colors = _stack_colors(len(self.stack_labels))
        bar_h = self.theme.width_basic

        for idx, values in enumerate(self.stack_values):
            arr = np.asarray(values, dtype=float)
            ax.barh(
                y,
                arr,
                left=left,
                height=bar_h,
                color=colors[idx],
                edgecolor=colors[idx],
                linewidth=0.8,
            )
            left = left + arr

        ax.set_yticks(y, self.categories)
        ax.invert_yaxis()
        return ax
