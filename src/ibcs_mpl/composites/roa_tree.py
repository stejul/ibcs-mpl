"""Return-on-Assets tree composite layout."""

from dataclasses import dataclass
from typing import Sequence

import matplotlib.figure

from ibcs_mpl.composites.canvas import (
    Box,
    Node,
    OperatorNode,
    Edge,
    CanvasStyle,
    draw_canvas,
    title_block_h_from_pt,
)
from ibcs_mpl.composites.units import pt_to_fig_y
from ibcs_mpl.charts.columns import SingleColumnChart
from ibcs_mpl.theme import IBCSTheme
from ibcs_mpl.types import ScenarioCode


__all__ = [
    "ROATreeData",
    "ROATreeLayout",
    "build_roa_tree",
]


@dataclass(frozen=True)
class ROATreeData:
    years: Sequence[str]

    # left KPI
    roa_pct: Sequence[float]

    # middle KPIs
    ros_pct: Sequence[float]  # return on sales
    asset_turnover: Sequence[float]  # sales/assets ratio

    # right KPIs (drivers)
    return_meur: Sequence[float]
    sales_meur: Sequence[float]
    assets_meur: Sequence[float]

    # scenario coding for each series (common in your example: AC then PL)
    scenario_roa: ScenarioCode = ScenarioCode.AC
    scenario_ros: ScenarioCode = ScenarioCode.AC
    scenario_turn: ScenarioCode = ScenarioCode.AC
    scenario_return: ScenarioCode = ScenarioCode.AC
    scenario_sales: ScenarioCode = ScenarioCode.AC
    scenario_assets: ScenarioCode = ScenarioCode.AC


@dataclass(frozen=True)
class ROATreeLayout:
    """All boxes and operator positions in figure coords [0..1]."""

    roa: Box
    ros: Box
    turn: Box
    ret: Box
    sales: Box
    assets: Box

    op_mul: OperatorNode
    op_div_ros: OperatorNode
    op_div_turn: OperatorNode

    @staticmethod
    def default() -> "ROATreeLayout":
        # ── Column positions ─────────────────────────────────────────────────
        # Three columns with comfortable horizontal gaps.
        #
        #   col_left  col_mid   col_right
        #   [0.03]    [0.42]    [0.68]
        #
        # The left ("root") box is dominant in height – it spans nearly the
        # full usable figure height to make ROA visually prominent.
        # The middle column has two equal boxes; the right column has three.
        # All boxes share the same top (0.92) and bottom (0.06) boundary so
        # horizontal alignment of axes is clean.

        TOP = 0.92
        BOT = 0.06
        TOTAL_H = TOP - BOT  # 0.86

        # ── Left column: one tall dominant box ───────────────────────────────
        roa = Box(left=0.03, bottom=BOT, width=0.34, height=TOTAL_H)

        # ── Middle column: two equal boxes with a gap ─────────────────────
        MID_L = 0.42
        MID_W = 0.22
        MID_GAP = 0.04  # gap between the two middle boxes
        mid_each_h = (TOTAL_H - MID_GAP) / 2.0
        ros = Box(left=MID_L, bottom=BOT + mid_each_h + MID_GAP, width=MID_W, height=mid_each_h)
        turn = Box(left=MID_L, bottom=BOT, width=MID_W, height=mid_each_h)

        # ── Right column: three equal boxes with gaps ─────────────────────
        RIGHT_L = 0.69
        RIGHT_W = 0.29
        RIGHT_GAP = 0.03  # gap between the three right boxes
        right_each_h = (TOTAL_H - 2 * RIGHT_GAP) / 3.0
        ret = Box(
            left=RIGHT_L,
            bottom=BOT + 2 * (right_each_h + RIGHT_GAP),
            width=RIGHT_W,
            height=right_each_h,
        )
        sales = Box(
            left=RIGHT_L,
            bottom=BOT + right_each_h + RIGHT_GAP,
            width=RIGHT_W,
            height=right_each_h,
        )
        assets = Box(left=RIGHT_L, bottom=BOT, width=RIGHT_W, height=right_each_h)

        # ── Operator circles ──────────────────────────────────────────────
        # Every operator is placed at the EXACT mid-y of its source box so
        # that the trunk segment (source.mid_right → operator left boundary)
        # is perfectly horizontal.  X is the midpoint of the inter-column gap.

        # × : source = ROA, gap between ROA right edge and mid-col left edge.
        x_mul = (roa.mid_right()[0] + ros.mid_left()[0]) / 2.0
        y_mul = roa.mid_right()[1]  # == ROA.mid_y
        op_mul = OperatorNode(id="mul", kind="mul", center=(x_mul, y_mul), radius_pt=12, gap_pt=5)

        # ÷ circles: source = ROS and TURN respectively; gap between mid-col
        # right edge and right-col left edge.
        x_div = (ros.mid_right()[0] + ret.mid_left()[0]) / 2.0

        # div_ros y aligns with ROS.mid_y so the ROS trunk is horizontal.
        op_div_ros = OperatorNode(
            id="div_ros", kind="div", center=(x_div, ros.mid_right()[1]), radius_pt=12, gap_pt=5
        )
        # div_turn y aligns with TURN.mid_y so the TURN trunk is horizontal.
        op_div_turn = OperatorNode(
            id="div_turn", kind="div", center=(x_div, turn.mid_right()[1]), radius_pt=12, gap_pt=5
        )

        return ROATreeLayout(
            roa=roa,
            ros=ros,
            turn=turn,
            ret=ret,
            sales=sales,
            assets=assets,
            op_mul=op_mul,
            op_div_ros=op_div_ros,
            op_div_turn=op_div_turn,
        )


