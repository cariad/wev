from logging import getLogger
from os import environ
from typing import Dict, Optional

from colorama import Style

from wev import Cache, get_plugin, get_variables
from wev.sdk import Resolution


def fresh_resolution(resolution: Optional[Resolution]) -> Optional[Resolution]:
    """
    Returns the resolution if it exists and hasn't expired.

    Args:
        resolution: Resolution.

    Returns:
        Resolution if it's fresh, otherwise `None`.
    """
    if not resolution:
        return None
    elif resolution.seconds_until_expiry is None:
        return None
    elif resolution.seconds_until_expiry <= 0:
        return None
    else:
        return resolution


def resolve() -> Dict[str, str]:
    """
    Gathers values for all the required environment variables. Reads from the
    cache where possible, and invokes plugins where needed.

    Returns:
        Environment variable names and values.
    """

    logger = getLogger("wev")

    cache = Cache()
    cache.read()

    environs: Dict[str, str] = {**environ}

    for variable in get_variables(cache=cache):
        if resolution := fresh_resolution(variable.resolution):
            logger.debug(
                "%s%s%s has a fresh cache.",
                Style.BRIGHT,
                variable.name,
                Style.NORMAL,
            )
        else:
            logger.info(
                "Resolving %s%s%s...",
                Style.BRIGHT,
                variable.name,
                Style.NORMAL,
            )

            plugin = get_plugin(
                handler=variable.handler,
                configuration=variable.configuration,
            )
            resolution = plugin.resolve(logger=getLogger(variable.handler))
            if resolution.expires_at:
                cache.update(var_name=variable.name, resolution=resolution)
            else:
                cache.remove(var_name=variable.name)

        if resolution.value is not None:
            environs.update({variable.name: resolution.value})

    cache.write()
    return environs
