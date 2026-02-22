from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from ibcs_mpl.types import ScenarioCode


@dataclass(frozen=True, slots=True, kw_only=True)
class ScenarioPoint:
    category: str
    value: float
    scenario: ScenarioCode = ScenarioCode.AC


@dataclass(frozen=True, slots=True, kw_only=True)
class ScenarioSeriesData:
    name: str
    categories: Sequence[str]
    values: Sequence[float]
    scenario: ScenarioCode = ScenarioCode.AC

    def validate(self) -> None:
        if len(self.categories) == 0:
            raise ValueError("categories must not be empty")
        if len(self.categories) != len(self.values):
            raise ValueError("categories and values must have the same length")


def from_records(
    records: Sequence[Mapping[str, Any]],
    *,
    category_key: str,
    value_key: str,
    name: str,
    scenario: ScenarioCode = ScenarioCode.AC,
) -> ScenarioSeriesData:
    categories = [str(row[category_key]) for row in records]
    values = [float(row[value_key]) for row in records]
    out = ScenarioSeriesData(name=name, categories=categories, values=values, scenario=scenario)
    out.validate()
    return out


def from_pandas(
    df: Any,
    *,
    category_col: str,
    value_col: str,
    name: str,
    scenario: ScenarioCode = ScenarioCode.AC,
) -> ScenarioSeriesData:
    if not hasattr(df, "__getitem__"):
        raise TypeError("df must support column indexing")
    categories = [str(v) for v in df[category_col].tolist()]
    values = [float(v) for v in df[value_col].tolist()]
    out = ScenarioSeriesData(name=name, categories=categories, values=values, scenario=scenario)
    out.validate()
    return out
