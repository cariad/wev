import locale
from logging import Logger, StreamHandler, getLogger, root
from sys import stdout

from colorama import init as colorama_init

from wev.logging import Formatter

done_init = False


def get_logger(name: str = "wev") -> Logger:
    """
    Gets a logger.

    Arguments:
        name: Name of the logger. Defaults to "wev". When getting a logger for
              a plugin, use the plugin's name.

    Returns:
        Logger.
    """

    global done_init

    if not done_init:
        init()
        done_init = True

    logger = getLogger(name)

    # Register our `Formatter` as a handler if it hasn't already.
    for handler in logger.handlers:
        if isinstance(handler.formatter, Formatter):
            break
    else:
        handler = StreamHandler(stdout)
        handler.setFormatter(Formatter(name=name))
        logger.addHandler(handler)

    return logger


def init(level: str = "INFO") -> None:
    """
    Initialises logging.

    Args:
        level: Log level.
    """
    colorama_init()
    locale.setlocale(locale.LC_ALL, "")
    set_level(level)


def set_level(level: str) -> None:
    """
    Sets the log level.

    Args:
        level: Log level.
    """
    root.setLevel(level)
