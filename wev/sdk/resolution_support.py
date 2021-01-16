from logging import Logger
from typing import Callable


class ResolutionSupport:
    """
    Helps plugins to resolve values.

    Arguments:
        confidential_prompt: A function for requesting runtime confidential
                             information from the user.

                             The first argument prescribes a short preamble, and
                             the second is the short prompt to print next to the
                             input cursor.

                             The function returns the user-entered string.

        logger:              Logger. Plugins should use this rather than
                             instantiate their own.
    """

    def __init__(
        self,
        confidential_prompt: Callable[[str, str], str],
        logger: Logger,
    ) -> None:
        self.logger: Logger = logger
        self.confidential_prompt: Callable[[str, str], str] = confidential_prompt
