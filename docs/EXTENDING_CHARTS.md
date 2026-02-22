# Extending Charts

This project is designed to make new IBCS chart types easy to add.

## 1) Add a chart class

Create a new module in `src/ibcs_mpl/charts/` and implement a chart as a dataclass inheriting `ChartBase`.

Minimal pattern:

```python
from dataclasses import dataclass

import matplotlib.axes

from ibcs_mpl.charts.base import ChartBase


@dataclass(frozen=True, slots=True, kw_only=True)
class MyChart(ChartBase):
    categories: list[str]
    values: list[float]

    def draw(self, ax: matplotlib.axes.Axes) -> matplotlib.axes.Axes:
        self._prep(ax)
        ax.bar(self.categories, self.values)
        return ax
```

## 2) Add/Reuse typed specs

If your chart needs structured inputs, add a spec in `src/ibcs_mpl/charts/specs.py` and validate lengths/required fields.

## 3) Use semantic helpers

Prefer shared semantic helpers instead of hardcoding:

- scenario style: `ibcs_mpl.theme.scenario_style`
- variance impact: `ibcs_mpl.semantic.impact_from_value`
- semantic checks: `ibcs_mpl.validation.*`

## 4) Register the chart

Add it to the registry in `src/ibcs_mpl/charts/__init__.py`:

```python
registry.register("my_chart", MyChart)
```

Then users can build dynamically:

```python
chart = registry.build("my_chart", title="Demo", categories=["Jan"], values=[10])
```

## 5) Optional: plugin registration

For external packages, expose a plugin function:

```python
from ibcs_mpl.charts import ChartRegistry

def register(registry: ChartRegistry) -> None:
    registry.register("my_chart", MyChart)
```

Load it with:

```python
from ibcs_mpl.plugins import load_plugins_from_modules

load_plugins_from_modules(["my_package.my_plugin"])
```

or via entry points (`ibcs_mpl.plugins`).

## 6) Add tests

Add at least:

- smoke render test (`tests/test_render_smoke.py` style)
- spec validation tests
- optional snapshot test for regression safety
