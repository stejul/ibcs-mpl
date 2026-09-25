"""Chart plugin registration and entry-point loading."""

from collections.abc import Callable
from importlib import import_module
from importlib.metadata import entry_points
from typing import Protocol, runtime_checkable, Any

from ibcs_mpl.charts import ChartRegistry, registry as default_registry


__all__ = [
    "ChartPlugin",
    "register_plugin",
    "load_entrypoint_plugins",
    "load_plugins_from_modules",
]


@runtime_checkable
class ChartPlugin(Protocol):
    def register(self, registry: ChartRegistry) -> None: ...


PluginCallable = Callable[[ChartRegistry], None]


def register_plugin(
    plugin: ChartPlugin | PluginCallable, *, registry: ChartRegistry = default_registry
) -> None:
    if callable(plugin):
        plugin(registry)
        return
    plugin.register(registry)


def load_entrypoint_plugins(
    *,
    group: str = "ibcs_mpl.plugins",
    registry: ChartRegistry = default_registry,
) -> list[str]:
    loaded: list[str] = []

    for ep in entry_points(group=group):
        plugin_obj: Any = ep.load()
        register_plugin(plugin_obj, registry=registry)
        loaded.append(ep.name)

    return loaded


def load_plugins_from_modules(
    modules: list[str],
    *,
    attr: str = "register",
    registry: ChartRegistry = default_registry,
) -> list[str]:
    loaded: list[str] = []

    for module_name in modules:
        module = import_module(module_name)
        if not hasattr(module, attr):
            raise AttributeError(f"Module '{module_name}' has no attribute '{attr}'")
        plugin_obj = getattr(module, attr)
        register_plugin(plugin_obj, registry=registry)
        loaded.append(module_name)

    return loaded
