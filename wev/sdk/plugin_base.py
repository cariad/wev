from abc import ABC, abstractmethod
from logging import Logger
from typing import List

from wev.sdk import Resolution, ResolutionSupport


class PluginBase(ABC, dict):
    @abstractmethod
    def explain(self, logger: Logger) -> List[str]:
        """
        Gets a human-readable explanation of how this plugin will resolve the
        environment variable.

        `logger` should be used for logging debug information and not for
        returning the explanation.
        """
        pass

    @abstractmethod
    def resolve(self, support: ResolutionSupport) -> Resolution:
        """
        Resolves the environment variable.
        """
        pass
