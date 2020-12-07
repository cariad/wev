from logging import Logger
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from ruamel.yaml import YAML

from wev.exceptions import CacheReadError
from wev.logging import get_logger
from wev.sdk import Resolution


class ResolutionCache:
    """
    Local cache of resolutions.

    Args:
        context: An environment variable could have different meanings in
                 different contexts. For example,
        path: Path to cache. Uses the user's home directory by default.
    """

    def __init__(
        self,
        context: str,
        logger: Optional[Logger] = None,
        path: Optional[Path] = None,
    ) -> None:
        if not context:
            raise ValueError("Cannot create a ResolutionCache with an empty context.")

        self.logger = logger or get_logger()
        self.context = context
        self.path = path or Path.home().absolute().joinpath(".wevcache")
        self.resolutions: Dict[Tuple[str, ...], Dict[str, Any]] = {}
        self.logger.debug(
            'ResolutionCache: context="%s" path="%s"',
            self.context,
            self.path,
        )

    def get(self, names: Tuple[str, ...]) -> Optional[Resolution]:
        """
        Gets a cached resolution, or `None` if not cached.
        """
        if store := self.resolutions.get(names, None):
            if values := store.get("values", None):
                if isinstance(values, list):
                    store["values"] = tuple(values)
            return Resolution(store=store)
        return None

    def read_all(self) -> Dict[str, Dict[Tuple[str, ...], Dict[str, Any]]]:
        """
        Reads the entire cache file.

        Raises `CacheReadError` if the cache cannot be read.
        """
        everything: Dict[str, Dict[Tuple[str, ...], Dict[str, Any]]] = {}
        self.logger.debug("Reading cache: %s", self.path)
        try:
            with open(self.path, "r") as stream:
                if content := stream.read().strip():
                    everything = YAML(typ="safe").load(content)
                    self.logger.debug("Read cache: %s", everything)
                else:
                    self.logger.debug("Cache is empty: %s", self.path)
        except FileNotFoundError:
            self.logger.debug("Cache does not exist: %s", self.path)
        except Exception as ex:
            self.logger.error("Failed to read cache: %s", ex)
            raise CacheReadError(exception=ex, path=self.path)
        return everything

    def load(self) -> None:
        """
        Reads the contextual cache.

        Raises `CacheReadError` if the cache cannot be read.
        """
        everything = self.read_all()
        self.resolutions = everything.get(self.context, {})

    def remove(self, names: Tuple[str, ...]) -> None:
        """
        Removes a cached resolution.

        Args:
            var_name: Name of the environment variable.
        """
        if names in self.resolutions:
            self.logger.debug("Removing %s from cache.", names)
            del self.resolutions[names]
        else:
            self.logger.debug("Could not remove %s from cache: not cached.", names)

    def save(self) -> None:
        """
        Writes the cache file.
        """
        self.logger.debug("Writing cache: %s", self.path)
        everything = self.read_all()
        everything[self.context] = self.resolutions
        self.logger.debug("Saving entire cache: %s", everything)
        with open(self.path, "w") as stream:
            yaml = YAML(typ="safe")
            yaml.dump(everything, stream)

    def update(self, names: Tuple, resolution: Resolution) -> None:
        """
        Updates a cached resolution.

        Args:
            var_name:   Name of the environment variable.
            resolution: Resolution.
        """
        self.logger.debug("Updating %s in cache: %s", names, resolution.store)
        self.resolutions[names] = resolution.store
