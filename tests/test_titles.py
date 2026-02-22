import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from ibcs_mpl.charts import SingleColumnChart
from ibcs_mpl.titles import MessageBlock, PageTitle


def test_page_title_render() -> None:
    title = PageTitle(
        line1_reporting_unit="Alpha Corp.",
        line2_measure="Net sales in mEUR",
        line3_context="2026 AC and PY",
    )
    assert title.render().count("\n") == 2


def test_chart_with_message_block_smoke() -> None:
    fig, ax = plt.subplots()
    chart = SingleColumnChart(
        title=PageTitle(
            line1_reporting_unit="Alpha Corp.",
            line2_measure="Net sales in mEUR",
            line3_context="2026 AC",
        ),
        message=MessageBlock(text="Sales are above plan."),
        categories=["Jan", "Feb"],
        values=[10, 12],
    )
    chart.draw(ax)
    plt.close(fig)


def test_dynamic_title_subtitle_spacing_for_multiline_blocks() -> None:
    fig, ax = plt.subplots(figsize=(6, 3))
    chart = SingleColumnChart(
        title="Line 1\nLine 2\nLine 3",
        subtitle="Sub 1\nSub 2",
        categories=["Jan", "Feb", "Mar"],
        values=[10, 11, 12],
    )
    chart.draw(ax)

    assert len(fig.texts) >= 2
    title_text = fig.texts[0]
    subtitle_text = fig.texts[1]

    title_y = float(title_text.get_position()[1])
    subtitle_y = float(subtitle_text.get_position()[1])
    assert title_y - subtitle_y > 0.03

    plt.close(fig)
