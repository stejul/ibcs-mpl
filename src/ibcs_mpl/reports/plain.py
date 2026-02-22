from typing import Any, Sequence

from ibcs_mpl.tables import Table, ColumnSpec, TableStyle
from ibcs_mpl.tables.cells import TextCell, NumberCell, PercentCell


def build_plain_report_table(
    *,
    rows: Sequence[dict[str, Any]],
    style: TableStyle | None = None,
) -> Table:
    columns = [
        ColumnSpec(key="name", title="Item", width=2.4, renderer=TextCell()),
        ColumnSpec(key="revenue", title="Revenue (EUR)", width=1.3, renderer=NumberCell(fmt="{:,.0f}")),
        ColumnSpec(key="gm", title="Gross margin", width=1.1, renderer=PercentCell(decimals=1)),
        ColumnSpec(key="fte", title="FTE", width=0.8, renderer=NumberCell(fmt="{:,.0f}")),
    ]
    return Table(columns=columns, rows=rows, style=style or TableStyle())
