import hashlib
import json
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.axes
import matplotlib.pyplot as plt

from ibcs_mpl.charts import (
    GroupedBarChart,
    GroupedColumnChart,
    HorizontalWaterfallChart,
    RelativeVariancePinChart,
    SingleColumnChart,
    StackedBarChart,
    VerticalWaterfallChart,
)


def _rounded(values: list[float], digits: int = 4) -> list[float]:
    return [round(float(v), digits) for v in values]


def _artist_snapshot(ax: matplotlib.axes.Axes) -> str:
    payload: dict[str, Any] = {
        "xlim": _rounded([*ax.get_xlim()]),
        "ylim": _rounded([*ax.get_ylim()]),
        "xticks": _rounded(list(ax.get_xticks())),
        "yticks": _rounded(list(ax.get_yticks())),
        "patches": [],
        "lines": [],
    }

    for patch in ax.patches:
        payload["patches"].append(
            {
                "x": round(float(patch.get_x()), 4),  # type: ignore[attr-defined]
                "y": round(float(patch.get_y()), 4),  # type: ignore[attr-defined]
                "w": round(float(patch.get_width()), 4),  # type: ignore[attr-defined]
                "h": round(float(patch.get_height()), 4),  # type: ignore[attr-defined]
                "fc": tuple(round(float(v), 3) for v in patch.get_facecolor()),  # type: ignore[arg-type]
                "ec": tuple(round(float(v), 3) for v in patch.get_edgecolor()),  # type: ignore[arg-type]
                "lw": round(float(patch.get_linewidth()), 3),
                "hatch": patch.get_hatch() or "",
            }
        )

    for line in ax.lines:
        x_data = _rounded([float(v) for v in line.get_xdata()])  # type: ignore
        y_data = _rounded([float(v) for v in line.get_ydata()])  # type: ignore
        payload["lines"].append(
            {
                "x": x_data,
                "y": y_data,
                "lw": round(float(line.get_linewidth()), 3),
                "color": line.get_color(),
            }
        )

    blob = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


EXPECTED_SNAPSHOTS = {
    "single_column": "75740cdc761c75169c33c7b65729d8a766ae8238065cef0f848a55fd1c27a0eb",
    "grouped_column": "fa1d02773cc24615b6e3865111e0433f4b035df5d9a3b4d545bbde404326e200",
    "grouped_bar": "9b2f8ecdaa446412d4d5b0f876adf9db9e8908ef1a93ca415f43971672af0628",
    "stacked_bar": "c1e4c609bae6a37ccb34ddf110d37ed3f8b9873126198ccb19d5d13d5a6f6310",
    "relative_variance_pin": "f70cf409f9c8d4be60daed37610d56bf332e0faea5fa3d6edb0f8e906de0818c",
    "vertical_waterfall": "5c9b94412991877ab882c799242dbf321a1eaf72f15281b771ce4e18b02ba4e1",
    "horizontal_waterfall": "71cf54180fe5b9c7e84563c59494e1d8bddc45d83560e9cdd982b734ecddf549",
}


def test_visual_snapshots() -> None:
    charts = {
        "single_column": SingleColumnChart(
            title="t", categories=["Jan", "Feb", "Mar"], values=[10, 15, 12]
        ),
        "grouped_column": GroupedColumnChart(
            title="t",
            categories=["Jan", "Feb", "Mar"],
            primary_values=[10, 15, 12],
            reference_values=[9, 14, 11],
        ),
        "grouped_bar": GroupedBarChart(
            title="t",
            categories=["A", "B", "C"],
            primary_values=[10, 7, 11],
            reference_values=[9, 8, 10],
        ),
        "stacked_bar": StackedBarChart(
            title="t",
            categories=["A", "B", "C"],
            stack_labels=["L1", "L2"],
            stack_values=[[5, 3, 4], [2, 4, 1]],
        ),
        "relative_variance_pin": RelativeVariancePinChart(
            title="t",
            categories=["Jan", "Feb", "Mar"],
            rel_variance_pct=[-3.5, 2.0, 5.5],
        ),
        "vertical_waterfall": VerticalWaterfallChart(
            title="t",
            categories=["Start", "+A", "-B", "End"],
            values=[100, 15, -8, 107],
            is_total=[True, False, False, True],
        ),
        "horizontal_waterfall": HorizontalWaterfallChart(
            title="t",
            categories=["Start", "+A", "-B", "End"],
            values=[100, 15, -8, 107],
            is_total=[True, False, False, True],
        ),
    }

    for key, chart in charts.items():
        fig, ax = plt.subplots(figsize=(6.0, 3.0))
        chart.draw(ax)  # type: ignore[attr-defined]
        digest = _artist_snapshot(ax)
        plt.close(fig)
        assert digest == EXPECTED_SNAPSHOTS[key]
