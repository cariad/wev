from json import dumps, loads
from logging import getLogger
from pathlib import Path
from typing import Dict, Optional

from wev.sdk import Resolution


class Cache:
    def __init__(self) -> None:
        self.logger = getLogger("wev")
        self.path = Path.home().absolute().joinpath(".wevcache")
        self.resolutions: Dict[str, Resolution] = {}

    def read(self) -> None:
        self.logger.debug("Reading cache: %s", self.path)
        try:
            with open(self.path, "r") as stream:
                if content := stream.read().strip():
                    self.resolutions = loads(content)
                else:
                    self.logger.debug("Cache is empty: %s", self.path)
        except FileNotFoundError:
            self.logger.debug("Cache does not exist: %s", self.path)
            self.resolutions = {}

    def write(self) -> None:
        self.logger.debug("Writing cache: %s", self.path)
        with open(self.path, "w") as stream:
            stream.write(dumps(self.resolutions))

    def get(self, var_name: str) -> Optional[Resolution]:
        return self.resolutions.get(var_name, None)

    def update(self, var_name: str, resolution: Resolution) -> None:
        self.resolutions[var_name] = resolution

    def remove(self, var_name: str) -> None:
        if var_name in self.resolutions:
            del self.resolutions[var_name]
