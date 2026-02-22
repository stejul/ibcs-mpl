import matplotlib.pyplot as plt
from ibcs_mpl.reports import build_plain_report_table
from ibcs_mpl.tables import TableStyle

rows = [
    {"name": "Germany", "revenue": 70_000_000, "gm": 32.4, "fte": 120},
    {"name": "Austria", "revenue": 20_000_000, "gm": 28.1, "fte": 45},
    {"name": "Americas", "revenue": 55_000_000, "gm": 35.0, "fte": 95},
]

table = build_plain_report_table(rows=rows, style=TableStyle(row_height=0.11, header_height=0.14))

fig, ax = plt.subplots(figsize=(8.4, 2.6))
table.draw(ax)
plt.tight_layout()
plt.show()
