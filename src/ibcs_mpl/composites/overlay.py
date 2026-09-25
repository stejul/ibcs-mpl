"""Overlay layout for dual-axis charts."""

from dataclasses import dataclass
from typing import Sequence

import matplotlib.axes
import matplotlib.figure

from ibcs_mpl.charts.base import Chart


__all__ = [
    "draw_overlay",
]


def draw_overlay(
    ax: matplotlib.axes.Axes,
    primary_chart: Chart,
    secondary_chart: Chart,
    *,
    twin_axis: str = "x",  # "x" = twinx (second y-axis), "y" = twiny (second x-axis)
) -> tuple[matplotlib.axes.Axes, matplotlib.axes.Axes]:
    """Draw two charts sharing a primary axis, with an optional secondary (twin) axis for the second."""
    primary_chart.draw(ax)

    if twin_axis == "x":
        ax2 = ax.twinx()
    else:
        ax2 = ax.twiny()

    secondary_chart.draw(ax2)

    return (ax, ax2)


@dataclass(frozen=True, slots=True, kw_only=True)
class ExtendedLayout:
    left: float = 0.05
    right: float = 0.97
    top: float = 0.88
    bottom: float = 0.12
    gap: float = 0.015  # gap between panels
    break_marker: bool = True  # draw break symbols between panels


def draw_extended(
    fig: matplotlib.figure.Figure,
    charts: Sequence[Chart],
    *,
    layout: ExtendedLayout = ExtendedLayout(),
    shared_ylim: tuple[float, float] | None = None,
) -> list[matplotlib.axes.Axes]:
    """Draw a chart series as a horizontal continuation — multiple panels sharing the same y-axis scale."""
    if len(charts) < 2:
        raise ValueError("draw_extended requires at least 2 charts")

    n = len(charts)
    total_w = layout.right - layout.left
    panel_w = (total_w - (n - 1) * layout.gap) / n
    panel_h = layout.top - layout.bottom

    axes: list[matplotlib.axes.Axes] = []

    for idx, chart in enumerate(charts):
        x = layout.left + idx * (panel_w + layout.gap)
        ax = fig.add_axes((x, layout.bottom, panel_w, panel_h))
        chart.draw(ax)

        if shared_ylim is not None:
            ax.set_ylim(*shared_ylim)

        if layout.break_marker and idx < n - 1:
            # Draw two short diagonal slash lines (//) at the right edge of each panel
            # except the last, using axes coordinates with clip_on=False
            ax.plot(
                [1.0, 1.02],
                [0.3, 0.5],
                transform=ax.transAxes,
                linewidth=1.5,
                color="#888888",
                clip_on=False,
            )
            ax.plot(
                [1.0, 1.02],
                [0.4, 0.6],
                transform=ax.transAxes,
                linewidth=1.5,
                color="#888888",
                clip_on=False,
            )

        axes.append(ax)

    return axes
