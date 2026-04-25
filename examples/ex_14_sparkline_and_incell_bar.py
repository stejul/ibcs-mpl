"""
ex_14 — SparklineCell and InCellBarCell in tables

Demonstrates:
- SparklineCell: miniature line chart inside a table cell
- InCellBarCell: scenario-styled bar inside a table cell
Both used alongside existing cell renderers in a variance-style report.
"""
import matplotlib.pyplot as plt

from ibcs_mpl.tables import ColumnSpec, Table, TableStyle
from ibcs_mpl.tables.cells import (
    InCellBarCell,
    NumberCell,
    SparklineCell,
    TextCell,
    VariancePercentCell,
)
from ibcs_mpl.types import ScenarioCode

ROWS = [
    {
        "region": "North",
        "ac": 820,
        "trend": [740, 760, 790, 810, 820],
        "delta_pct": 5.1,
        "ac_bar": 820,
    },
    {
        "region": "South",
        "ac": 650,
        "trend": [700, 680, 660, 655, 650],
        "delta_pct": -8.5,
        "ac_bar": 650,
    },
    {
        "region": "East",
        "ac": 740,
        "trend": [690, 700, 715, 730, 740],
        "delta_pct": 2.8,
        "ac_bar": 740,
    },
    {
        "region": "West",
        "ac": 910,
        "trend": [850, 870, 890, 900, 910],
        "delta_pct": 7.1,
        "ac_bar": 910,
    },
    {
        "region": "Central",
        "ac": 580,
        "trend": [610, 600, 590, 585, 580],
        "delta_pct": -4.9,
        "ac_bar": 580,
    },
]

columns = [
    ColumnSpec(key="region", title="Region", width=1.4, renderer=TextCell()),
    ColumnSpec(key="ac", title="AC (mEUR)", width=1.0, renderer=NumberCell(), header_ha="right"),
    ColumnSpec(key="trend", title="Trend (6M)", width=1.8,
               renderer=SparklineCell(show_endpoints=True), header_ha="center"),
    ColumnSpec(key="delta_pct", title="ΔPY%", width=0.8,
               renderer=VariancePercentCell(), header_ha="right"),
    ColumnSpec(key="ac_bar", title="AC vs 1000", width=1.6,
               renderer=InCellBarCell(max_abs=1000, scenario=ScenarioCode.AC),
               header_ha="center"),
]

table = Table(columns=columns, rows=ROWS, style=TableStyle(row_height=0.13, header_height=0.16))

fig, ax = plt.subplots(figsize=(12, 3.6))
table.draw(ax)
fig.suptitle("SparklineCell · InCellBarCell — new table cell renderers", fontsize=10, y=1.02)
plt.tight_layout()
plt.show()
