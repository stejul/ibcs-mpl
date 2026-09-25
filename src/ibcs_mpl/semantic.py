"""Semantic analysis helpers (impact, variance direction)."""

from ibcs_mpl.types import Impact


__all__ = [
    "impact_from_value",
]


def impact_from_value(value: float) -> Impact:
    if value > 0:
        return Impact.POSITIVE
    if value < 0:
        return Impact.NEGATIVE
    return Impact.NEUTRAL
