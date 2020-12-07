from logging import Logger, basicConfig

from pytest import fixture

from wev.logging import get_logger
from wev.sdk import ResolutionSupport


@fixture
def logger() -> Logger:
    basicConfig()
    logger = get_logger()
    logger.setLevel(level="DEBUG")
    return logger


@fixture
def resolution_support() -> ResolutionSupport:
    return ResolutionSupport(
        logger=get_logger(),
        confidential_prompt=confidential_prompt,
    )


def confidential_prompt(preamble: str, prompt: str) -> str:
    return f"preamble={preamble} prompt={prompt}"
