"""Data specifications and validation for chart input data."""

from dataclasses import dataclass
from typing import Sequence

from ibcs_mpl.types import ScenarioCode, ReferenceScenario


__all__ = [
    "CategorySeries",
    "ScenarioSeries",
    "GroupedScenarioSeries",
    "StackedSeries",
    "WaterfallSeries",
]


@dataclass(frozen=True, slots=True, kw_only=True)
class CategorySeries:
    categories: Sequence[str]
    values: Sequence[float]

    def validate(self) -> None:
        if len(self.categories) == 0:
            raise ValueError("categories must not be empty")
        if len(self.categories) != len(self.values):
            raise ValueError("categories and values must have the same length")


@dataclass(frozen=True, slots=True, kw_only=True)
class ScenarioSeries(CategorySeries):
    scenario: ScenarioCode = ScenarioCode.AC


@dataclass(frozen=True, slots=True, kw_only=True)
class RelativeVarianceSeries:
    categories: Sequence[str]
    rel_variance_pct: Sequence[float]
    minuend_scenario: ScenarioCode = ScenarioCode.AC
    reference_scenario: ReferenceScenario = ReferenceScenario.PY

    def validate(self) -> None:
        if len(self.categories) == 0:
            raise ValueError("categories must not be empty")
        if len(self.categories) != len(self.rel_variance_pct):
            raise ValueError("categories and rel_variance_pct must have the same length")


@dataclass(frozen=True, slots=True, kw_only=True)
class GroupedScenarioSeries:
    categories: Sequence[str]
    primary_values: Sequence[float]
    reference_values: Sequence[float]
    primary_scenario: ScenarioCode = ScenarioCode.AC
    reference_scenario: ScenarioCode = ScenarioCode.PY

    def validate(self) -> None:
        if len(self.categories) == 0:
            raise ValueError("categories must not be empty")
        if len(self.categories) != len(self.primary_values):
            raise ValueError("categories and primary_values must have the same length")
        if len(self.categories) != len(self.reference_values):
            raise ValueError("categories and reference_values must have the same length")


@dataclass(frozen=True, slots=True, kw_only=True)
class StackedSeries:
    categories: Sequence[str]
    stack_labels: Sequence[str]
    stack_values: Sequence[Sequence[float]]

    def validate(self) -> None:
        if len(self.categories) == 0:
            raise ValueError("categories must not be empty")
        if len(self.stack_labels) == 0:
            raise ValueError("stack_labels must not be empty")
        if len(self.stack_labels) != len(self.stack_values):
            raise ValueError("stack_labels and stack_values must have the same length")
        expected = len(self.categories)
        for idx, values in enumerate(self.stack_values):
            if len(values) != expected:
                raise ValueError(f"stack_values[{idx}] must have length {expected}")


@dataclass(frozen=True, slots=True, kw_only=True)
class WaterfallSeries:
    categories: Sequence[str]
    values: Sequence[float]
    is_total: Sequence[bool]

    def validate(self) -> None:
        if len(self.categories) == 0:
            raise ValueError("categories must not be empty")
        if len(self.categories) != len(self.values):
            raise ValueError("categories and values must have the same length")
        if len(self.categories) != len(self.is_total):
            raise ValueError("categories and is_total must have the same length")
