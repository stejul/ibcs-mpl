"""Chart input validation helpers."""

from dataclasses import dataclass
from typing import Sequence


__all__ = [
    "ValidationIssue",
    "validate_stacked_sign_consistency",
    "validate_ratio_widths",
    "validate_scenario_order",
]


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """A single chart input validation problem."""

    code: str
    message: str


def validate_stacked_sign_consistency(
    stack_values: Sequence[Sequence[float]],
) -> list[ValidationIssue]:
    """Ensure no single stack mixes positive and negative values."""
    issues: list[ValidationIssue] = []
    for series_idx, series in enumerate(stack_values):
        if not series:
            continue
        has_pos = any(v > 0 for v in series)
        has_neg = any(v < 0 for v in series)
        if has_pos and has_neg:
            issues.append(
                ValidationIssue(
                    code="STACKED_MIXED_SIGN",
                    message=f"stack series {series_idx} mixes positive and negative values",
                )
            )
    return issues


def validate_ratio_widths(width_basic: float, width_ratio: float) -> list[ValidationIssue]:
    """Check that ratio width is half of basic width per IBCS."""
    issues: list[ValidationIssue] = []
    if width_basic <= 0 or width_ratio <= 0:
        issues.append(ValidationIssue(code="WIDTH_NON_POSITIVE", message="widths must be positive"))
        return issues
    expected = width_basic * 0.5
    if abs(width_ratio - expected) > 1e-9:
        issues.append(
            ValidationIssue(
                code="RATIO_WIDTH_NOT_HALF",
                message="ratio width should be 50% of basic width per IBCS semantics",
            )
        )
    return issues


def validate_scenario_order(order: Sequence[str]) -> list[ValidationIssue]:
    """Warn if reference scenarios appear before primary scenarios."""
    issues: list[ValidationIssue] = []
    # Recommended AC/FC in foreground; PY/PL as reference.
    if len(order) >= 2 and order[0] in {"PY", "PL", "BU"} and order[1] in {"AC", "FC"}:
        issues.append(
            ValidationIssue(
                code="SCENARIO_ORDER_REFERENCE_FIRST",
                message="reference scenario appears before primary scenario; consider primary-first order",
            )
        )
    return issues
