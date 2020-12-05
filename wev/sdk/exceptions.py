from typing import Optional


class MissingConfigurationError(Exception):
    def __init__(self, key: str, explanation: Optional[str] = None):
        value = f'The "{key}" configuration key is required'

        if explanation:
            value = f"{value}: {explanation}"
        else:
            value = f"{value}."

        super().__init__(explanation)