def _default_canvas_style(fig: matplotlib.figure.Figure, title_size_pt: float) -> CanvasStyle:
    """
    Build a CanvasStyle whose vertical padding is derived from the actual figure
    height rather than hard-coded figure-fraction magic numbers.

    - title_block_h: one text line of `title_size_pt` with 1.35× leading + 4 pt top pad
    - inset_pad_bottom: enough room for x-tick labels at `label_size_pt` (≈ 6 pt)
      plus 2 pt breathing room
    - inset_pad_top: a small gap between the bars and the top of the axes area
    - inset_pad_x: symmetric horizontal inset so bars don't touch the box edge
    """
    label_size_pt = title_size_pt - 2.0  # tick labels are a bit smaller than titles
    title_block_h = title_block_h_from_pt(fig, title_size_pt)
    inset_pad_bottom = pt_to_fig_y(fig, label_size_pt * 1.5 + 2.0)
    inset_pad_top = pt_to_fig_y(fig, 3.0)
    inset_pad_x = 0.008

    return CanvasStyle(
        frame_linewidth=0.8,
        connector_linewidth=0.8,
        title_size=int(title_size_pt),
        inset_pad_x=inset_pad_x,
        inset_pad_top=inset_pad_top,
        inset_pad_bottom=inset_pad_bottom,
        title_block_h=title_block_h,
        title_pad_top=pt_to_fig_y(fig, 4.0),
    )


def build_roa_tree(
    fig: matplotlib.figure.Figure,
    data: ROATreeData,
    *,
    layout: ROATreeLayout | None = None,
    style: CanvasStyle | None = None,
) -> None:
    lay = layout or ROATreeLayout.default()

    # Title size used for node labels.  All padding is derived from this so
    # the layout is consistent regardless of figure size.
    TITLE_PT = 9.0
    canvas_style = style or _default_canvas_style(fig, TITLE_PT)

    # Per-column mini themes.
    # The dominant left box is large enough for slightly bigger text.
    # The three right-column boxes are the smallest – use tighter label size
    # to keep tick labels readable without overlapping on 7 categories.
    roa_theme = IBCSTheme(font_size=9, title_size=9, label_size=8)
    mid_theme = IBCSTheme(font_size=8, title_size=9, label_size=7)
    right_theme = IBCSTheme(font_size=7, title_size=9, label_size=6)

    no_labels = None

    roa_chart = SingleColumnChart(
        title="",
        categories=data.years,
        values=data.roa_pct,
        scenario=data.scenario_roa,
        labels=no_labels,
        theme=roa_theme,
    )
    ros_chart = SingleColumnChart(
        title="",
        categories=data.years,
        values=data.ros_pct,
        scenario=data.scenario_ros,
        labels=no_labels,
        theme=mid_theme,
    )
    turn_chart = SingleColumnChart(
        title="",
        categories=data.years,
        values=data.asset_turnover,
        scenario=data.scenario_turn,
        labels=no_labels,
        theme=mid_theme,
    )
    ret_chart = SingleColumnChart(
        title="",
        categories=data.years,
        values=data.return_meur,
        scenario=data.scenario_return,
        labels=no_labels,
        theme=right_theme,
    )
    sales_chart = SingleColumnChart(
        title="",
        categories=data.years,
        values=data.sales_meur,
        scenario=data.scenario_sales,
        labels=no_labels,
        theme=right_theme,
    )
    assets_chart = SingleColumnChart(
        title="",
        categories=data.years,
        values=data.assets_meur,
        scenario=data.scenario_assets,
        labels=no_labels,
        theme=right_theme,
    )

    nodes = [
        Node("roa", "Return on assets in %", roa_chart, lay.roa),
        Node("ros", "Return on sales in %", ros_chart, lay.ros),
        Node("turn", "Asset turnover", turn_chart, lay.turn),
        Node("ret", "Return in mEUR", ret_chart, lay.ret),
        Node("sales", "Net sales in mEUR", sales_chart, lay.sales),
        Node("assets", "Assets in mEUR", assets_chart, lay.assets),
    ]

    operators = [lay.op_mul, lay.op_div_ros, lay.op_div_turn]

    edges = [
        # ROA → × → ROS (upper) and TURN (lower)
        Edge("roa", "ros", op_id="mul"),
        Edge("roa", "turn", op_id="mul"),
        # ROS → ÷ → Return (upper) and Sales (lower)
        Edge("ros", "ret", op_id="div_ros"),
        Edge("ros", "sales", op_id="div_ros"),
        # TURN → ÷ → Sales (upper) and Assets (lower)
        Edge("turn", "sales", op_id="div_turn"),
        Edge("turn", "assets", op_id="div_turn"),
    ]

    draw_canvas(
        fig,
        nodes=nodes,
        operators=operators,
        edges=edges,
        style=canvas_style,
    )
