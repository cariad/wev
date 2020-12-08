from typing import Any, Dict, Optional, Tuple

from wev.logging import get_logger
from wev.sdk import PluginConfiguration, Resolution


class Variable:
    """
    Represents the configuration for an environment variable.
    """

    def __init__(self, names: Tuple[str, ...], store: Dict[str, Any]) -> None:
        self.logger = get_logger()

        # Don't log the values; they're probably confidential.
        self.logger.debug('Variable: name="%s"', names)

        if "resolution" in store and not isinstance(store["resolution"], dict):
            raise ValueError(
                '"resolution" is not a dictionary: %s',
                type(store["resolution"]),
            )

        self.names = names
        self.store = store

    @property
    def plugin(self) -> PluginConfiguration:
        """
        Gets the plugin configuration.
        """
        try:
            return PluginConfiguration(self.store["plugin"])
        except KeyError:
            raise ValueError(f'"plugin" not defined in variable: {self.store}')
        except ValueError as ex:
            raise ValueError(
                f'Cannot create PluginConfiguration with: {self.store["plugin"]} ({ex})'
            )

    @property
    def resolution(self) -> Optional[Resolution]:
        """
        Gets the resolution.
        """
        if store := self.store.get("resolution", None):
            return Resolution(store=store)
        return None

    @property
    def should_read_from_cache(self) -> bool:
        return not not (self.resolution and self.resolution.should_read_from_cache)
