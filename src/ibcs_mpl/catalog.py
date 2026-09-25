"""Chart catalog introspection utilities."""

from typing import Iterable

from ibcs_mpl.charts import registry


__all__ = [
    "available_chart_types",
    "print_chart_catalog",
]


def available_chart_types() -> tuple[str, ...]:
    return registry.keys()


def print_chart_catalog() -> None:
    print("Available chart types:")
    for key in registry.keys():
        print(f"- {key}")


def assert_required_charts(required: Iterable[str]) -> None:
    available = set(registry.keys())
    missing = [key for key in required if key not in available]
    if missing:
        raise KeyError(f"Missing chart types: {', '.join(missing)}")
