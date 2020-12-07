from typing import Tuple


def displayable(value: Tuple[str, ...]) -> str:
    """
    Returns a readable form of the value.
    """
    if len(value) == 0:
        return ""

    if len(value) == 1:
        return value[0]

    return " and ".join([", ".join(value[:-1]), value[-1]])
