from dataclasses import dataclass
from typing import Any, Sequence

import matplotlib.axes
from matplotlib.patches import Rectangle

from ibcs_mpl.tables.types import ColumnSpec, Rect, TableStyle


@dataclass(frozen=True, slots=True, kw_only=True)
class Table:
    columns: Sequence[ColumnSpec]
    rows: Sequence[dict[str, Any]]
    style: TableStyle = TableStyle()

    def draw(self, ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        cols = self.columns
        rows = self.rows
        st = self.style
        total_units = sum(c.width + c.gap_after for c in cols)

        header_y0 = 1.0 - st.header_height
        ax.add_patch(Rectangle((0, header_y0), 1, st.header_height, fill=False, linewidth=st.outer_lw))

        x0 = 0.0
        for c in cols:
            col_w = c.width / total_units

            if c.header_ha == "left":
                hx = x0 + st.pad_x
            elif c.header_ha == "right":
                hx = x0 + col_w - st.pad_x
            else:
                hx = x0 + col_w / 2.0

            ax.text(hx, header_y0 + st.header_height / 2.0, c.title, ha=c.header_ha, va="center", fontsize=st.header_fontsize)
            x0 += col_w + (c.gap_after / total_units)

        n_rows = len(rows)
        body_top = header_y0

        for row_idx, row in enumerate(rows):
            y0 = body_top - (row_idx + 1) * st.row_height

            if row_idx % 2 == 1:
                ax.add_patch(Rectangle((0, y0), 1, st.row_height, linewidth=0, alpha=st.zebra_alpha))

            ax.plot([0, 1], [y0, y0], linewidth=st.row_lw)

            x0 = 0.0
            for c in cols:
                col_w = c.width / total_units
                rect = Rect(x=x0, y=y0, w=col_w, h=st.row_height)
                c.renderer.draw(ax, rect, row.get(c.key))
                x0 += col_w + (c.gap_after / total_units)

        body_h = st.row_height * n_rows
        ax.add_patch(Rectangle((0, body_top - body_h), 1, body_h, fill=False, linewidth=st.outer_lw))
        return ax
