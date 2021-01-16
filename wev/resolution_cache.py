from logging import Logger
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, cast

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
                    store["values"] = tuple(cast(List[str], values))
            return Resolution(store=store)
        return None

    def read_all(self) -> Dict[str, Dict[Tuple[str, ...], Dict[str, Any]]]:
        """
        Reads the entire cache file.

        Raises `CacheReadError` if the cache cannot be read.
        """
        everything: Dict[str, Dict[Tuple[str, ...], Dict[str, Any]]] = {}
        self.logger.debug("Reading entire cache: %s", self.path)
        try:
            with open(self.path, "r") as stream:
                if content := stream.read().strip():
                    everything = YAML(typ="safe").load(content)
                    # Don't log the cache; it contains confidential information.
                    self.logger.debug("Successfully read the entire cache.")
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
        # Don't log the cache; it contains confidential information.
        self.logger.debug("Saving the entire cache: %s", self.path)
        with open(self.path, "w") as stream:
            YAML(typ="safe").dump(everything, stream)
            self.logger.debug("Successfully saved the entire cache.")

    def update(self, names: Tuple[str, ...], resolution: Resolution) -> None:
        """
        Updates a cached resolution.

        Args:
            names:      Names of the environment variable.
            resolution: Resolution.
        """
        # Don't log the store; it's confidential.
        self.logger.debug("Updating %s in cache.", names)
        self.resolutions[names] = resolution.store
