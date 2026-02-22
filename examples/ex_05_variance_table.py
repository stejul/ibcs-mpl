import matplotlib.pyplot as plt
from ibcs_mpl.reports import build_variance_table
from ibcs_mpl.tables import TableStyle
from ibcs_mpl.types import ScenarioCode, ReferenceScenario

rows = [
    {"name": "Germany", "ac": 70, "py": 65},
    {"name": "Austria", "ac": 20, "py": 18},
    {"name": "Americas", "ac": 55, "py": 60},
    {"name": "Weird case", "ac": 30, "py": -30},  # ΔPY% -> n.a. :contentReference[oaicite:18]{index=18}
]

table = build_variance_table(
    rows=rows,
    minuend_key="ac",
    reference_key="py",
    minuend_scenario=ScenarioCode.AC,
    reference_scenario=ReferenceScenario.PY,
    style=TableStyle(row_height=0.11, header_height=0.14),
)

fig, ax = plt.subplots(figsize=(10.8, 3.0))
table.draw(ax)
plt.tight_layout()
plt.show()
