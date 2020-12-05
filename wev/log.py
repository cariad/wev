from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    Formatter,
    LogRecord,
    StreamHandler,
    basicConfig,
    root,
)
from sys import stdout
from typing import Optional

from colorama import Style
from colorama import init as colorama_init


def init() -> None:
    basicConfig()
    colorama_init()
    handler = StreamHandler(stdout)
    handler.setFormatter(LogFormatter())
    root.addHandler(handler)
    set_level("INFO")


def set_level(level: str) -> None:
    root.setLevel(level)


class LogFormatter(Formatter):
    def __init__(self, fmt: Optional[str] = "%(levelno)s: %(msg)s"):
        super().__init__(fmt, datefmt=None, style="%")
        self.formatters = {
            DEBUG: Formatter(Style.DIM + "[wev debug] %(message)s" + Style.RESET_ALL),
            INFO: Formatter("%(message)s"),
            ERROR: Formatter("[wev error]: %(message)s"),
            CRITICAL: Formatter("[wev failed]: %(message)s"),
        }

    def get_formatter(self, level: int) -> Formatter:
        return self.formatters.get(level, self.formatters[INFO])

    def format(self, record: LogRecord) -> str:
        return self.get_formatter(level=record.levelno).format(record=record)
