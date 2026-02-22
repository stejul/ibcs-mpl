from dataclasses import dataclass
from typing import Sequence, Literal

from ibcs_mpl.charts.base import Chart

import math

import matplotlib.figure
import matplotlib.axes
from matplotlib.patches import Rectangle, Ellipse
from matplotlib.lines import Line2D

from ibcs_mpl.types import Point
from ibcs_mpl.composites.units import pt_to_fig_x, pt_to_fig_y


@dataclass(frozen=True)
class Box:
    """Figure-coordinates box [0..1]."""

    left: float
    bottom: float
    width: float
    height: float

    def mid_left(self) -> Point:
        return (self.left, self.bottom + self.height / 2.0)

    def mid_right(self) -> Point:
        return (self.left + self.width, self.bottom + self.height / 2.0)

    # Optional: more control (use later if you want nicer routing)
    def left_at(self, frac: float) -> Point:
        return (self.left, self.bottom + self.height * frac)

    def right_at(self, frac: float) -> Point:
        return (self.left + self.width, self.bottom + self.height * frac)

    def top(self) -> Point:
        return self.bottom + self.height

    def mid_y(self) -> Point:
        return self.bottom + self.height / 2.0

    def mid_x(self) -> Point:
        return self.left + self.width / 2.0


@dataclass(frozen=True)
class Node:
    id: str
    title: str
    chart: Chart
    box: Box


@dataclass(frozen=True)
class OperatorNode:
    """
    Operator is drawn as a circle visually, but in figure coordinates it is an ellipse
    (because figure X/Y scales differ). We specify size in points so it's not "magic".
    """

    id: str
    kind: Literal["mul", "div"]
    center: Point

    radius_pt: float = 11.0  # concrete: points
    gap_pt: float = 4.0  # concrete: whitespace around circle for connectors


@dataclass(frozen=True)
class Edge:
    src: str
    dst: str
    op_id: str | None = None  # operator junction id; if None -> straight line
    src_anchor: float = 0.5
    dst_anchor: float = 0.5


@dataclass(frozen=True)
class CanvasStyle:
    frame_linewidth: float = 1.0
    connector_linewidth: float = 1.0
    title_size: int = 9

    inset_pad_x: float = 0.02
    inset_pad_top: float = 0.06
    inset_pad_bottom: float = 0.06

    title_pad_top: float = 0.018
    title_block_h: float = 0.050


def _operator_symbol(kind: str) -> str:
    return "×" if kind == "mul" else "÷"


def _ellipse_boundary_point(center: Point, toward: Point, rx: float, ry: float) -> Point:
    """
    Point on ellipse boundary along ray from center -> toward.

    Ellipse equation: (x/rx)^2 + (y/ry)^2 = 1
    Ray: center + t*(dx, dy)
    Solve for t: (t*dx/rx)^2 + (t*dy/ry)^2 = 1
      => t = 1 / sqrt((dx/rx)^2 + (dy/ry)^2)
    """
    cx, cy = center
    dx = toward[0] - cx
    dy = toward[1] - cy

    if abs(dx) < 1e-12 and abs(dy) < 1e-12:
        # degenerate: pick a point to the right
        return (cx + rx, cy)

    denom = math.sqrt((dx / rx) ** 2 + (dy / ry) ** 2)
    t = 1.0 / denom
    return (cx + dx * t, cy + dy * t)


def _operator_attach_points(
    fig: matplotlib.figure.Figure, src: Point, dst: Point, op: OperatorNode
) -> tuple[Point, Point]:
    """
    Compute where connectors should meet the operator circle boundary.
    Important: we DO NOT draw any segment inside the circle.
    """
    rx = pt_to_fig_x(fig, op.radius_pt + op.gap_pt)
    ry = pt_to_fig_y(fig, op.radius_pt + op.gap_pt)

    p_src = _ellipse_boundary_point(op.center, src, rx, ry)
    p_dst = _ellipse_boundary_point(op.center, dst, rx, ry)
    return p_src, p_dst


def _draw_operator(fig: matplotlib.figure.Figure, op: OperatorNode, *, lw: float = 1.0) -> None:
    # Draw operator as ellipse in figure coords so it appears circular on screen.
    rx = pt_to_fig_x(fig, op.radius_pt)
    ry = pt_to_fig_y(fig, op.radius_pt)

    fig.patches.append(
        Ellipse(
            op.center,
            width=2 * rx,
            height=2 * ry,
            transform=fig.transFigure,
            fill=False,
            linewidth=lw,
        )
    )
    fig.text(
        op.center[0], op.center[1], _operator_symbol(op.kind), ha="center", va="center", fontsize=10
    )


def draw_canvas(
    fig: matplotlib.figure.Figure,
    *,
    nodes: Sequence[Node],
    operators: Sequence[OperatorNode],
    edges: Sequence[Edge],
    style: CanvasStyle = CanvasStyle(),
) -> None:
    """
    Draw a composite canvas:
      - each Node gets a framed box + a child inset Axes that the chart draws into
      - operators are drawn in figure coordinates
      - edges are drawn in figure coordinates; when op_id is set we connect to the operator boundary
    """
    node_map = {n.id: n for n in nodes}
    op_map = {op.id: op for op in operators}

    # 1) Node frames + titles + inset axes
    for n in nodes:
        b = n.box

        fig.patches.append(
            Rectangle(
                (b.left, b.bottom),
                b.width,
                b.height,
                transform=fig.transFigure,
                fill=False,
                linewidth=style.frame_linewidth,
            )
        )

        fig.text(
            b.left + 0.01,
            b.bottom + b.height - style.title_pad_top,
            n.title,
            ha="left",
            va="top",
            fontsize=style.title_size,
        )

        ax = fig.add_axes(
            [
                b.left + style.inset_pad_x,
                b.bottom + style.inset_pad_bottom,
                b.width - 2 * style.inset_pad_x,
                b.height - style.title_block_h - style.inset_pad_bottom - style.inset_pad_top,
            ]
        )
        n.chart.draw(ax)

    # 2) Operators
    for op in operators:
        _draw_operator(fig, op, lw=style.frame_linewidth)

    # 3) Connectors
    def add_segment(a: Point, b: Point) -> None:
        fig.lines.append(
            Line2D(
                [a[0], b[0]],
                [a[1], b[1]],
                transform=fig.transFigure,
                linewidth=style.connector_linewidth,
            )
        )

    for e in edges:
        src = node_map[e.src]
        dst = node_map[e.dst]

        a = src.box.right_at(e.src_anchor)
        b = dst.box.left_at(e.dst_anchor)

        if e.op_id is None:
            add_segment(a, b)
            continue

        op = op_map.get(e.op_id)
        if op is None:
            add_segment(a, b)
            continue

        p_src, p_dst = _operator_attach_points(fig, a, b, op)

        # dont draw p_src -> p_dst (would cross the operator symbol)
        add_segment(a, p_src)
        add_segment(p_dst, b)
