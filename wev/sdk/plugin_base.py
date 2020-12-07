from abc import ABC, abstractmethod
from logging import Logger
from typing import List

from wev.sdk import Resolution, ResolutionSupport

# from wev.sdk.exceptions import CannotPrepareError


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

    # @property
    # def plugin_configuration(self) -> PluginConfiguration:
    #     """
    #     Gets the plugin configuration (from the "plugin" key of the
    #     configuration file).
    #     """
    #     try:
    #         return PluginConfiguration(self["plugin"])
    #     except KeyError:
    #         raise CannotPrepareError(self)
