import matplotlib.pyplot as plt

from ibcs_mpl.composites.roa_tree import ROATreeData, build_roa_tree
from ibcs_mpl.types import ScenarioCode

years = ["'10", "'11", "'12", "'13", "'14", "'15", "'16"]

data = ROATreeData(
    years=years,
    roa_pct=[24.9, -9.7, -17.8, 14.7, 17.9, 19.2, 18.9],
    ros_pct=[19.2, -7.0, -13.1, 14.0, 17.2, 19.8, 22.5],
    asset_turnover=[1.3, 1.4, 1.4, 1.0, 1.0, 1.0, 0.8],
    return_meur=[5.0, -1.8, -3.5, 3.1, 4.1, 4.7, 5.3],
    sales_meur=[26.1, 25.7, 26.4, 22.1, 23.8, 23.7, 23.6],
    assets_meur=[20.1, 18.5, 19.4, 21.1, 22.9, 24.5, 28.0],
    scenario_roa=ScenarioCode.AC,
    scenario_ros=ScenarioCode.AC,
    scenario_turn=ScenarioCode.AC,
    scenario_return=ScenarioCode.AC,
    scenario_sales=ScenarioCode.AC,
    scenario_assets=ScenarioCode.AC,
)

fig = plt.figure(figsize=(16, 9.5))
fig.suptitle(
    "We plan to achieve an ROA of around 19% in 2016\ndespite increasing assets",
    x=0.02,
    y=0.99,
    ha="left",
    fontsize=14,
)

build_roa_tree(fig, data)

plt.show()
