import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from ibcs_mpl.charts import SingleColumnChart
from ibcs_mpl.composites import draw_multi_tier, draw_small_multiples


def test_small_multiples_smoke() -> None:
    fig = plt.figure(figsize=(8, 6))
    charts = [
        SingleColumnChart(title=f"C{i}", categories=["A", "B"], values=[1 + i, 2 + i])
        for i in range(4)
    ]
    draw_small_multiples(fig, charts)
    assert len(fig.axes) == 4
    plt.close(fig)


def test_multi_tier_smoke() -> None:
    fig = plt.figure(figsize=(8, 6))
    charts = [
        SingleColumnChart(title="Tier1", categories=["A", "B"], values=[3, 4]),
        SingleColumnChart(title="Tier2", categories=["A", "B"], values=[1, 2]),
    ]
    draw_multi_tier(fig, charts)
    assert len(fig.axes) == 2
    plt.close(fig)
