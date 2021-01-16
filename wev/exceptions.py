from pathlib import Path


class CacheReadError(Exception):
    """
    Raised when the cache cannot be read.
    """

    def __init__(self, exception: Exception, path: Path) -> None:
        super().__init__(f'Could not read cache at "{path}": {exception}')


class MultiplePluginsError(Exception):
    """
    Raised when multiple plugins are installed for a given handler.
    """

    def __init__(self, plugin_id: str, count: int) -> None:
        super().__init__(f'{count} plugins are claiming to be "{plugin_id}".')


class NoPluginError(Exception):
    """
    Raised when a plugin is not installed for a given handler.
    """

    def __init__(self, plugin_id: str) -> None:
        super().__init__(
            f'"{plugin_id}" isn\'t installed. Try "pip3 install {plugin_id}"?'
        )


class IncorrectResolutionCountError(Exception):
    """
    Raised when the number of resolutions does not match the number of variables.
    """

    def __init__(
        self,
        plugin_id: str,
        variable_count: int,
        resolution_count: int,
    ) -> None:
        super().__init__(
            f'"{plugin_id}" resolved {resolution_count} variables but expected '
            f"{variable_count}."
        )
