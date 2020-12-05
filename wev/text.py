from datetime import datetime

from colorama import Style


def get_now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def bold(text: str) -> str:
    return styled(style=Style.BRIGHT, text=text)


def dim(text: str) -> str:
    return styled(style=Style.DIM, text=text)


def styled(style: int, text: str) -> str:
    return f"{style}{text}{Style.NORMAL}"
