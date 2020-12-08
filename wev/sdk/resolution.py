from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple, Union

from pytz import UTC

from wev.logging import get_logger


class Resolution:
    def __init__(self, store: Dict[str, Any]) -> None:
        self.logger = get_logger()

        # Don't log the store; it probably contains confidential information.
        self.logger.debug("Initialising new Resolution.")

        if not isinstance(store, dict):
            raise ValueError(
                'Resolution "store" is not a dictionary: %s',
                type(store),
            )
        self.store = store

    def __eq__(self, other: Any) -> bool:
        self.logger.debug('Checking if "%s" == "%s".', self, other)
        return isinstance(other, Resolution) and self.store == other.store

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return str(self.store)

    @classmethod
    def make(
        cls,
        value: Optional[Union[str, Tuple[str, ...]]] = None,
        expires_at: Optional[datetime] = None,
    ) -> "Resolution":
        """
        Makes a `Resolution` to describe a value and the duration to cache it.

        Args:
            value:      Environment variable value, or `None` to not set.
            expires_at: Time to cache the value until. `None` to not cache.

        Returns:
            Resolution.
        """
        store: Dict[str, Any] = {}
        if value is not None:
            if isinstance(value, str):
                store.update({"values": (value,)})
            else:
                store.update({"values": value})
        if expires_at:
            store.update({"expires_at": expires_at.isoformat()})

        # Don't log the store; it contains confidential information.
        get_logger().debug('"Resolution.make" created a new store.')
        return Resolution(store=store)

    @property
    def expires_at(self) -> Optional[datetime]:
        if expires_at := self.store.get("expires_at", None):
            dt = datetime.fromisoformat(str(expires_at))
            if not dt.tzinfo:
                dt = UTC.localize(dt)
                self.logger.debug(
                    '"expires_at" (%s) has been localized to UTC: %s',
                    expires_at,
                    dt,
                )
            return dt
        return None

    def now(self) -> datetime:
        return datetime.now(timezone.utc)

    @property
    def should_read_from_cache(self) -> bool:
        return not not (self.expires_at and self.now() < self.expires_at)

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
        return int((self.expires_at - self.now()).total_seconds())

    @property
    def time_until_expiry(self) -> str:
        if self.seconds_until_expiry is None:
            return "immediately"
        elif self.seconds_until_expiry > 0:
            return f"in {self.seconds_until_expiry:n} seconds"
        else:
            return f"{0-self.seconds_until_expiry:n} seconds ago"

    @property
    def values(self) -> Tuple[str, ...]:
        # Don't log the store; it's confidential.
        self.logger.debug("Reading the resolved value.")
        values = self.store.get("values", [])
        if isinstance(values, tuple):
            return values
        return (values,)
