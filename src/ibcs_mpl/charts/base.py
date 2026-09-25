"""Base protocol and dataclass for all IBCS charts."""

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

import matplotlib.axes
import matplotlib.figure

from ibcs_mpl.theme import IBCSTheme, DEFAULT_THEME
from ibcs_mpl.primitives import add_title_block, minimal_axes
from ibcs_mpl.titles import MessageBlock, PageTitle


__all__ = [
    "Chart",
    "ChartBase",
]


@runtime_checkable
class Chart(Protocol):
    """Protocol that all IBCS charts must satisfy."""

    def draw(self, ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes: ...


@dataclass(frozen=True, slots=True, kw_only=True)
class ChartBase:
    """Base dataclass with common chart attributes (title, subtitle, theme)."""

    title: str | PageTitle
    subtitle: str | None = None
    message: MessageBlock | None = None
    theme: IBCSTheme = DEFAULT_THEME

    title_top_pad: float = 0.012
    title_subtitle_gap: float = 0.020

    def _prep(self, ax: matplotlib.axes.Axes) -> None:
        minimal_axes(ax, self.theme)

        fig = ax.figure
        title_text = self.title.render() if isinstance(self.title, PageTitle) else self.title
        add_title_block(
            fig,  # type: ignore[arg-type]
            ax,
            title_text,
            self.subtitle,
            self.theme,
            message=self.message,
            top_pad=self.title_top_pad,
            title_to_subtitle_gap=self.title_subtitle_gap,
        )
