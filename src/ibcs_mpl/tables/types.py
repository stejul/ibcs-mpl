"""Table geometry types and style definitions."""

from dataclasses import dataclass
from typing import Any, Protocol, Literal

import matplotlib.axes


__all__ = [
    "Rect",
    "CellRenderer",
    "ColumnSpec",
    "TableStyle",
]


@dataclass(frozen=True, slots=True)
class Rect:
    """Rectangle in axes coordinates [0..1]."""

    x: float
    y: float
    w: float
    h: float


class CellRenderer(Protocol):
    """Protocol for table cell renderers."""

    def draw(self, ax: matplotlib.axes.Axes, rect: Rect, value: Any) -> None: ...


@dataclass(frozen=True, slots=True, kw_only=True)
class ColumnSpec:
    """Column definition for a report table."""

    key: str
    title: str
    width: float  # relative width units
    renderer: CellRenderer

    gap_after: float = 0.0
    header_ha: Literal["left", "center", "right"] = "left"


@dataclass(frozen=True, slots=True, kw_only=True)
class TableStyle:
    """Visual styling parameters for report tables."""

    header_height: float = 0.14
    row_height: float = 0.11
    pad_x: float = 0.01
    zebra_alpha: float = 0.06
    outer_lw: float = 1.0
    row_lw: float = 0.6
    header_fontsize: int = 9
    cell_fontsize: int = 9
