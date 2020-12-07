from logging import Logger
from typing import Optional

from wev import get_plugin, get_version
from wev.logging import get_logger
from wev.state import BaseState, State
from wev.text import bold, dim, displayable, get_now


def explain(logger: Optional[Logger] = None, state: Optional[BaseState] = None) -> None:
    """
    Logs an explanation of what an execution will do.

    Args:
        logger: Logger. One will be created if not specified.
    """
    return _explain(logger=logger or get_logger(), state=state or State())


def _explain(logger: Logger, state: BaseState) -> None:
    """
    Logs an explanation of what an execution will do.

    Args:
        logger: Logger.
    """
    logger.info(
        "%s (%s) execution plan generated at %s:",
        bold("wev"),
        get_version(),
        bold(get_now()),
    )

    list_index_padding = 2
    list_index_suffix = "."

    logger.info("")

    for index, variable in enumerate(state.get_variables()):
        logger.info(
            "%s%s %s will be resolved by the %s plugin.",
            str(index + 1).rjust(list_index_padding),
            list_index_suffix,
            bold(displayable(variable.names)),
            bold(variable.plugin.id),
        )

        margin = "    "

        if variable.resolution:
            logger.info("")
            logger.info("%s%s", margin, dim(variable.resolution.explain_cache))

        if not variable.should_read_from_cache:
            logger.info("")
            plugin = get_plugin(variable.plugin)
            for line in plugin.explain(logger=get_logger(name=variable.plugin.id)):
                logger.info("%s%s", margin, dim(line))

        logger.info("")
