from datetime import datetime, timedelta
from logging import Logger
from typing import List

from wev.sdk import PluginBase, Resolution, ResolutionSupport


class MockPlugin(PluginBase):
    def explain(self, logger: Logger) -> List[str]:
        return ["(explanation)"]

    def resolve(self, support: ResolutionSupport) -> Resolution:
        return Resolution.make(
            value="(value)", expires_at=datetime.now() + timedelta(seconds=60)
        )
