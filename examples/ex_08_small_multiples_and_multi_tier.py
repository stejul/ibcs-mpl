import matplotlib.pyplot as plt

from ibcs_mpl.charts import GroupedColumnChart, RelativeVariancePinChart, SingleColumnChart
from ibcs_mpl.composites import (
    MultiTierLayout,
    SmallMultiplesLayout,
    draw_multi_tier,
    draw_small_multiples,
)


# Small multiples
fig1 = plt.figure(figsize=(13, 8))
charts = [
    SingleColumnChart(
        title=f"Country {i + 1}", categories=["Jan", "Feb", "Mar"], values=[10 + i, 12 + i, 11 + i]
    )
    for i in range(6)
]
draw_small_multiples(
    fig1,
    charts,
    layout=SmallMultiplesLayout(columns=3, top=0.94, bottom=0.07, v_gap=0.10, min_title_band=0.05),
)


# Multi-tier chart (base + abs/rel variance style proxy)
fig2 = plt.figure(figsize=(10, 7))
tier1 = GroupedColumnChart(
    title="Sales",
    subtitle="AC vs PY",
    categories=["Jan", "Feb", "Mar", "Apr"],
    primary_values=[44, 52, 49, 56],
    reference_values=[41, 50, 47, 54],
)
tier2 = RelativeVariancePinChart(
    title="Relative variance",
    subtitle="ΔPY%",
    categories=["Jan", "Feb", "Mar", "Apr"],
    rel_variance_pct=[7.3, 4.0, 4.3, 3.7],
)
draw_multi_tier(
    fig2,
    [tier1, tier2],
    layout=MultiTierLayout(
        top=0.94, bottom=0.08, tier_gap=0.10, tier_ratios=(0.62, 0.38), min_title_band=0.06
    ),
)

plt.show()
