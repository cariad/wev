from datetime import datetime
from logging import getLogger
from typing import Any, Dict, Optional


class Resolution(dict):
    def __init__(self, values: Optional[Dict[str, Any]] = None) -> None:
        self.logger = getLogger("wev")
        if values:
            self.update(values)

    @classmethod
    def make(
        cls, value: Optional[str] = None, expires_at: Optional[datetime] = None
    ) -> "Resolution":
        """
        Makes a `Resolution` to describe a value and the duration to cache it.

        Args:
            value:      Environment variable value, or `None` to not set.
            expires_at: Time to cache the value until. `None` to not cache.

        Returns:
            Resolution.
        """
        values: Dict[str, Any] = {}
        if value is not None:
            values.update({"value": value})
        if expires_at:
            values.update({"expires_at": expires_at.isoformat()})
        getLogger("wev").debug(values)
        return Resolution(values)

    @property
    def variable_name(self) -> Optional[str]:
        if variable_name := self.get("variable_name", None):
            return str(variable_name)
        return None

    @property
    def expires_at(self) -> Optional[datetime]:
        if expires_at := self.get("expires_at", None):
            return datetime.fromisoformat(expires_at)
        return None

    @property
    def should_read_from_cache(self) -> bool:
        return not not (self.expires_at and datetime.now() < self.expires_at)

    @property
    def explain_cache(self) -> str:
        if self.seconds_until_expiry is None:
            return "The value is never cached."
        elif self.seconds_until_expiry > 0:
            return f"The cached value will expire {self.time_until_expiry}."
        else:
            return f"The cached value expired {self.time_until_expiry}."

    @property
    def seconds_until_expiry(self) -> Optional[int]:
        if not self.expires_at:
            return None
        return int((self.expires_at - datetime.now()).total_seconds())

    @property
    def time_until_expiry(self) -> str:
        if self.seconds_until_expiry is None:
            return "immediately"
        elif self.seconds_until_expiry > 0:
            return f"in {self.seconds_until_expiry:n} seconds"
        else:
            return f"{0-self.seconds_until_expiry:n} seconds ago"

    @property
    def value(self) -> str:
        self.logger.debug("Reading the resolved value: %s", self)
        return str(self["value"])
