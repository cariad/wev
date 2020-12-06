from logging import getLogger
from typing import Any, Dict, Optional

from wev.sdk import Resolution


class Variable(dict):
    """
    Represents the configuration for an environment variable.

    Arguments:
        name (str):    Environment variable name.
        values (dict): Configuration values.
    """

    def __init__(self, name: str, values: Dict[str, Any]) -> None:
        self.logger = getLogger("wev")
        self.logger.debug('Variable: name="%s" values="%s"', name, values)
        self.name = name
        self.update(values)

    @property
    def configuration(self) -> Dict[Any, Any]:
        """
        Gets the handler's configuration.

        Returns:
            Handler's configuration.
        """
        configuration: Dict[Any, Any] = self.get("configuration", {})
        if not configuration:
            self.logger.debug("%s has no configuration.", self.name)
        return configuration

    @property
    def handler(self) -> str:
        """
        Gets the name of the handler.

        Returns:
            Handler.
        """
        try:
            return str(self["handler"])
        except KeyError:
            raise KeyError(f'"handler" not set in variable: {self}')

    @property
    def resolution(self) -> Optional[Resolution]:
        """
        Gets the most-recent resolution.

        Returns:
            Resolution.
        """
        if resolution := self.get("resolution", None):
            r = Resolution(resolution)
            r["variable_name"] = self.name
            return r
        return None

    @property
    def should_read_from_cache(self) -> bool:
        return not not (self.resolution and self.resolution.should_read_from_cache)
