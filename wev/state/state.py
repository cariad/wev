from re import match
from typing import Iterator, Optional

from dwalk import dwalk

from wev import ResolutionCache, Variable
from wev.state import BaseState
from copy import deepcopy


class State(BaseState):
    def __init__(self) -> None:
        super().__init__()
        self.config = dwalk(filenames=[".wev.yml", ".wev.user.yml"], include_meta=True)
        self.logger.debug("Getting context...")
        self.context = self.config["__dwalk__"]["__dwalk__"]["most_specific_src"]
        self._resolution_cache: Optional[ResolutionCache] = None
        self.logger.debug("Created state.")

    @property
    def resolution_cache(self) -> ResolutionCache:
        if not self._resolution_cache:
            self._resolution_cache = ResolutionCache(self.context)
            self._resolution_cache.load()
        return self._resolution_cache

    def get_variables(self) -> Iterator[Variable]:
        self.logger.debug("Starting a new variables iteration.")
        for name in self.config:
            if match(r"__(.+)__", name):
                self.logger.debug('Ignoring configuration key "%s".', name)
                continue

            self.logger.debug('Configuration describes a variable named "%s".', name)
            values = deepcopy(self.config[name])
            self.logger.debug('Configuration values: %s', values)

            if cached_resolution := self.resolution_cache.get(var_name=name):
                self.logger.debug("Adding cached resolution: %s", cached_resolution)
                values.update({"resolution": cached_resolution})

            yield Variable(name=name, values=values)
