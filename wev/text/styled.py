from typing import Tuple, Union

from colorama import Style

from wev.text.normalize import displayable


def bold(text: Union[str, Tuple[str, ...]]) -> str:
    return styled(style=Style.BRIGHT, text=text)


def dim(text: Union[str, Tuple[str, ...]]) -> str:
    return styled(style=Style.DIM, text=text)


def styled(style: int, text: Union[str, Tuple[str, ...]]) -> str:
    displayed = displayable(text) if isinstance(text, tuple) else text
    return f"{style}{displayed}{Style.NORMAL}"
