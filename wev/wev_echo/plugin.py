from datetime import datetime, timedelta
from logging import Logger
from typing import List

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
        expires_at = datetime.now() + timedelta(seconds=60)
        support.logger.debug("Calculated expiry date: %s", expires_at)
        return Resolution.make(value=self.value, expires_at=expires_at)

    @property
    def value(self) -> str:
        """
        Gets the hard-coded value from the configuration.
        """
        try:
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
