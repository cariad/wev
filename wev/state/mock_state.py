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
        yield Variable(name="alpha", values={"handler": "alpha-handler"})

        yield Variable(
            name="beta",
            values={
                "handler": "beta-handler",
                "resolution": {"value": "beta-value-old"},
            },
        )

        yield Variable(
            name="gamma",
            values={
                "handler": "gamma-handler",
                "resolution": {
                    "expires_at": self.future.isoformat(),
                    "value": "gamma-value-old",
                },
            },
        )

        yield Variable(
            name="delta",
            values={
                "handler": "delta-handler",
                "resolution": {
                    "expires_at": self.past.isoformat(),
                    "value": "delta-value-old",
                },
            },
        )

    @property
    def resolution_cache(self) -> ResolutionCache:
        return self._resolution_cache
