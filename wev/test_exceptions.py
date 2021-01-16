from pathlib import Path

from wev.exceptions import (
    CacheReadError,
    IncorrectResolutionCountError,
    MultiplePluginsError,
    NoPluginError,
)


def test_cachereaderror() -> None:
    ex = CacheReadError(exception=Exception("cake is on fire"), path=Path("/foo"))
    assert str(ex) == 'Could not read cache at "/foo": cake is on fire'


def test_incorrectresolutioncounterror() -> None:
    ex = IncorrectResolutionCountError(
        plugin_id="foo",
        variable_count=1,
        resolution_count=2,
    )
    assert str(ex) == '"foo" resolved 2 variables but expected 1.'


def test_nopluginrerror() -> None:
    ex = NoPluginError(plugin_id="foo")
    assert str(ex) == '"foo" isn\'t installed. Try "pip3 install foo"?'


def test_multiplepluginsforhandlererror() -> None:
    ex = MultiplePluginsError(plugin_id="foo", count=3)
    assert str(ex) == '3 plugins are claiming to be "foo".'
