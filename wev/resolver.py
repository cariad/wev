from logging import getLogger
from os import environ
from typing import Dict, Optional

from colorama import Style

from wev import Cache, get_plugin, get_variables
from wev.sdk import Resolution


def fresh_resolution(resolution: Optional[Resolution]) -> Optional[Resolution]:
    if not resolution:
        return None
    elif resolution.seconds_until_expiry is None:
        return None
    elif resolution.seconds_until_expiry <= 0:
        return None
    else:
        return resolution


def resolve() -> Dict[str, str]:

    # logger = getLogger("wev")

    cache = Cache()
    cache.read()
    environs: Dict[str, str] = {**environ}

    for variable in get_variables(cache=cache):

        if resolution := fresh_resolution(variable.resolution):
            print(
                Style.BRIGHT,
                variable.name,
                Style.RESET_ALL,
                " has a fresh cache.",
                sep="",
            )
        else:
            print(
                "Resolving ",
                Style.BRIGHT,
                variable.name,
                Style.RESET_ALL,
                "...",
                sep="",
            )

            plugin = get_plugin(variable)
            plugin_logger = getLogger(variable.handler)
            resolution = plugin.resolve(logger=plugin_logger)
            if resolution.expires_at:
                cache.update(var_name=variable.name, resolution=resolution)
            else:
                cache.remove(var_name=variable.name)

        environs.update({variable.name: resolution.value})

    cache.write()

    return environs
