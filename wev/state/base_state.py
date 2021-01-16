from abc import ABC, abstractmethod
from typing import Iterator

from wev import ResolutionCache, Variable
from wev.logging import get_logger


class BaseState(ABC):
    def __init__(self) -> None:
        self.logger = get_logger()
        self.logger.debug("Creating a new state.")

    @property
    @abstractmethod
    def resolution_cache(self) -> ResolutionCache:
        pass

    @abstractmethod
    def get_variables(self) -> Iterator[Variable]:
        pass
