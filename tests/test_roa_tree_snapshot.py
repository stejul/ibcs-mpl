import hashlib
import json
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.figure
import matplotlib.pyplot as plt

from ibcs_mpl.composites.roa_tree import ROATreeData, build_roa_tree
from ibcs_mpl.types import ScenarioCode


def _round4(value: float) -> float:
    return round(float(value), 4)


def _roa_tree_signature(fig: matplotlib.figure.Figure) -> str:
    payload: dict[str, Any] = {
        "fig_size": [_round4(v) for v in fig.get_size_inches()],
        "axes": [],
        "figure_texts": [],
        "figure_lines": len(fig.lines),
        "figure_patches": len(fig.patches),
    }

    for ax in fig.axes:
        bbox = ax.get_position()
        payload["axes"].append(
            {
                "bbox": [
                    _round4(bbox.x0),
                    _round4(bbox.y0),
                    _round4(bbox.width),
                    _round4(bbox.height),
                ],
                "patches": len(ax.patches),
                "lines": len(ax.lines),
                "texts": len(ax.texts),
                "xlim": [_round4(v) for v in ax.get_xlim()],
                "ylim": [_round4(v) for v in ax.get_ylim()],
            }
        )

    for text in fig.texts:
        payload["figure_texts"].append(
            {
                "s": text.get_text(),
                "x": _round4(text.get_position()[0]),
                "y": _round4(text.get_position()[1]),
                "ha": text.get_ha(),  # type: ignore[attr-defined]
                "va": text.get_va(),  # type: ignore[attr-defined]
            }
        )

    blob = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def test_roa_tree_layout_snapshot() -> None:
    years = ["Y10", "Y11", "Y12", "Y13", "Y14", "Y15", "Y16"]
    data = ROATreeData(
        years=years,
        roa_pct=[24.9, -9.7, -17.8, 14.7, 17.9, 19.2, 18.9],
        ros_pct=[19.2, -7.0, -13.1, 14.0, 17.2, 19.8, 22.5],
        asset_turnover=[1.3, 1.4, 1.4, 1.0, 1.0, 1.0, 0.8],
        return_meur=[5.0, -1.8, -3.5, 3.1, 4.1, 4.7, 5.3],
        sales_meur=[26.1, 25.7, 26.4, 22.1, 23.8, 23.7, 23.6],
        assets_meur=[20.1, 18.5, 19.4, 21.1, 22.9, 24.5, 28.0],
        scenario_roa=ScenarioCode.AC,
        scenario_ros=ScenarioCode.AC,
        scenario_turn=ScenarioCode.AC,
        scenario_return=ScenarioCode.AC,
        scenario_sales=ScenarioCode.AC,
        scenario_assets=ScenarioCode.AC,
    )

    fig = plt.figure(figsize=(14, 8))
    fig.suptitle(
        "We plan to achieve an ROA of around 19% in 2016\ndespite increasing assets",
        x=0.02,
        y=0.99,
        ha="left",
        fontsize=14,
    )
    build_roa_tree(fig, data)

    digest = _roa_tree_signature(fig)
    plt.close(fig)

    assert digest == "d20c0eada608efc71ce70f114c540cdd2f2979428e5a6c790024eede4107b7cc"
