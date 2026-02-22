import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from ibcs_mpl.charts import GroupedColumnChart, RelativeVariancePinChart, SingleColumnChart
from ibcs_mpl.charts import LineChart, ScenarioLineSeries, StackedColumnChart


def test_single_column_draw_smoke() -> None:
    fig, ax = plt.subplots()
    chart = SingleColumnChart(title="t", categories=["Jan", "Feb"], values=[10, 20])
    chart.draw(ax)
    plt.close(fig)


def test_relative_variance_pin_draw_smoke() -> None:
    fig, ax = plt.subplots()
    chart = RelativeVariancePinChart(
        title="t",
        categories=["Jan", "Feb"],
        rel_variance_pct=[-2.5, 3.0],
    )
    chart.draw(ax)
    plt.close(fig)


def test_grouped_column_draw_smoke() -> None:
    fig, ax = plt.subplots()
    chart = GroupedColumnChart(
        title="t",
        categories=["Jan", "Feb"],
        primary_values=[11, 22],
        reference_values=[10, 21],
    )
    chart.draw(ax)
    plt.close(fig)


def test_stacked_column_draw_smoke() -> None:
    fig, ax = plt.subplots()
    chart = StackedColumnChart(
        title="t",
        categories=["Jan", "Feb"],
        stack_labels=["L1", "L2"],
        stack_values=[[10, 12], [3, 2]],
    )
    chart.draw(ax)
    plt.close(fig)


def test_line_chart_draw_smoke() -> None:
    fig, ax = plt.subplots()
    chart = LineChart(
        title="t",
        categories=["Jan", "Feb", "Mar"],
        series=[
            ScenarioLineSeries(label="AC", values=[10, 11, 12]),
            ScenarioLineSeries(label="PY", values=[9, 10, 11]),
        ],
    )
    chart.draw(ax)
    plt.close(fig)
