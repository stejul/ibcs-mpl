from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias, Sequence

Number: TypeAlias = float
Label: TypeAlias = str
Point: TypeAlias = tuple[float, float]
Pt: TypeAlias = float

class ScenarioCode(str, Enum):
    AC = "AC"  # Actual (measured)
    PY = "PY"  # Previous year (measured, earlier period)
    PL = "PL"  # Plan (fictitious)
    BU = "BU"  # Budget (fictitious)
    FC = "FC"  # Forecast (expected)

class ReferenceScenario(str, Enum):
    PY = "PY"
    PL = "PL"
    BU = "BU"

class Impact(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

@dataclass(frozen=True)
class Series:
    name: str
    values: Sequence[float]

@dataclass(frozen=True)
class CategoryAxis:
    categories: Sequence[str]
