from dataclasses import dataclass
from typing import Sequence

import matplotlib.figure

from ibcs_mpl.composites.canvas import Box, Node, OperatorNode, Edge, CanvasStyle, draw_canvas
from ibcs_mpl.charts.columns import SingleColumnChart
from ibcs_mpl.theme import IBCSTheme
from ibcs_mpl.types import ScenarioCode


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
    """All boxes and operator positions in figure coords."""

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
        roa = Box(0.04, 0.26, 0.35, 0.42)

        ros = Box(0.41, 0.52, 0.24, 0.24)
        turn = Box(0.41, 0.20, 0.24, 0.24)

        ret = Box(0.68, 0.70, 0.29, 0.20)
        sales = Box(0.68, 0.44, 0.29, 0.20)
        assets = Box(0.68, 0.18, 0.29, 0.20)

        # 1) MUL circle: centered between ROS and TURN vertically
        y_mul = (ros.mid_left()[1] + turn.mid_left()[1]) / 2.0

        # place it in the horizontal gap between ROA and middle column
        # 45% into the gap from ROA right edge towards ROS left edge:
        x_mul = roa.mid_right()[0] + 0.45 * (ros.mid_left()[0] - roa.mid_right()[0])

        op_mul = OperatorNode(id="mul", kind="mul", center=(x_mul, y_mul), radius_pt=11, gap_pt=4)

        # 2) DIV circle for ROS: centered vertically between Return and Sales
        y_div_ros = (ret.mid_left()[1] + sales.mid_left()[1]) / 2.0
        x_div = ros.mid_right()[0] + 0.45 * (ret.mid_left()[0] - ros.mid_right()[0])
        op_div_ros = OperatorNode(
            id="div_ros", kind="div", center=(x_div, y_div_ros), radius_pt=11, gap_pt=4
        )

        # 3) DIV circle for Turnover: centered vertically between Sales and Assets
        y_div_turn = (sales.mid_left()[1] + assets.mid_left()[1]) / 2.0
        op_div_turn = OperatorNode(
            id="div_turn", kind="div", center=(x_div, y_div_turn), radius_pt=11, gap_pt=4
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


def build_roa_tree(
    fig: matplotlib.figure.Figure,
    data: ROATreeData,
    *,
    layout: ROATreeLayout | None = None,
    style: CanvasStyle | None = None,
) -> None:
    lay = layout or ROATreeLayout.default()
    canvas_style = style or CanvasStyle(
        frame_linewidth=1.0,
        connector_linewidth=1.0,
        title_size=9,
        inset_pad_x=0.010,
        inset_pad_top=0.002,
        inset_pad_bottom=0.018,
        title_block_h=0.030,
        title_pad_top=0.012,
    )

    mini_theme = IBCSTheme(font_size=8, title_size=9, label_size=7)
    no_labels = None

    # Mini charts (you already have SingleColumnChart)
    # Titles should be inside the node frame (canvas), so chart title can be blank.
    roa_chart = SingleColumnChart(
        title="",
        categories=data.years,
        values=data.roa_pct,
        scenario=data.scenario_roa,
        labels=no_labels,
        theme=mini_theme,
    )
    ros_chart = SingleColumnChart(
        title="",
        categories=data.years,
        values=data.ros_pct,
        scenario=data.scenario_ros,
        labels=no_labels,
        theme=mini_theme,
    )
    turn_chart = SingleColumnChart(
        title="",
        categories=data.years,
        values=data.asset_turnover,
        scenario=data.scenario_turn,
        labels=no_labels,
        theme=mini_theme,
    )

    ret_chart = SingleColumnChart(
        title="",
        categories=data.years,
        values=data.return_meur,
        scenario=data.scenario_return,
        labels=no_labels,
        theme=mini_theme,
    )
    sales_chart = SingleColumnChart(
        title="",
        categories=data.years,
        values=data.sales_meur,
        scenario=data.scenario_sales,
        labels=no_labels,
        theme=mini_theme,
    )
    assets_chart = SingleColumnChart(
        title="",
        categories=data.years,
        values=data.assets_meur,
        scenario=data.scenario_assets,
        labels=no_labels,
        theme=mini_theme,
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

    # Elbow connectors (via operator centers)
    edges = [
        # ROA splits to ROS (upper) and Turnover (lower)
        Edge("roa", "ros", op_id="mul", src_anchor=0.62, dst_anchor=0.55),
        Edge("roa", "turn", op_id="mul", src_anchor=0.38, dst_anchor=0.45),
        # ROS splits to Return (upper) and Sales (lower)
        Edge("ros", "ret", op_id="div_ros", src_anchor=0.60, dst_anchor=0.55),
        Edge("ros", "sales", op_id="div_ros", src_anchor=0.40, dst_anchor=0.50),
        # Turnover splits to Sales (upper) and Assets (lower)
        Edge("turn", "sales", op_id="div_turn", src_anchor=0.60, dst_anchor=0.45),
        Edge("turn", "assets", op_id="div_turn", src_anchor=0.40, dst_anchor=0.50),
    ]

    draw_canvas(
        fig,
        nodes=nodes,
        operators=operators,
        edges=edges,
        style=canvas_style,
    )
