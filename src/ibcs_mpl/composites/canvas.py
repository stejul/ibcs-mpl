"""Canvas layout with nodes, operators, and edge routing."""

from collections import defaultdict
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


__all__ = [
    "title_block_h_from_pt",
    "Box",
    "Node",
    "OperatorNode",
    "Edge",
    "CanvasStyle",
    "draw_canvas",
]


def title_block_h_from_pt(fig: matplotlib.figure.Figure, title_size_pt: float) -> float:
    """
    Compute the title-block height in figure-fraction from the font size in points.

    Reserves: one line of text (title_size_pt * 1.35 leading) plus 4 pt top padding.
    This replaces the hard-coded figure-fraction magic number so the result is
    consistent across figure sizes.
    """
    return pt_to_fig_y(fig, title_size_pt * 1.35 + 4.0)


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

    def top(self) -> float:
        return self.bottom + self.height

    def mid_y(self) -> float:
        return self.bottom + self.height / 2.0

    def mid_x(self) -> float:
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


def _operator_h_boundaries(fig: matplotlib.figure.Figure, op: OperatorNode) -> tuple[Point, Point]:
    """
    Return the exact left and right horizontal boundary points of the operator
    ellipse (including the gap clearance).  Used by the elbow router so that
    trunk and branch segments start/end flush with the circle perimeter.
    """
    rx = pt_to_fig_x(fig, op.radius_pt + op.gap_pt)
    ry = pt_to_fig_y(fig, op.radius_pt + op.gap_pt)
    cx, cy = op.center
    left_pt = _ellipse_boundary_point(op.center, (cx - 1.0, cy), rx, ry)
    right_pt = _ellipse_boundary_point(op.center, (cx + 1.0, cy), rx, ry)
    return left_pt, right_pt


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
            (
                b.left + style.inset_pad_x,
                b.bottom + style.inset_pad_bottom,
                b.width - 2 * style.inset_pad_x,
                b.height - style.title_block_h - style.inset_pad_bottom - style.inset_pad_top,
            )
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
                color="black",
                solid_capstyle="butt",
            )
        )

    # Group edges by operator so we draw each trunk exactly once.
    # op_id -> list of (src_node, dst_node)
    op_edges: dict[str, list[tuple[Node, Node]]] = defaultdict(list)
    direct_edges: list[tuple[Node, Node]] = []

    for e in edges:
        src_node = node_map[e.src]
        dst_node = node_map[e.dst]
        if e.op_id is not None and e.op_id in op_map:
            op_edges[e.op_id].append((src_node, dst_node))
        else:
            direct_edges.append((src_node, dst_node))

    # Direct edges (no operator): horizontal trunk then vertical then horizontal
    # (simple two-segment elbow using the x midpoint as the bend column).
    for src_node, dst_node in direct_edges:
        a = src_node.box.mid_right()
        dst_pt = dst_node.box.mid_left()
        mid_x = (a[0] + dst_pt[0]) / 2.0
        add_segment(a, (mid_x, a[1]))
        add_segment((mid_x, a[1]), (mid_x, dst_pt[1]))
        add_segment((mid_x, dst_pt[1]), dst_pt)

    # Operator edges: orthogonal H-tree routing.
    #
    # Each operator connects ONE source box (the "trunk" side) to ONE OR MORE
    # destination boxes (the "branch" side).  All edges sharing the same op_id
    # must have the same source box, so we derive it from the first entry.
    #
    # Routing pattern (all segments axis-aligned):
    #
    #   TRUNK:
    #     src.mid_right  ──h──►  op_left_boundary
    #
    #   BRANCH per destination:
    #     op_right_boundary  ──h──►  (corner_x, op_y)
    #                                      │ v
    #                                (corner_x, dst_mid_y)
    #                                      ──h──►  dst.mid_left
    #
    # corner_x is the horizontal midpoint between the operator right boundary
    # and the destination box left edge.  When multiple destinations share the
    # same op_id they share the same corner_x (all dst boxes have the same left
    # edge in the ROA tree) so the vertical segments are neatly stacked.

    for op_id, pairs in op_edges.items():
        op = op_map[op_id]
        op_left, op_right = _operator_h_boundaries(fig, op)

        # Derive the single source node (all pairs for one op share one source).
        src_node = pairs[0][0]
        src_pt = src_node.box.mid_right()

        # TRUNK: horizontal from source mid-right to operator left boundary.
        # The operator is always positioned at the source box mid_y so this
        # segment is perfectly horizontal.
        add_segment(src_pt, op_left)

        # Compute corner_x once: midpoint between op_right.x and dst.left.
        # All destinations in this group share the same left edge.
        dst_left_x = pairs[0][1].box.left
        corner_x = op_right[0] + 0.5 * (dst_left_x - op_right[0])

        # BRANCHES: right boundary → corner column → dst mid_y → dst mid_left.
        for _, dst_node in pairs:
            dst_pt = dst_node.box.mid_left()
            op_y = op_right[1]  # operator centre y (same as src mid_y)

            # Horizontal stub out of the operator to the corner column.
            add_segment(op_right, (corner_x, op_y))
            # Vertical run to destination y.
            add_segment((corner_x, op_y), (corner_x, dst_pt[1]))
            # Horizontal run into the destination box.
            add_segment((corner_x, dst_pt[1]), dst_pt)
