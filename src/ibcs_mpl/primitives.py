"""Low-level drawing primitives shared across charts."""

from dataclasses import dataclass
from typing import Sequence

import matplotlib.axes
import matplotlib.figure
import matplotlib.patches as mpatches

from ibcs_mpl.theme import IBCSTheme
from ibcs_mpl.titles import MessageBlock, draw_title_message_block


__all__ = [
    "minimal_axes",
    "add_title_block",
    "DataLabels",
    "rect",
]


def minimal_axes(ax: matplotlib.axes.Axes, theme: IBCSTheme) -> None:
    """Remove spines and grid to create a clean IBCS axis."""
    ax.grid(False)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", left=False, labelleft=False)
    ax.tick_params(axis="x", labelsize=theme.label_size)


def add_title_block(
    fig: matplotlib.figure.Figure,
    ax: matplotlib.axes.Axes,
    title: str,
    subtitle: str | None,
    theme: IBCSTheme,
    *,
    message: MessageBlock | None = None,
    top_pad: float = 0.012,
    title_to_subtitle_gap: float = 0.020,
) -> None:
    """Draw title, subtitle, and optional message block above an Axes."""
    draw_title_message_block(
        fig,
        ax,
        title=title,
        subtitle=subtitle,
        theme=theme,
        message=message,
        top_pad=top_pad,
        title_to_subtitle_gap=title_to_subtitle_gap,
    )


@dataclass(frozen=True)
class DataLabels:
    """Configurable data-label formatter for bar/column values."""

    fmt: str = "{:,.0f}"

    def draw_above_bars(
        self,
        ax: matplotlib.axes.Axes,
        x: Sequence[float],
        y: Sequence[float],
        pad: float = 3.0,
    ) -> None:
        for xi, yi in zip(x, y, strict=True):
            va = "bottom" if yi >= 0 else "top"
            dy = pad if yi >= 0 else -pad
            ax.annotate(
                self.fmt.format(yi),
                (xi, yi),
                xytext=(0, dy),
                textcoords="offset points",
                ha="center",
                va=va,
                fontsize=9,
            )

    def draw_right_of_bars(
        self,
        ax: matplotlib.axes.Axes,
        y: Sequence[float],
        x: Sequence[float],
        pad: float = 3.0,
    ) -> None:
        for yi, xi in zip(y, x, strict=True):
            ha = "left" if xi >= 0 else "right"
            dx = pad if xi >= 0 else -pad
            ax.annotate(
                self.fmt.format(xi),
                (xi, yi),
                xytext=(dx, 0),
                textcoords="offset points",
                ha=ha,
                va="center",
                fontsize=9,
            )


def rect(
    x: float,
    y: float,
    w: float,
    h: float,
    facecolor: str | None,
    edgecolor: str,
    linewidth: float,
    hatch: str | None,
) -> mpatches.Rectangle:
    """Create a matplotlib Rectangle patch."""
    return mpatches.Rectangle(
        (x, y), w, h, facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth, hatch=hatch
    )
