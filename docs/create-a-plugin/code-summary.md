The finished `plugin.py` should look something like this:

```python
from datetime import datetime, timedelta
from logging import Logger
from typing import List, Optional

from wev.sdk import PluginBase, Resolution, ResolutionSupport


class Plugin(PluginBase):

    @property
    def cache_duration(self) -> int:
        return int(self.get("cache_duration", 30))

    def explain(self, logger: Logger) -> List[str]:
        plan: List[str] = []
        plan.append(
            "You will be prompted to enter a special value, which will be "
            f"cached for {self.cache_duration} seconds.",
        )
        if self.force_case:
            plan.append(
                f"The value will be translated to {self.force_case} case."
            )
        return plan

    @property
    def force_case(self) -> Optional[str]:
        return self.get("force_case", None)

    def resolve(self, support: ResolutionSupport) -> Resolution:
        value = support.confidential_prompt("Please enter any value.", "Value:")

        if self.force_case == "upper":
            value = value.upper()
        elif self.force_case == "lower":
            value = value.lower()

        return Resolution.make(
            value=value,
            expires_at=datetime.now() + timedelta(seconds=self.cache_duration),
        )

    @property
    def version(self) -> str:
        """ Gets the plugin's version. """
        return "1.0.0"
```

Your directory structure should look something like this:

```text
~/wev-ask/wev_ask/__init__.py
~/wev-ask/wev_ask/plugin.py
~/wev-ask/setup.py
```
