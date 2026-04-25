from dataclasses import dataclass
from typing import Sequence

import matplotlib.axes
import numpy as np

from ibcs_mpl.charts.base import ChartBase
from ibcs_mpl.theme import scenario_style
from ibcs_mpl.types import ScenarioCode


__all__ = [
    "ScatterChart",
    "BubbleChart",
]


def _validate_equal_lengths(**named_seqs: Sequence) -> None:
    lengths = {name: len(seq) for name, seq in named_seqs.items()}
    if any(v == 0 for v in lengths.values()):
        raise ValueError(f"All sequences must be non-empty: {lengths}")
    if len(set(lengths.values())) > 1:
        names = ", ".join(f"{k}={v}" for k, v in lengths.items())
        raise ValueError(f"All sequences must have the same length, got {names}")


def _plot_points(ax: matplotlib.axes.Axes, x, y, sizes, st) -> None:
    ax.scatter(
        list(x),
        list(y),
        s=sizes,
        c=st.facecolor if st.facecolor is not None else st.edgecolor,
        edgecolors=st.edgecolor,
        linewidths=st.linewidth,
        zorder=3,
    )


def _annotate_labels(ax: matplotlib.axes.Axes, x, y, labels: Sequence[str], fontsize: float) -> None:
    for xi, yi, lbl in zip(x, y, labels):
        ax.annotate(
            lbl,
            xy=(xi, yi),
            xytext=(4, 4),
            textcoords="offset points",
            fontsize=fontsize,
            va="bottom",
            ha="left",
        )


def _apply_axes_labels(ax: matplotlib.axes.Axes, x_label: str, y_label: str, fontsize: float) -> None:
    if x_label:
        ax.set_xlabel(x_label, fontsize=fontsize)
    if y_label:
        ax.set_ylabel(y_label, fontsize=fontsize)


@dataclass(frozen=True, slots=True, kw_only=True)
class ScatterChart(ChartBase):
    """IBCS-styled scatter chart for portfolio / two-value-axis analysis."""

    x_values: Sequence[float] = ()
    y_values: Sequence[float] = ()
    labels: Sequence[str] = ()
    scenario: ScenarioCode = ScenarioCode.AC
    x_label: str = ""
    y_label: str = ""
    marker_size: float = 40.0
    show_quadrants: bool = False

    def draw(self, ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        _validate_equal_lengths(x_values=self.x_values, y_values=self.y_values)
        self._prep(ax)

        st = scenario_style(self.theme, self.scenario)
        _plot_points(ax, self.x_values, self.y_values, self.marker_size, st)

        if self.labels:
            _annotate_labels(ax, self.x_values, self.y_values, self.labels, self.theme.label_size)

        if self.show_quadrants:
            ax.axhline(0, color="#CCCCCC", linewidth=0.6, zorder=0)
            ax.axvline(0, color="#CCCCCC", linewidth=0.6, zorder=0)

        _apply_axes_labels(ax, self.x_label, self.y_label, self.theme.label_size)
        return ax


@dataclass(frozen=True, slots=True, kw_only=True)
class BubbleChart(ChartBase):
    """Like ScatterChart but with a third dimension encoded as bubble size."""

    x_values: Sequence[float] = ()
    y_values: Sequence[float] = ()
    size_values: Sequence[float] = ()
    labels: Sequence[str] = ()
    scenario: ScenarioCode = ScenarioCode.AC
    x_label: str = ""
    y_label: str = ""
    size_scale: float = 500.0
    size_label: str = ""
    show_quadrants: bool = False

    def draw(self, ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        _validate_equal_lengths(
            x_values=self.x_values, y_values=self.y_values, size_values=self.size_values
        )
        self._prep(ax)

        raw = np.array(self.size_values, dtype=float)
        max_abs = np.max(np.abs(raw))
        sizes = raw / max_abs * self.size_scale if max_abs > 0 else raw

        st = scenario_style(self.theme, self.scenario)
        _plot_points(ax, self.x_values, self.y_values, sizes, st)

        if self.labels:
            _annotate_labels(ax, self.x_values, self.y_values, self.labels, self.theme.label_size)

        if self.show_quadrants:
            ax.axhline(0, color="#CCCCCC", linewidth=0.6, zorder=0)
            ax.axvline(0, color="#CCCCCC", linewidth=0.6, zorder=0)

        _apply_axes_labels(ax, self.x_label, self.y_label, self.theme.label_size)
        return ax
