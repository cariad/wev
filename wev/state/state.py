from typing import Iterator, Optional

from dwalk import dwalk

from wev import ResolutionCache, Variable
from wev.state import BaseState


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
        for var_name in self.config:
            values = {
                **self.config[var_name],
                "resolution": self.resolution_cache.get(var_name=var_name),
            }

            yield Variable(name=var_name, values=values)
