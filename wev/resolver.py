from os import environ
from typing import Dict, Optional

from wev import get_plugin
from wev.exceptions import IncorrectResolutionCountError
from wev.logging import get_logger
from wev.sdk import Resolution, ResolutionSupport
from wev.sdk.exceptions import CannotResolveError
from wev.state import BaseState, State
from wev.text import bold, dim


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


def resolve(state: Optional[BaseState] = None) -> Dict[str, str]:
    """
    Gathers values for all the required environment variables. Reads from the
    cache where possible, and invokes plugins where needed.

    Returns:
        Environment variable names and values.
    """

    logger = get_logger()
    this_state = state or State()

    environs: Dict[str, str] = {**environ}

    for variable in this_state.get_variables():
        if resolution := fresh_resolution(variable.resolution):
            logger.debug("%s has a fresh cache.", variable.names)
        else:
            logger.info("Resolving %s...", bold(variable.names))

            support = ResolutionSupport(
                logger=get_logger(name=variable.plugin.id),
                confidential_prompt=confidential_prompt,
            )

            plugin = get_plugin(variable.plugin)

            try:
                resolution = plugin.resolve(support=support)
            except CannotResolveError as ex:
                raise CannotResolveError(f'"{variable.plugin.id}" failed: {ex}')

            # If the resolution has a cache expiry date then cache it.
            # Otherwise don't cache it, and remove any previously-set cache.
            if resolution.expires_at:
                this_state.resolution_cache.update(
                    names=variable.names,
                    resolution=resolution,
                )
            else:
                this_state.resolution_cache.remove(names=variable.names)

        if resolution.values:
            logger.debug("Enumerating resolved values: %s", resolution.values)
            variable_count = len(variable.names)
            resolution_count = len(resolution.values)

            if variable_count != resolution_count:
                raise IncorrectResolutionCountError(
                    plugin_id=variable.plugin.id,
                    variable_count=variable_count,
                    resolution_count=resolution_count,
                )

            for index, name in enumerate(variable.names):
                value = resolution.values[index]
                logger.debug("Adding resolved variable: %s=%s", name, value)
                environs.update({name: value})

    # Save the cache only if we own it.
    if not state:
        this_state.resolution_cache.save()

    return environs


def confidential_prompt(preamble: str, prompt: str) -> str:
    print(dim(preamble))
    print()
    return input(f"{prompt} ")
