"""Core type aliases and enums for IBCS semantics."""

from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias, Sequence


__all__ = [
    "Number",
    "Label",
    "Point",
    "Pt",
    "ScenarioCode",
    "ReferenceScenario",
    "Impact",
]

Number: TypeAlias = float
Label: TypeAlias = str
Point: TypeAlias = tuple[float, float]
Pt: TypeAlias = float


class ScenarioCode(str, Enum):
    """IBCS scenario codes for data classification."""

    AC = "AC"  # Actual (measured)
    PY = "PY"  # Previous year (measured, earlier period)
    PL = "PL"  # Plan (fictitious)
    BU = "BU"  # Budget (fictitious)
    FC = "FC"  # Forecast (expected)


class ReferenceScenario(str, Enum):
    """Scenarios that may serve as reference baselines."""

    PY = "PY"
    PL = "PL"
    BU = "BU"


class Impact(str, Enum):
    """Semantic impact direction for variance values."""

    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


@dataclass(frozen=True)
class Series:
    """A simple named series of floats."""

    name: str
    values: Sequence[float]


@dataclass(frozen=True)
class CategoryAxis:
    """Category labels for a chart axis."""

    categories: Sequence[str]
