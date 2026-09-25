"""Small-multiples grid layout."""

from dataclasses import dataclass
from math import ceil
from typing import Sequence, Any

import matplotlib.axes
import matplotlib.figure

from ibcs_mpl.charts.base import Chart
from ibcs_mpl.titles import PageTitle


__all__ = [
    "SmallMultiplesLayout",
    "draw_small_multiples",
    "compute_shared_ylim",
]


@dataclass(frozen=True, slots=True, kw_only=True)
class SmallMultiplesLayout:
    columns: int = 3
    left: float = 0.05
    right: float = 0.97
    top: float = 0.92
    bottom: float = 0.08
    h_gap: float = 0.03
    v_gap: float = 0.08
    min_title_band: float = 0.04


def _line_count(text: str | None) -> int:
    if not text:
        return 0
    return text.count("\n") + 1


def _chart_title_band(fig: matplotlib.figure.Figure, chart: Any, *, min_band: float) -> float:
    theme = getattr(chart, "theme", None)
    title_size = int(getattr(theme, "title_size", 11))
    subtitle_size = int(getattr(theme, "font_size", 9))

    title = getattr(chart, "title", None)
    if isinstance(title, PageTitle):
        title_text = title.render()
    else:
        title_text = title if isinstance(title, str) else ""

    subtitle = getattr(chart, "subtitle", None)
    message = getattr(chart, "message", None)
    message_text = getattr(message, "text", None)
    message_size = int(getattr(message, "size", max(title_size, 11))) if message is not None else 0

    lines_title = _line_count(title_text)
    lines_sub = _line_count(subtitle if isinstance(subtitle, str) else None)
    lines_msg = _line_count(message_text if isinstance(message_text, str) else None)

    fig_h_in = float(fig.get_size_inches()[1])

    def h_points(font_size: int, lines: int, spacing: float = 1.20) -> float:
        if lines <= 0:
            return 0.0
        return ((font_size / 72.0) / fig_h_in) * lines * spacing

    band = 0.0
    band += h_points(title_size, lines_title)
    if lines_sub > 0:
        band += h_points(subtitle_size, lines_sub)
        band += (max(3.0, subtitle_size * 0.30) / 72.0) / fig_h_in
    if lines_msg > 0:
        band += h_points(message_size, lines_msg)
        band += (max(4.0, message_size * 0.35) / 72.0) / fig_h_in

    top_pad = float(getattr(chart, "title_top_pad", 0.012))
    band += top_pad
    return max(min_band, band)


def draw_small_multiples(
    fig: matplotlib.figure.Figure,
    charts: Sequence[Chart],
    *,
    layout: SmallMultiplesLayout = SmallMultiplesLayout(),
    shared_ylim: tuple[float, float] | None = None,
) -> None:
    if len(charts) == 0:
        return

    cols = max(1, layout.columns)
    rows = ceil(len(charts) / cols)

    total_w = layout.right - layout.left
    total_h = layout.top - layout.bottom
    ax_w = (total_w - (cols - 1) * layout.h_gap) / cols
    slot_h = (total_h - (rows - 1) * layout.v_gap) / rows
    title_band = max(
        _chart_title_band(fig, chart, min_band=layout.min_title_band) for chart in charts
    )
    ax_h = max(0.03, slot_h - title_band)

    for idx, chart in enumerate(charts):
        row = idx // cols
        col = idx % cols
        x = layout.left + col * (ax_w + layout.h_gap)
        slot_top = layout.top - row * (slot_h + layout.v_gap)
        y = slot_top - slot_h
        ax = fig.add_axes((x, y, ax_w, ax_h))
        chart.draw(ax)
        if shared_ylim is not None:
            ax.set_ylim(*shared_ylim)


def compute_shared_ylim(axes: Sequence[matplotlib.axes.Axes]) -> tuple[float, float]:
    """Compute a common y-axis range covering all provided axes."""
    all_mins = [ax.get_ylim()[0] for ax in axes]
    all_maxs = [ax.get_ylim()[1] for ax in axes]
    return (min(all_mins), max(all_maxs))
