from pathlib import Path

from wev.exceptions import CacheReadError, MultiplePluginsError, NoPluginError


def test_cachereaderror() -> None:
    ex = CacheReadError(exception=Exception("cake is on fire"), path=Path("/foo"))
    assert str(ex) == 'Could not read cache at "/foo": cake is on fire'


def test_nopluginrerror() -> None:
    ex = NoPluginError(plugin_id="foo")
    assert str(ex) == '"foo" isn\'t installed. Try "pip3 install foo"?'


def test_multiplepluginsforhandlererror() -> None:
    ex = MultiplePluginsError(plugin_id="foo", count=3)
    assert str(ex) == '3 plugins are claiming to be "foo".'
