from logging import getLogger
from subprocess import run
from typing import List

from colorama import Style

from wev.resolver import resolve


def execute(command: List[str]) -> int:
    """
    Executes the command with environment variables.

    Args:
        command: Shell command.

    Returns:
        Shell return code.
    """
    logger = getLogger("wev")
    variables = resolve()
    logger.info("Starting %s%s%s...", Style.BRIGHT, command[0], Style.RESET_ALL)
    return run(command, env=variables).returncode
