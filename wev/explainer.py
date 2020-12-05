from logging import Logger, getLogger
from typing import Optional

from wev import Cache, get_plugin, get_variables, get_version
from wev.text import bold, dim, get_now


def explain(logger: Optional[Logger] = None) -> None:
    """
    Logs an explanation of what an execution will do.

    Args:
        logger: Logger. One will be created if not specified.
    """
    return _explain(logger=logger or getLogger("wev"))


def _explain(logger: Logger) -> None:
    """
    Logs an explanation of what an execution will do.

    Args:
        logger: Logger.
    """
    cache = Cache()
    cache.read()

    logger.info(
        "%s (%s) execution plan generated at %s:",
        bold("wev"),
        get_version(),
        bold(get_now()),
    )

    list_index_padding = 2
    list_index_suffix = "."

    for index, variable in enumerate(get_variables(cache=cache)):
        logger.info("")

        logger.info(
            "%s%s %s will be resolved by the %s plugin.",
            str(index + 1).rjust(list_index_padding),
            list_index_suffix,
            bold(variable.name),
            bold(variable.handler),
        )

        margin = "    "

        if variable.resolution:
            logger.info("")
            logger.info("%s%s", margin, dim(variable.resolution.explain_cache))

        if not variable.should_read_from_cache:
            logger.info("")
            plugin = get_plugin(variable)
            for line in plugin.explain():
                logger.info("%s%s", margin, dim(line))
