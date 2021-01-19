from re import match
from typing import Iterator, Optional, Tuple

from dwalk import dwalk

from wev import ResolutionCache, Variable
from wev.state import BaseState


class State(BaseState):
    def __init__(self) -> None:
        super().__init__()
        self.config = dwalk(
            filenames=[
                ".wev.yml",
                "wev.yml",
                ".wev.user.yml",
                "wev.user.yml",
            ],
            include_meta=True,
        )
        self.logger.debug("Merged configuration: %s", self.config)
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
        try:
            for key in self.config:
                if isinstance(key, str) and match(r"__(.+)__", key):
                    self.logger.debug('Ignoring configuration key "%s".', key)
                    continue

                names: Tuple[str, ...] = key if isinstance(key, tuple) else (key,)

                self.logger.debug(
                    'Configuration describes a variable named "%s".',
                    names,
                )

                store = self.config[key]

                if cached_resolution := self.resolution_cache.get(names):
                    # Don't log the resolution; the values are probably
                    # confidential.
                    self.logger.debug("Adding cached resolution.")
                    store.update({"resolution": cached_resolution.store})

                yield Variable(names=names, store=store)

        except Exception as ex:
            self.logger.exception(ex)
