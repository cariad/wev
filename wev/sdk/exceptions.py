from typing import Optional


class MissingConfigurationError(Exception):
    """
    Raised when a plugin cannot resolve a value because some required
    configuration is missing.

    Args:
        key:         The missing configuration key.

        explanation: Optional explanation for why the key is required. For
                     example, the key might be required only in some specific
                     scenarios.
    """

    def __init__(self, key: str, explanation: Optional[str] = None):
        message = f'The "{key}" configuration key is required'
        message = f"{message}: {explanation}" if explanation else f"{message}."
        super().__init__(message)
