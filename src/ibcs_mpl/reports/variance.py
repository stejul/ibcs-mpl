"""Variance report table builder with Δ…% and pin cells."""

from typing import Any, Sequence

from ibcs_mpl.tables import Table, ColumnSpec, TableStyle
from ibcs_mpl.tables.cells import (
    TextCell,
    NumberCell,
    VarianceNumberCell,
    VariancePercentCell,
    RelativeVariancePinCell,
)
from ibcs_mpl.types import ScenarioCode, ReferenceScenario


__all__ = [
    "build_variance_table",
]


def _relative_variance_pct(minuend: float, ref: float) -> float | None:
    """
    Δ…% = (minuend - ref) / ref * 100

    Per guide: show 'n.a.' when result cannot be interpreted, often when comparing
    positive to negative reference (denominator).
    """
    if ref == 0:
        return None
    # typical "not interpretable" case: opposite signs
    if (minuend > 0 and ref < 0) or (minuend < 0 and ref > 0):
        return None
    return (minuend - ref) / ref * 100.0


def build_variance_table(
    *,
    rows: Sequence[dict[str, Any]],
    minuend_key: str = "ac",
    reference_key: str = "py",
    minuend_scenario: ScenarioCode = ScenarioCode.AC,
    reference_scenario: ReferenceScenario = ReferenceScenario.PY,
    style: TableStyle | None = None,
) -> Table:
    d_title = f"Δ{reference_scenario.value}"
    dp_title = f"Δ{reference_scenario.value}%"

    computed: list[dict[str, Any]] = []
    max_abs_d = 0.0
    max_abs_dp = 0.0

    for r in rows:
        minuend = float(r[minuend_key])
        ref = float(r[reference_key])

        d = minuend - ref
        dp = _relative_variance_pct(minuend, ref)

        max_abs_d = max(max_abs_d, abs(d))
        if dp is not None:
            max_abs_dp = max(max_abs_dp, abs(dp))

        computed.append({**r, "d": d, "dp": dp, "dp_pin": dp})

    max_abs_d = max_abs_d if max_abs_d > 0 else 1.0
    max_abs_dp = max_abs_dp if max_abs_dp > 0 else 1.0

    columns = [
        ColumnSpec(
            key="name",
            title="Item",
            width=2.6,
            renderer=TextCell(),
            gap_after=0.30,
            header_ha="left",
        ),
        ColumnSpec(
            key=minuend_key,
            title=minuend_scenario.value,
            width=1.0,
            renderer=NumberCell(fmt="{:,.0f}"),
            header_ha="right",
        ),
        ColumnSpec(
            key=reference_key,
            title=reference_scenario.value,
            width=1.0,
            renderer=NumberCell(fmt="{:,.0f}"),
            gap_after=0.25,
            header_ha="right",
        ),
        ColumnSpec(
            key="d",
            title=d_title,
            width=1.0,
            renderer=VarianceNumberCell(fmt="{:+,.0f}"),
            header_ha="right",
        ),
        ColumnSpec(
            key="dp",
            title=dp_title,
            width=1.0,
            renderer=VariancePercentCell(decimals=1),
            gap_after=0.20,
            header_ha="right",
        ),
        ColumnSpec(
            key="dp_pin",
            title="",
            width=1.2,
            renderer=RelativeVariancePinCell(
                max_abs_pct=max_abs_dp,
                minuend=minuend_scenario,
                reference=reference_scenario,
            ),
            header_ha="center",
        ),
    ]

    return Table(columns=columns, rows=computed, style=style or TableStyle())
