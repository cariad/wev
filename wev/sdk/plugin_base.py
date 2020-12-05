from abc import ABC, abstractmethod
from logging import Logger
from typing import List

from wev.sdk import Resolution


class PluginBase(ABC, dict):
    @abstractmethod
    def explain(self) -> List[str]:
        """
        Gets a human-readable explanation of how this plugin will resolve the
        environment variable.

        Returns:
            Explanation.
        """
        pass

    @abstractmethod
    def resolve(self, logger: Logger) -> Resolution:
        """
        Resolves the environment variable.

        Args:
            logger: Logger. Do not log confidential information.

        Returns:
            Resolution.
        """
        pass
