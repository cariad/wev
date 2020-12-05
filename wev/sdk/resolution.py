from datetime import datetime
from logging import getLogger
from typing import Any, Dict, Optional


class Resolution(dict):
    def __init__(self, values: Optional[Dict[str, Any]] = None) -> None:
        self.logger = getLogger("wev")
        if values:
            self.update(values)

    @classmethod
    def make(cls, value: str, expires_at: Optional[datetime] = None) -> "Resolution":
        values: Dict[str, Any] = {"value": value}

        if expires_at:
            values.update({"expires_at": expires_at.isoformat()})

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
    def seconds_until_expiry(self) -> Optional[int]:
        expires_at = self.expires_at

        if not expires_at:
            self.logger.debug(
                "%s is never cached, so will be considered expired.",
                self.variable_name,
            )
            return None

        seconds = int((expires_at - datetime.now()).total_seconds())

        if seconds > 0:
            self.logger.debug(
                "%s will expire in %s seconds at %s.",
                self.variable_name,
                seconds,
                expires_at,
            )
        else:
            self.logger.debug(
                "%s expired %s seconds ago at %s.",
                self.variable_name,
                0 - seconds,
                expires_at,
            )

        return seconds

    @property
    def value(self) -> str:
        return str(self["value"])
