from pathlib import Path

from wev.exceptions import (
    CacheReadError,
    MultiplePluginsForHandlerError,
    NoPluginForHandlerError,
)


def test_cachereaderror() -> None:
    ex = CacheReadError(exception=Exception("cake is on fire"), path=Path("/foo"))
    assert str(ex) == 'Could not read cache at "/foo": cake is on fire'


def test_nopluginforhandlererror() -> None:
    ex = NoPluginForHandlerError(handler="foo")
    assert str(ex) == 'No plugin installed for "foo".'


def test_multiplepluginsforhandlererror() -> None:
    ex = MultiplePluginsForHandlerError(handler="foo", count=3)
    assert str(ex) == '3 plugins are installed for "foo".'
