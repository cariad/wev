from datetime import datetime, timedelta
from logging import Logger
from typing import Any, Dict, List

from wev.sdk import PluginBase, Resolution
from wev.sdk.exceptions import MissingConfigurationError


class Plugin(PluginBase):
    def __init__(self, config: Dict[Any, Any]) -> None:
        self.config = WevEchoConfig(config)

    def explain(self) -> List[str]:
        return [
            f'The environment variable will be set directly to "{self.config.value}".'
        ]

    def resolve(self, logger: Logger) -> Resolution:
        expires_at = datetime.now() + timedelta(seconds=60)
        logger.debug("Calculated expiry date: %s", expires_at)
        return Resolution.make(value=self.config.value, expires_at=expires_at)


class WevEchoConfig(dict):
    def __init__(self, values: Dict[Any, Any]) -> None:
        self.update(values)

    @property
    def value(self) -> str:
        try:
            return str(self["value"])
        except KeyError:
            raise MissingConfigurationError(
                key="value",
                explanation="This is the value that will be echoed.",
            )
