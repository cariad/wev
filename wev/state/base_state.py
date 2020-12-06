from abc import ABC, abstractmethod, abstractproperty
from logging import getLogger
from typing import Iterator

from wev import ResolutionCache, Variable


class BaseState(ABC):
    def __init__(self) -> None:
        self.logger = getLogger("wev")
        self.logger.debug("Creating a new state.")

    @abstractproperty
    def resolution_cache(self) -> ResolutionCache:
        pass

    @abstractmethod
    def get_variables(self) -> Iterator[Variable]:
        pass
