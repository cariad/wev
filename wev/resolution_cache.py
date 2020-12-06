from json import dumps, loads
from logging import getLogger
from pathlib import Path
from typing import Dict, Optional

from wev.exceptions import CacheReadError
from wev.sdk import Resolution


class ResolutionCache:
    """
    Local cache of resolutions.

    Args:
        context: An environment variable could have different meanings in
                 different contexts. For example,
        path: Path to cache. Uses the user's home directory by default.
    """

    def __init__(self, context: str, path: Optional[Path] = None) -> None:
        self.logger = getLogger("wev")
        self.context = context
        self.path = path or Path.home().absolute().joinpath(".wevcache.json")
        self.resolutions: Dict[str, Resolution] = {}
        self.logger.debug(
            'ResolutionCache: context="%s" path="%s"',
            self.context,
            self.path,
        )

    def get(self, var_name: str) -> Optional[Resolution]:
        """
        Gets a cached resolution.

        Args:
            var_name: Name of the environment variable.

        Returns:
            Resolution if cached, otherwise `None`.
        """
        return self.resolutions.get(var_name, None)

    def read_all(self) -> Dict[str, Dict[str, Resolution]]:
        """
        Reads the entire cache file.

        Raises `CacheReadError` if the cache cannot be read.
        """
        everything: Dict[str, Dict[str, Resolution]] = {}
        self.logger.debug("Reading cache: %s", self.path)
        try:
            with open(self.path, "r") as stream:
                if content := stream.read().strip():
                    everything = loads(content)
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
        self.resolutions = self.read_all().get(self.context, {})

    def remove(self, var_name: str) -> None:
        """
        Removes a cached resolution.

        Args:
            var_name: Name of the environment variable.
        """
        if var_name in self.resolutions:
            self.logger.debug("Removing %s from cache.", var_name)
            del self.resolutions[var_name]
        else:
            self.logger.debug("Could not remove %s from cache: not cached.", var_name)

    def save(self) -> None:
        """
        Writes the cache file.
        """
        self.logger.debug("Writing cache: %s", self.path)
        everything = self.read_all()
        everything[self.context] = self.resolutions
        with open(self.path, "w") as stream:
            stream.write(dumps(everything, indent=2, sort_keys=True))

    def update(self, var_name: str, resolution: Resolution) -> None:
        """
        Updates a cached resolution.

        Args:
            var_name:   Name of the environment variable.
            resolution: Resolution.
        """
        self.logger.debug("Updating %s in cache.", var_name)
        self.resolutions[var_name] = resolution
