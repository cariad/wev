from abc import ABC, abstractmethod
from logging import Logger
from typing import List

from wev.sdk import Resolution


class PluginBase(ABC):
    @abstractmethod
    def explain(self) -> List[str]:
        pass

    @abstractmethod
    def resolve(self, logger: Logger) -> Resolution:
        pass
