from datetime import datetime, timedelta
from typing import Iterator

from wev import ResolutionCache, Variable
from wev.state import BaseState


class MockState(BaseState):
    def __init__(self) -> None:
        self._resolution_cache = ResolutionCache(context="text")
        self.future = datetime.now() + timedelta(seconds=60)
        self.past = datetime.now() - timedelta(seconds=60)

    def get_variables(self) -> Iterator[Variable]:
        yield Variable(names=("alpha",), store={"plugin": {"id": "alpha-handler"}})

        yield Variable(
            names=("beta",),
            store={
                "plugin": {"id": "beta-handler"},
                "resolution": {"values": ("beta-value-old")},
            },
        )

        yield Variable(
            names=("gamma",),
            store={
                "plugin": {"id": "gamma-handler"},
                "resolution": {
                    "expires_at": self.future.isoformat(),
                    "values": ("gamma-value-old"),
                },
            },
        )

        yield Variable(
            names=("delta",),
            store={
                "plugin": {"id": "delta-handler"},
                "resolution": {
                    "expires_at": self.past.isoformat(),
                    "values": ("delta-value-old"),
                },
            },
        )

    @property
    def resolution_cache(self) -> ResolutionCache:
        return self._resolution_cache
