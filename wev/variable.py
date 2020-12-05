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
        self.name = name
        self.update(values)

    @property
    def configuration(self) -> Any:
        """
        Gets the handler's configuration.

        Returns:
            Handler's configuration.
        """
        return self["configuration"]

    @property
    def handler(self) -> str:
        """
        Gets the name of the handler.

        Returns:
            Handler.
        """
        return str(self["handler"])

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
