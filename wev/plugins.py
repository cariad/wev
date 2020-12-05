from typing import Any, Dict, cast

from pkg_resources import iter_entry_points

from wev.exceptions import MultiplePluginsError, NoPluginError
from wev.sdk import PluginBase


def get_plugin(handler: str, configuration: Dict[Any, Any]) -> PluginBase:
    """
    Gets a plugin instance for the given handler.

    Args:
        handler:       Handler to get a plugin for.
        configuration: Configuration to pass to the plugin.

    Returns:
        Plugin instance.

    Raises:
        NoPluginError:        No plugins installed for this handler.
        MultiplePluginsError: Multple plugins installed for this handler.
    """
    plugins = [e for e in iter_entry_points("wev.plugins") if e.name == handler]

    if len(plugins) == 0:
        raise NoPluginError(handler=handler)

    if len(plugins) > 1:
        raise MultiplePluginsError(handler=handler, count=len(plugins))

    return cast(PluginBase, plugins[0].load().Plugin(configuration))
