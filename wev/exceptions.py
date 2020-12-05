from pathlib import Path


class CacheReadError(Exception):
    """
    Raised when the cache cannot be read.
    """

    def __init__(self, exception: Exception, path: Path) -> None:
        super().__init__(f'Could not read cache at "{path}": {exception}')


class MultiplePluginsForHandlerError(Exception):
    """
    Raised when multiple plugins are installed for a given handler.
    """

    def __init__(self, handler: str, count: int) -> None:
        super().__init__(f'{count} plugins are installed for "{handler}".')


class NoPluginForHandlerError(Exception):
    """
    Raised when a plugin is not installed for a given handler.
    """

    def __init__(self, handler: str) -> None:
        super().__init__(f'No plugin installed for "{handler}".')
