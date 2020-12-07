from logging import Logger
from typing import Callable


class ResolutionSupport:
    def __init__(
        self, logger: Logger, confidential_prompt: Callable[[str, str], str]
    ) -> None:
        self.logger = logger
        self.confidential_prompt = confidential_prompt
