from dataclasses import dataclass
from typing import Any

__all__ = ["ComplianceIssue", "ComplianceEngine", "format_report"]


@dataclass(frozen=True, slots=True)
class ComplianceIssue:
    rule_id: str        # e.g. "UN 4.1"
    message: str
    severity: str       # "error" | "warning"


class ComplianceEngine:
    """Checks charts for IBCS rule violations."""

    def check(self, chart: Any) -> list[ComplianceIssue]:
        """Run all compliance checks on a chart and return a list of issues."""
        issues: list[ComplianceIssue] = []

        # CH 1.1: Title required
        title = getattr(chart, "title", None)
        if title is None or title == "":
            issues.append(ComplianceIssue(
                rule_id="CH 1.1",
                message="Chart must have a title (CH 1.1)",
                severity="error",
            ))

        # UN 4.1: Scenario notation
        primary_scenario = getattr(chart, "primary_scenario", None)
        reference_scenario = getattr(chart, "reference_scenario", None)
        if primary_scenario is not None and reference_scenario is not None:
            from ibcs_mpl.types import ScenarioCode, ReferenceScenario
            reference_type_codes = {ScenarioCode.PY, ScenarioCode.PL, ScenarioCode.BU}
            if primary_scenario in reference_type_codes and reference_scenario == ReferenceScenario.AC:
                issues.append(ComplianceIssue(
                    rule_id="UN 4.1",
                    message="Primary scenario appears to be a reference type (UN 4.1)",
                    severity="warning",
                ))

        # UN 3.1: Width ratio
        theme = getattr(chart, "theme", None)
        if theme is not None:
            width_basic = getattr(theme, "width_basic", None)
            width_ratio = getattr(theme, "width_ratio", None)
            if width_basic is not None and width_ratio is not None:
                expected = width_basic / 2.0
                if abs(width_ratio - expected) / max(abs(expected), 1e-12) > 0.05:
                    issues.append(ComplianceIssue(
                        rule_id="UN 3.1",
                        message="width_ratio should be approximately half of width_basic (UN 3.1)",
                        severity="warning",
                    ))

        # EX 1.1: Empty data
        for attr in ("values", "primary_values"):
            data = getattr(chart, attr, None)
            if data is not None and hasattr(data, "__len__") and len(data) == 0:
                issues.append(ComplianceIssue(
                    rule_id="EX 1.1",
                    message="Chart data must not be empty (EX 1.1)",
                    severity="error",
                ))
                break

        # EX 2.1: Stacked sign consistency
        stack_values = getattr(chart, "stack_values", None)
        if stack_values is not None:
            from ibcs_mpl.validation import validate_stacked_sign_consistency
            stacked_issues = validate_stacked_sign_consistency(stack_values)
            for issue in stacked_issues:
                issues.append(ComplianceIssue(
                    rule_id="EX 2.1",
                    message=f"Stacked values mix positive and negative in the same stack (EX 2.1): {issue.message}",
                    severity="warning",
                ))

        return issues

    def check_all(self, charts: list[Any]) -> dict[int, list[ComplianceIssue]]:
        """Run check() on each chart and return {index: issues} for charts with issues."""
        results: dict[int, list[ComplianceIssue]] = {}
        for idx, chart in enumerate(charts):
            issues = self.check(chart)
            if issues:
                results[idx] = issues
        return results


def format_report(results: dict[int, list[ComplianceIssue]]) -> str:
    """Return a human-readable compliance report string."""
    if not results:
        return "No compliance issues found."

    lines: list[str] = ["IBCS Compliance Report", "=" * 40]
    for idx in sorted(results):
        issues = results[idx]
        lines.append(f"\nChart {idx}:")
        for issue in issues:
            severity_label = issue.severity.upper()
            lines.append(f"  [{severity_label}] {issue.rule_id}: {issue.message}")

    total = sum(len(v) for v in results.values())
    errors = sum(1 for v in results.values() for i in v if i.severity == "error")
    warnings = sum(1 for v in results.values() for i in v if i.severity == "warning")
    lines.append(f"\nTotal: {total} issue(s) — {errors} error(s), {warnings} warning(s)")

    return "\n".join(lines)
