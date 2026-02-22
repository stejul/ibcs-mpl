import pathlib
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def export() -> None:
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))

    from ibcs_mpl.charts import (
        GroupedBarChart,
        RelativeVariancePinChart,
        SingleColumnChart,
        VerticalWaterfallChart,
    )
    from ibcs_mpl.composites.roa_tree import ROATreeData, build_roa_tree
    from ibcs_mpl.types import ScenarioCode

    out = ROOT / "docs" / "images"
    out.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    SingleColumnChart(
        title="Accounts receivable",
        subtitle="Aug..Apr (mUSD)",
        categories=["Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr"],
        values=[653, 1040, 943, 737, 898, 985, 1150, 984, 943],
        scenario=ScenarioCode.AC,
    ).draw(ax)
    plt.subplots_adjust(top=0.80)
    fig.savefig(out / "single-column.svg")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8.6, 3.2))
    RelativeVariancePinChart(
        title="Sales variance",
        subtitle="ΔPY% (monthly)",
        categories=["Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"],
        rel_variance_pct=[-8.0, 5.0, 2.5, -3.0, 0.0, 7.2, -1.1, 4.0],
    ).draw(ax)
    plt.subplots_adjust(top=0.80)
    fig.savefig(out / "relative-variance-pins.svg")
    plt.close(fig)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))
    GroupedBarChart(
        title="Contribution",
        subtitle="AC vs PY (kEUR)",
        categories=["Berlin", "Paris", "Rome", "Vienna"],
        primary_values=[620, 795, 618, 720],
        reference_values=[592, 759, 575, 690],
    ).draw(ax1)
    VerticalWaterfallChart(
        title="EBIT Bridge",
        subtitle="AC variance walk (mEUR)",
        categories=["PY", "Volume", "Price", "Cost", "AC"],
        values=[42.0, 6.5, 3.0, -4.0, 47.5],
        is_total=[True, False, False, False, True],
    ).draw(ax2)
    plt.subplots_adjust(top=0.78, wspace=0.28)
    fig.savefig(out / "grouped-bar-and-waterfall.svg")
    plt.close(fig)

    years = ["'10", "'11", "'12", "'13", "'14", "'15", "'16"]
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
    fig = plt.figure(figsize=(16, 9.5))
    fig.suptitle(
        "We plan to achieve an ROA of around 19% in 2016\ndespite increasing assets",
        x=0.02,
        y=0.99,
        ha="left",
        fontsize=14,
    )
    build_roa_tree(fig, data)
    fig.savefig(out / "roa-tree.svg")
    plt.close(fig)


if __name__ == "__main__":
    export()
