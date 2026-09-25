import sys
import types

from ibcs_mpl.charts import ChartRegistry, SingleColumnChart
from ibcs_mpl.plugins import load_plugins_from_modules, register_plugin


def _register_single_column_alias(registry: ChartRegistry) -> None:
    registry.register("single_column_alias", SingleColumnChart)


def test_register_plugin_callable() -> None:
    local_registry = ChartRegistry()
    register_plugin(_register_single_column_alias, registry=local_registry)
    assert "single_column_alias" in local_registry.keys()


def test_load_plugins_from_modules() -> None:
    module_name = "test_plugin_module"
    module = types.ModuleType(module_name)

    def register(registry: ChartRegistry) -> None:
        registry.register("line_alias", SingleColumnChart)

    setattr(module, "register", register)

    sys.modules[module_name] = module

    local_registry = ChartRegistry()
    loaded = load_plugins_from_modules([module_name], registry=local_registry)

    assert loaded == [module_name]
    assert "line_alias" in local_registry.keys()
