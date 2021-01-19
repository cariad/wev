from typing import Tuple

from pytest import mark

from wev.text.normalize import displayable


@mark.parametrize(
    "value, expect",
    [
        ((), ""),
        (("one",), "one"),
        (("one", "two"), "one and two"),
        (("one", "two", "three"), "one, two and three"),
    ],
)
def test_displayable__tuple(value: Tuple[str, ...], expect: str) -> None:
    assert displayable(value) == expect
