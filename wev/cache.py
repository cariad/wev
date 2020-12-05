from json import dumps, loads
from logging import getLogger
from pathlib import Path
from typing import Dict, Optional

from wev.exceptions import CacheReadError
from wev.sdk import Resolution


class Cache:
    """
    Local cache of resolutions.

    Args:
        path: Path to cache. Uses the user's home directory by default.
    """

    def __init__(self, path: Optional[Path] = None) -> None:
        self.logger = getLogger("wev")
        self.path = path or Path.home().absolute().joinpath(".wevcache")
        self.resolutions: Dict[str, Resolution] = {}

    def get(self, var_name: str) -> Optional[Resolution]:
        """
        Gets a cached resolution.

        Args:
            var_name: Name of the environment variable.

        Returns:
            Resolution if cached, otherwise `None`.
        """
        return self.resolutions.get(var_name, None)

    def read(self) -> None:
        """
        Reads the cache file into memory.

        Raises:
            CacheReadError: The cache could not be read.
        """
        self.resolutions = {}
        self.logger.debug("Reading cache: %s", self.path)
        try:
            with open(self.path, "r") as stream:
                if content := stream.read().strip():
                    self.resolutions = loads(content)
                else:
                    self.logger.debug("Cache is empty: %s", self.path)
        except FileNotFoundError:
            self.logger.debug("Cache does not exist: %s", self.path)
        except Exception as ex:
            self.logger.error("Failed to read cache: %s", ex)
            raise CacheReadError(exception=ex, path=self.path)

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

    def update(self, var_name: str, resolution: Resolution) -> None:
        """
        Updates a cached resolution.

        Args:
            var_name:   Name of the environment variable.
            resolution: Resolution.
        """
        self.logger.debug("Updating %s in cache.", var_name)
        self.resolutions[var_name] = resolution

    def write(self) -> None:
        """
        Writes the cache file.
        """
        self.logger.debug("Writing cache: %s", self.path)
        with open(self.path, "w") as stream:
            stream.write(dumps(self.resolutions))