## Plugin class

Create `plugin.py` inside your package directory.

Stub an implementation of the abstract `wev.sdk.PluginBase` class:

```python
from logging import Logger
from typing import List

from wev.sdk import PluginBase, Resolution, ResolutionSupport

class Plugin(PluginBase):
    def explain(self, logger: Logger) -> List[str]:
        pass

    def resolve(self, support: ResolutionSupport) -> Resolution:
        pass

    @property
    def version(self) -> str:
        pass
```

## Reading configuration

For your plugin to be invoked, the user must have a `.wev.yml` configuration that refers to it.

Our example plugin will resolve to whatever the user enters, but let's say we want the option to translate the input to upper or lower case.

The user's configuration could look something like this:

```yaml
DEFAULT_FOO:
  plugin:
    id: wev-ask

LOWER_FOO:
  plugin:
    id: wev-ask
    force_case: lower

UPPER_FOO:
  plugin:
    id: wev-ask
    force_case: upper
```

To read this configuration, treat your `Plugin` clas instance as a dictionary.

For example, to read the `force_case` configuration and default to `None` if it's not set:

```python
@property
def force_case(self) -> Optional[str]:
    return self.get("force_case", None)
```

## explain() function

The `explain` function returns a human-readable list of strings that describe what the plugin will do.

!!! warning
    Do **not** return the actual resolved value.

    This function is expected to run quickly and not expose private information.

The `logger` can be used to log any useful debugging information, but the explanation _must_ be returned as a list.

For our example, the plugin will:

1. Prompt the user for a value.
1. Cache it.
1. Potentially translate the casing.

```python
def explain(self, logger: Logger) -> List[str]:
    plan: List[str] = []
    plan.append("You will be prompted to enter a special value, which will be cached for {self.cache_duration} seconds.")
    if self.force_case:
        plan.append(f"The value will be translated to {self.force_case} case.")
    return plan
```

## resolve() function

The `resolve` function resolves and returns the value for the environment variable.

A `ResolutionSupport` instance will be passed in, which gives you:

- `confidential_prompt`: A function for getting a string from the user. The first argument is a short preamble. The second argument is the prompt.
- `logger`: A logger for any useful debugging. Take care not to log any private values, since users might share their logs in bug reports.

The function expects a `wev.sdk.Resolution` instance to be returned. This class has a static `make` function to help you out, with the following arguments:

- `value`: The resolved value. Set to a _string_ to return a single value or a _tuple_ for multiple values (for example, if your plugin sets several environment variables to different parts of a set of credentials).
- `expires_at`: An optional _datetime_ which prescribes when the cached value should expire. Omit to not cache the value.

For our example, the plugin will:

1. Prompt the user to enter a string.
1. Translate the casing (if configured to).
1. Return the resolved value with a cache expiry date.

```python
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

```

## version property

The `version` property returns the plugin's version.

The value and format are currently used only in logging and aren't significant, but I recommend sementic versioning.

```python
@property
def version(self) -> str:
    return "1.0.0"
```
