"""Chart registry for plugin-based chart discovery."""

from collections.abc import Callable
from typing import Any

from ibcs_mpl.charts.base import Chart


__all__ = [
    "ChartRegistry",
]


ChartBuilder = Callable[..., Chart]


class ChartRegistry:
    def __init__(self) -> None:
        self._builders: dict[str, ChartBuilder] = {}

    def register(self, key: str, builder: ChartBuilder) -> None:
        if key in self._builders:
            raise ValueError(f"Chart key already registered: {key}")
        self._builders[key] = builder

    def register_builder(self, key: str) -> Callable[[ChartBuilder], ChartBuilder]:
        def decorator(builder: ChartBuilder) -> ChartBuilder:
            self.register(key, builder)
            return builder

        return decorator

    def build(self, key: str, /, **kwargs: Any) -> Chart:
        builder = self._builders.get(key)
        if builder is None:
            known = ", ".join(sorted(self._builders))
            raise KeyError(f"Unknown chart key: {key}. Known keys: {known}")
        return builder(**kwargs)

    def keys(self) -> tuple[str, ...]:
        return tuple(sorted(self._builders.keys()))
