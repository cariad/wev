from datetime import datetime, timedelta
from logging import Logger
from typing import Any, Dict, List, Optional, Tuple

from wev.sdk import PluginBase, Resolution, ResolutionSupport
from wev.sdk.exceptions import CannotResolveError


class MockPlugin(PluginBase):
    """
    A mock plugin for testing.

    `raises_cannot_resolve_error` will cause resolution to raise
    `CannotResolveError`.

    `return_value` describes the value to return from resolution.

    `return_expires_at` will cause resolution to return an expiry date 60
    seconds in the future.
    """

    def __init__(
        self,
        values: Dict[Any, Any],
        raises_cannot_resolve_error: Optional[bool] = False,
        return_value: Optional[Tuple[str, ...]] = None,
        return_expires_at: Optional[bool] = False,
    ) -> None:
        super().__init__(values)
        self.raises_cannot_resolve_error = raises_cannot_resolve_error
        self.return_value = return_value
        self.return_expires_at = (
            datetime.now() + timedelta(seconds=60) if return_expires_at else None
        )

    def explain(self, logger: Logger) -> List[str]:
        return ["(explanation)"]

    def resolve(self, support: ResolutionSupport) -> Resolution:
        if self.raises_cannot_resolve_error:
            raise CannotResolveError("cannot reticulate splines")
        return Resolution.make(
            value=self.return_value,
            expires_at=self.return_expires_at,
        )

    @property
    def version(self) -> str:
        return "1.2.3"
