"""Multi-tier figure layout for stacked charts."""

from dataclasses import dataclass
from typing import Sequence, Any

import matplotlib.figure

from ibcs_mpl.charts.base import Chart
from ibcs_mpl.titles import PageTitle


__all__ = [
    "MultiTierLayout",
    "draw_multi_tier",
]


@dataclass(frozen=True, slots=True, kw_only=True)
class MultiTierLayout:
    left: float = 0.08
    right: float = 0.95
    bottom: float = 0.10
    top: float = 0.90
    tier_gap: float = 0.08
    tier_ratios: Sequence[float] = (0.55, 0.25, 0.20)
    min_title_band: float = 0.045


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


def draw_multi_tier(
    fig: matplotlib.figure.Figure,
    tiers: Sequence[Chart],
    *,
    layout: MultiTierLayout = MultiTierLayout(),
) -> None:
    if len(tiers) == 0:
        return

    ratios = list(layout.tier_ratios)
    if len(ratios) < len(tiers):
        ratios.extend([ratios[-1]] * (len(tiers) - len(ratios)))
    ratios = ratios[: len(tiers)]

    total_h = layout.top - layout.bottom
    ratio_sum = sum(ratios)
    gaps_h = layout.tier_gap * (len(tiers) - 1)
    usable_h = total_h - gaps_h

    y_top = layout.top
    for ratio, chart in zip(ratios, tiers, strict=True):
        slot_h = usable_h * (ratio / ratio_sum)
        y = y_top - slot_h
        title_band = _chart_title_band(fig, chart, min_band=layout.min_title_band)
        ax_h = max(0.03, slot_h - title_band)
        ax = fig.add_axes((layout.left, y, layout.right - layout.left, ax_h))
        chart.draw(ax)
        y_top = y - layout.tier_gap
