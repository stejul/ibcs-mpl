from dataclasses import dataclass
from typing import Sequence

import matplotlib.axes
import numpy as np

from ibcs_mpl.annotations import CommentRef, LegendItem, draw_comment_refs, draw_inline_legend
from ibcs_mpl.charts.base import ChartBase
from ibcs_mpl.charts.specs import StackedSeries
from ibcs_mpl.theme import FillStyle
from ibcs_mpl.validation import validate_stacked_sign_consistency


def _series_shades(n: int) -> list[str]:
    shades = ["#2E2E2E", "#5A5A5A", "#868686", "#B0B0B0", "#D0D0D0", "#E8E8E8"]
    return [shades[i % len(shades)] for i in range(n)]


@dataclass(frozen=True, slots=True, kw_only=True)
class StackedColumnChart(ChartBase):
    categories: Sequence[str] = ()
    stack_labels: Sequence[str] = ()
    stack_values: Sequence[Sequence[float]] = ()
    show_legend: bool = True
    comments: Sequence[CommentRef] = ()
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
        x = np.arange(len(self.categories), dtype=float)
        bottoms = np.zeros(len(self.categories), dtype=float)
        colors = _series_shades(len(self.stack_labels))
        legend_items: list[LegendItem] = []

        for idx, values in enumerate(self.stack_values):
            vals = np.asarray(values, dtype=float)
            color = colors[idx]
            ax.bar(
                x,
                vals,
                width=self.theme.width_basic,
                bottom=bottoms,
                color=color,
                edgecolor=color,
                linewidth=0.8,
            )
            bottoms = bottoms + vals
            legend_items.append(
                LegendItem(
                    label=self.stack_labels[idx],
                    style=FillStyle(facecolor=color, edgecolor=color, linewidth=0.8),
                )
            )

        ax.set_xticks(x, self.categories)
        if self.show_legend:
            draw_inline_legend(ax, items=legend_items, x=1.01, y=0.85, dy=0.10)
        if self.comments:
            draw_comment_refs(ax, self.comments)

        return ax
