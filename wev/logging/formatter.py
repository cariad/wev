from logging import CRITICAL, DEBUG, ERROR, INFO
from logging import Formatter as BaseFormatter
from logging import LogRecord

from wev.text import dim


class Formatter(BaseFormatter):
    def __init__(self, name: str):
        super().__init__("%(levelno)s: %(message)s", datefmt=None, style="%")
        self.formatters = {
            DEBUG: BaseFormatter(dim(f'{self.prefix(name, "debug")}%(message)s')),
            INFO: BaseFormatter(f'{self.prefix(name, "info")}%(message)s'),
            ERROR: BaseFormatter(f'{self.prefix(name, "error")} %(message)s'),
            CRITICAL: BaseFormatter(f'{self.prefix(name, "critical")} %(message)s'),
        }

    def prefix(self, name: str, level: str) -> str:
        if name == "wev" and level == "info":
            return ""
        return f"[{name} {level.lower()}] "

    def get_formatter(self, level: int) -> BaseFormatter:
        return self.formatters.get(level, self.formatters[INFO])

    def format(self, record: LogRecord) -> str:
        return self.get_formatter(level=record.levelno).format(record=record)
