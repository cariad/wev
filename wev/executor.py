from subprocess import run
from typing import List

from wev.logging import get_logger
from wev.resolver import resolve


def execute(command: List[str]) -> int:
    """
    Executes the command with environment variables.

    Args:
        command: Shell command.

    Returns:
        Shell return code.
    """
    logger = get_logger()
    variables = resolve()
    logger.debug("Starting %s...", command[0])
    return run(command, env=variables).returncode
