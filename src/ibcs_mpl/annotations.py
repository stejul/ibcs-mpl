from dataclasses import dataclass
from typing import Sequence

import matplotlib.axes
from matplotlib.patches import Rectangle

from ibcs_mpl.theme import FillStyle


def _legend_fits_at(
    ax: matplotlib.axes.Axes,
    x: float,
    y: float,
    width: float,
    height: float,
) -> bool:
    """Check whether a legend box in axes-fraction coords avoids the data bounding box."""
    try:
        renderer = ax.figure.canvas.get_renderer()
        data_bbox = ax.dataLim
        # Convert data bbox to axes fraction
        inv = ax.transAxes.inverted()
        ll = inv.transform(ax.transData.transform((data_bbox.x0, data_bbox.y0)))
        ur = inv.transform(ax.transData.transform((data_bbox.x1, data_bbox.y1)))
        # Check overlap
        legend_r = x + width
        legend_t = y + height
        data_l, data_b = min(ll[0], ur[0]), min(ll[1], ur[1])
        data_r, data_t = max(ll[0], ur[0]), max(ll[1], ur[1])
        overlap = (x < data_r and legend_r > data_l and y < data_t and legend_t > data_b)
        return not overlap
    except Exception:
        return True


def find_legend_position(
    ax: matplotlib.axes.Axes,
    width: float = 0.18,
    height: float = 0.20,
    candidates: Sequence[tuple[float, float]] | None = None,
) -> tuple[float, float]:
    """Return (x, y) in axes-fraction coords for a legend that avoids chart data.

    Tries candidate positions in order and returns the first that does not overlap
    the data bounding box. Falls back to top-right if all overlap.
    """
    if candidates is None:
        candidates = [
            (0.78, 0.78),  # top-right
            (0.02, 0.78),  # top-left
            (0.02, 0.02),  # bottom-left
            (0.78, 0.02),  # bottom-right
            (0.40, 0.78),  # top-center
        ]
    for x, y in candidates:
        if _legend_fits_at(ax, x, y, width, height):
            return x, y
    return candidates[0]


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
