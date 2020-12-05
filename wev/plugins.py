from typing import cast

from pkg_resources import iter_entry_points

from wev.exceptions import HandlerNotInstalled
from wev.sdk import PluginBase
from wev.variable import Variable


def get_plugin(variable: Variable) -> PluginBase:
    for impl in iter_entry_points("wev.plugins"):
        if impl.name == variable.handler:
            return cast(PluginBase, impl.load().Plugin(config=variable.configuration))
    else:
        raise HandlerNotInstalled(name=variable.handler)
