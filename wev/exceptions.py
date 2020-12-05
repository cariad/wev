class HandlerNotInstalled(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(f'The plugin "{name}" is not installed.')
