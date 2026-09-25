"""Page title and message block layout."""

from dataclasses import dataclass

import matplotlib.axes
import matplotlib.figure

from ibcs_mpl.theme import IBCSTheme


__all__ = [
    "PageTitle",
    "MessageBlock",
    "draw_title_message_block",
]


@dataclass(frozen=True, slots=True, kw_only=True)
class PageTitle:
    line1_reporting_unit: str
    line2_measure: str
    line3_context: str

    def render(self) -> str:
        return f"{self.line1_reporting_unit}\n{self.line2_measure}\n{self.line3_context}"


@dataclass(frozen=True, slots=True, kw_only=True)
class MessageBlock:
    text: str
    size: int = 12


def _text_height_fig(
    fig: matplotlib.figure.Figure,
    *,
    fontsize: int,
    lines: int,
    line_spacing: float = 1.20,
) -> float:
    if lines <= 0:
        return 0.0
    fig_h_in = float(fig.get_size_inches()[1])
    return ((fontsize / 72.0) / fig_h_in) * lines * line_spacing


def _block_lines(text: str | None) -> int:
    if not text:
        return 0
    return text.count("\n") + 1


def _gap_fig(fig: matplotlib.figure.Figure, *, points: float) -> float:
    fig_h_in = float(fig.get_size_inches()[1])
    return (points / 72.0) / fig_h_in


def draw_title_message_block(
    fig: matplotlib.figure.Figure,
    ax: matplotlib.axes.Axes,
    *,
    title: str,
    subtitle: str | None,
    theme: IBCSTheme,
    message: MessageBlock | None = None,
    top_pad: float = 0.012,
    title_to_subtitle_gap: float = 0.020,
    message_gap: float = 0.030,
) -> None:
    bbox = ax.get_position()
    x = bbox.x0

    title_lines = _block_lines(title)
    subtitle_lines = _block_lines(subtitle)
    message_lines = _block_lines(message.text if message else None)

    title_h = _text_height_fig(fig, fontsize=theme.title_size, lines=title_lines)
    subtitle_h = _text_height_fig(fig, fontsize=theme.font_size, lines=subtitle_lines)
    message_h = _text_height_fig(
        fig, fontsize=message.size if message else theme.title_size, lines=message_lines
    )

    subtitle_gap = max(
        title_to_subtitle_gap, _gap_fig(fig, points=max(3.0, theme.font_size * 0.30))
    )
    msg_gap = max(
        message_gap,
        _gap_fig(fig, points=max(4.0, (message.size if message else theme.title_size) * 0.35)),
    )

    required_above_axes = top_pad + title_h
    if subtitle:
        required_above_axes += subtitle_gap + subtitle_h
    if message is not None:
        required_above_axes += msg_gap + message_h

    top_limit = 0.995
    available_above_axes = top_limit - bbox.y1

    if required_above_axes > available_above_axes:
        overflow = required_above_axes - available_above_axes
        new_height = max(0.05, bbox.height - overflow)
        ax.set_position((bbox.x0, bbox.y0, bbox.width, new_height))
        bbox = ax.get_position()
        x = bbox.x0

    y_title_top = bbox.y1 + top_pad + title_h

    if message is not None:
        y_msg_top = y_title_top + msg_gap + message_h
        y_msg_top = min(y_msg_top, top_limit)
        fig.text(
            x,
            y_msg_top,
            message.text,
            ha="left",
            va="top",
            fontsize=message.size,
            fontweight="bold",
        )

    if title:
        fig.text(x, y_title_top, title, ha="left", va="top", fontsize=theme.title_size)
    if subtitle:
        y_sub_top = y_title_top - title_h - subtitle_gap
        fig.text(
            x,
            y_sub_top,
            subtitle,
            ha="left",
            va="top",
            fontsize=theme.font_size,
        )
