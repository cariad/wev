from datetime import datetime, timedelta
from logging import Logger
from typing import List, Union

from wev.sdk import PluginBase, Resolution, ResolutionSupport
from wev.sdk.exceptions import MissingConfigurationError


class Plugin(PluginBase):
    """
    The `wev-echo` plugin.
    """

    def explain(self, logger: Logger) -> List[str]:
        """
        Gets a human-readable explanation of how this plugin will resolve the
        environment variable.

        `logger` should be used for logging and not for returning the
        explanation.
        """
        logger.debug("Returning plain explanation...")
        return [
            "The environment variable will be set directly to the configured value."
        ]

    def resolve(self, support: ResolutionSupport) -> Resolution:
        """
        Resolves the environment variable.

        Args:
            logger: Logger. Do not log confidential information.

        Returns:
            Resolution.
        """
        value = (
            self.value
            if isinstance(self.value, str)
            else self.separator.join(self.value)
        )
        return Resolution.make(
            value=value,
            expires_at=datetime.now() + timedelta(seconds=60),
        )

    @property
    def separator(self) -> str:
        """ Gets the single value to return. """
        return self.get("separator", " ")

    @property
    def value(self) -> Union[str, List[str]]:
        """ Gets the single value or list of values to return. """
        try:
            if isinstance(self["value"], list):
                return self["value"]
            return str(self["value"])
        except KeyError as ex:
            raise MissingConfigurationError(
                explanation="This is the value that will be echoed.",
                key=str(ex),
            )

    @property
    def version(self) -> str:
        """ Gets the plugin's version. """
        return "1.0.0"
