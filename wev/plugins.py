from typing import cast

from pkg_resources import iter_entry_points

from wev.exceptions import MultiplePluginsError, NoPluginError
from wev.logging import get_logger
from wev.sdk import PluginBase, PluginConfiguration


def get_plugin(config: PluginConfiguration) -> PluginBase:
    """
    Gets a plugin instance to handle the given configuration.

    Raises `NoPluginError` if there isn't a plugin available to handle this
    configuration.

    Raises `MultiplePluginsError` if there are multple plugins available to
    handle this configuration.
    """
    plugins = [e for e in iter_entry_points("wev.plugins") if e.name == config.id]

    if len(plugins) == 0:
        raise NoPluginError(plugin_id=config.id)

    if len(plugins) > 1:
        raise MultiplePluginsError(plugin_id=config.id, count=len(plugins))

    logger = get_logger()

    logger.debug("Instantiating plugin with: %s", config)
    plugin = cast(PluginBase, plugins[0].load().Plugin(config))

    logger.debug("Instantiated plugin: %s", plugin)
    return plugin
