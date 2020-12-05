from pathlib import Path

from wev.exceptions import CacheReadError, HandlerNotInstalled


def test_cachereaderror() -> None:
    ex = CacheReadError(exception=Exception("cake is on fire"), path=Path("/foo"))
    assert str(ex) == 'Could not read cache at "/foo": cake is on fire'


def test_handlernotinstallederror() -> None:
    ex = HandlerNotInstalled(name="foo")
    assert str(ex) == 'The plugin "foo" is not installed.'
