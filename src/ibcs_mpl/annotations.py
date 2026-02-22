from dataclasses import dataclass
from typing import Sequence

import matplotlib.axes
from matplotlib.patches import Rectangle

from ibcs_mpl.theme import FillStyle


@dataclass(frozen=True, slots=True)
class LegendItem:
    label: str
    style: FillStyle


@dataclass(frozen=True, slots=True)
class CommentRef:
    index: int
    x: float
    y: float
    text: str


def draw_inline_legend(
    ax: matplotlib.axes.Axes,
    *,
    items: Sequence[LegendItem],
    x: float,
    y: float,
    dy: float = 0.08,
    swatch_w: float = 0.03,
    swatch_h: float = 0.04,
    fontsize: int = 9,
) -> None:
    for idx, item in enumerate(items):
        yy = y - idx * dy
        ax.add_patch(
            Rectangle(
                (x, yy - swatch_h / 2.0),
                swatch_w,
                swatch_h,
                transform=ax.transAxes,
                facecolor=item.style.facecolor if item.style.facecolor else "none",
                edgecolor=item.style.edgecolor,
                hatch=item.style.hatch,
                linewidth=item.style.linewidth,
                clip_on=False,
            )
        )
        ax.text(
            x + swatch_w + 0.01,
            yy,
            item.label,
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=fontsize,
            clip_on=False,
        )


def draw_comment_refs(
    ax: matplotlib.axes.Axes, comments: Sequence[CommentRef], *, fontsize: int = 8
) -> None:
    for c in comments:
        ax.annotate(
            str(c.index),
            (c.x, c.y),
            xytext=(4, 4),
            textcoords="offset points",
            fontsize=fontsize,
            bbox={"boxstyle": "circle,pad=0.15", "fc": "white", "ec": "#5D9CEC", "lw": 1.0},
        )
        ax.text(
            c.x,
            c.y,
            c.text,
            fontsize=fontsize,
            va="top",
            ha="left",
            alpha=0.0,
        )
