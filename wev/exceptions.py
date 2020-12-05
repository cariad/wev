from pathlib import Path


class CacheReadError(Exception):
    """
    Raised when the cache cannot be read.
    """

    def __init__(self, exception: Exception, path: Path) -> None:
        super().__init__(f'Could not read cache at "{path}": {exception}')


class HandlerNotInstalled(Exception):
    """
    Raised when a required handler is not installed.
    """

    def __init__(self, name: str) -> None:
        super().__init__(f'The plugin "{name}" is not installed.')
